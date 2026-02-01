# --------------------------------------------------------------------------------------------
# Copyright (c) Ben Coleman, 2026. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import urllib.parse
from datetime import datetime, timezone
from knack.util import CLIError
from azure.cli.core._profile import Profile
import requests

# PIM API Constants
PIM_API_SCOPE = "https://api.azrbac.mspim.azure.com"
PIM_API_BASE_URL = (
    "https://api.azrbac.mspim.azure.com/api/v2/privilegedAccess/aadGroups"
)


def get_pim_token(cli_ctx):
    """Get an access token for the PIM API."""
    profile = Profile(cli_ctx=cli_ctx)

    # Get access token for PIM API scope
    token_info, _, _ = profile.get_raw_token(resource=PIM_API_SCOPE)
    return token_info[1]


def get_user_id(cli_ctx):
    """Get the current user's object ID using Microsoft Graph signed-in user API."""
    from azext_pim._client_factory import _graph_client_factory

    client = _graph_client_factory(cli_ctx)
    user = client.signed_in_user_get()
    return user["id"]


def pim_api_request(cli_ctx, method, url, body=None):
    """Make an authenticated request to the PIM API."""
    token = get_pim_token(cli_ctx)

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    if method.upper() == "GET":
        response = requests.get(url, headers=headers)
    elif method.upper() == "POST":
        response = requests.post(url, headers=headers, json=body)
    else:
        raise CLIError(f"Unsupported HTTP method: {method}")

    if response.status_code < 200 or response.status_code >= 300:
        try:
            error_data = response.json()
            if "error" in error_data and "message" in error_data["error"]:
                raise CLIError(error_data["error"]["message"])
        except (json.JSONDecodeError, KeyError):
            pass
        raise CLIError(f"PIM API error: {response.status_code} - {response.text}")

    if response.text:
        return response.json()
    return None


def get_role_assignments(cli_ctx, user_id, assignment_state):
    """Get role assignments for the current user."""
    filter_query = f"subjectId eq '{user_id}'"
    if assignment_state:
        filter_query += f" and assignmentState eq '{assignment_state}'"

    url = f"{PIM_API_BASE_URL}/roleAssignments?$filter={urllib.parse.quote(filter_query)}&$expand=resource,roleDefinition"

    response = pim_api_request(cli_ctx, "GET", url)
    return response.get("value", [])


def get_role_assignment_requests(cli_ctx, user_id, status):
    """Get role assignment requests for the current user."""
    filter_query = f"subjectId eq '{user_id}'"
    if status:
        filter_query += f" and status/subStatus eq '{status}'"

    url = f"{PIM_API_BASE_URL}/roleAssignmentRequests?$filter={urllib.parse.quote(filter_query)}&$expand=resource,roleDefinition"

    response = pim_api_request(cli_ctx, "GET", url)
    return response.get("value", [])


def create_role_assignment_request(
    cli_ctx, role_definition_id, resource_id, user_id, reason, duration_hours
):
    """Create a role assignment request to activate a PIM group."""
    # Convert duration (in hours) to ISO 8601 duration format (e.g., PT720M)
    duration_minutes = int(duration_hours * 60)
    iso_duration = f"PT{duration_minutes}M"

    # Prepare the activation request
    request_body = {
        "roleDefinitionId": role_definition_id,
        "resourceId": resource_id,
        "subjectId": user_id,
        "assignmentState": "Active",
        "type": "UserAdd",
        "reason": reason,
        "schedule": {
            "type": "Once",
            "startDateTime": None,
            "endDateTime": None,
            "duration": iso_duration,
        },
    }

    url = f"{PIM_API_BASE_URL}/roleAssignmentRequests"

    response = pim_api_request(cli_ctx, "POST", url, request_body)
    return response


def format_datetime(dt_str):
    """Format datetime string for display."""
    if not dt_str:
        return "Never expires"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%H:%M, %b %d")
    except:
        return dt_str


def calculate_time_remaining(dt_str):
    """Calculate time remaining until expiration."""
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        remaining = dt - datetime.now(timezone.utc)

        if remaining.total_seconds() < 0:
            return "Expired"

        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        return f"{hours}h {minutes}m"
    except:
        return "N/A"
