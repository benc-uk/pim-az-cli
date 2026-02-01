# --------------------------------------------------------------------------------------------
# Copyright (c) Ben Coleman, 2026. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

from collections import OrderedDict
from knack.util import CLIError
from azext_pim import pim


def list_pim(cmd):
    """List all eligible PIM groups for the current user."""
    user_id = pim.get_user_id(cmd.cli_ctx)
    assignments = pim.get_role_assignments(cmd.cli_ctx, user_id, "Eligible")

    if not assignments:
        from knack.log import get_logger

        logger = get_logger(__name__)
        logger.warning("No eligible PIM groups found")
        return []

    # Group by resource name
    groups = {}
    for assignment in assignments:
        group_name = assignment["resource"]["displayName"]
        if group_name not in groups:
            groups[group_name] = {"groupName": group_name, "roles": []}
        groups[group_name]["roles"].append(
            OrderedDict(
                [
                    ("role", assignment["roleDefinition"]["displayName"]),
                    ("memberType", assignment.get("memberType", "Unknown")),
                ]
            )
        )

    return list(groups.values())


def active_pim(cmd):
    """List all active PIM group activations for the current user."""
    user_id = pim.get_user_id(cmd.cli_ctx)
    assignments = pim.get_role_assignments(cmd.cli_ctx, user_id, "Active")

    if not assignments:
        from knack.log import get_logger

        logger = get_logger(__name__)
        logger.warning("No active groups found")
        return []

    results = []
    for assignment in assignments:
        end_datetime = assignment.get("endDateTime")
        status = assignment.get("status", "Unknown")
        if isinstance(status, dict):
            status = status.get("status", "Unknown")

        results.append(
            OrderedDict(
                [
                    ("groupName", assignment["resource"]["displayName"]),
                    ("role", assignment["roleDefinition"]["displayName"]),
                    ("memberType", assignment.get("memberType", "Unknown")),
                    ("expires", pim.format_datetime(end_datetime)),
                    ("timeRemaining", pim.calculate_time_remaining(end_datetime)),
                    ("status", status),
                ]
            )
        )

    return results


def pending_pim(cmd):
    """List all pending PIM group activation requests for the current user."""
    user_id = pim.get_user_id(cmd.cli_ctx)
    assignments = pim.get_role_assignment_requests(
        cmd.cli_ctx, user_id, "PendingApproval"
    )

    if not assignments:
        from knack.log import get_logger

        logger = get_logger(__name__)
        logger.warning("No pending requests found")
        return []

    results = []
    for assignment in assignments:
        status_info = assignment.get("status", {})
        if isinstance(status_info, dict):
            status = f"{status_info.get('status', '')} {status_info.get('subStatus', '')}".strip()
        else:
            status = str(status_info)

        requested_at = assignment.get("requestedDateTime")

        results.append(
            OrderedDict(
                [
                    ("groupName", assignment["resource"]["displayName"]),
                    ("role", assignment["roleDefinition"]["displayName"]),
                    ("requestedAt", pim.format_datetime(requested_at)),
                    ("status", status),
                ]
            )
        )

    return results


def status_pim(cmd):
    """List both active and pending PIM group activations for the current user."""
    active_groups = active_pim(cmd)
    pending_requests = pending_pim(cmd)

    # Flatten the output for better table display
    results = []

    # Add active groups with a type indicator
    for active in active_groups:
        result = OrderedDict(
            [
                ("groupName", active["groupName"]),
                ("role", active["role"]),
                ("type", "Active"),
                ("expires", active.get("expires")),
                ("timeRemaining", active.get("timeRemaining")),
                ("status", active.get("status")),
            ]
        )
        results.append(result)

    # Add pending requests with a type indicator
    for pending in pending_requests:
        result = OrderedDict(
            [
                ("groupName", pending["groupName"]),
                ("role", pending["role"]),
                ("type", "Pending"),
                ("requestedAt", pending.get("requestedAt")),
                ("status", pending.get("status")),
            ]
        )
        results.append(result)

    return results


def request_pim(cmd, name, reason, duration=12, role="Member"):
    """Request activation for a PIM group with the specified role."""
    user_id = pim.get_user_id(cmd.cli_ctx)

    # Validate inputs
    if not name:
        raise CLIError("Group name must be specified")
    if not reason:
        raise CLIError("Reason must be specified")
    if duration <= 0:
        raise CLIError("Duration must be greater than zero")

    # Find the eligible role assignment for the specified group
    assignments = pim.get_role_assignments(cmd.cli_ctx, user_id, "Eligible")

    target_assignment = None
    for assignment in assignments:
        if (
            assignment["resource"]["displayName"] == name
            and assignment["roleDefinition"]["displayName"].lower() == role.lower()
        ):
            target_assignment = assignment
            break

    if not target_assignment:
        raise CLIError(f"No eligible group found: {name} with role: {role}")

    try:
        response = pim.create_role_assignment_request(
            cmd.cli_ctx,
            target_assignment["roleDefinition"]["id"],
            target_assignment["resourceId"],
            user_id,
            reason,
            duration,
        )

        status_info = response.get("status", {})
        if isinstance(status_info, dict):
            status = status_info.get("status", "Unknown")
        else:
            status = str(status_info)

        return OrderedDict(
            [
                ("groupName", name),
                ("role", role),
                ("status", status),
                ("reason", reason),
                ("duration", f"{duration} hours"),
            ]
        )
    except CLIError as e:
        # Check if it's already active (HTTP 400 typically means already active)
        if "already" in str(e).lower() or "active" in str(e).lower():
            from knack.log import get_logger

            logger = get_logger(__name__)
            logger.warning(str(e))
            return OrderedDict(
                [
                    ("groupName", name),
                    ("role", role),
                    ("status", str(e)),
                    ("reason", reason),
                    ("duration", f"{duration} hours"),
                ]
            )
        raise
