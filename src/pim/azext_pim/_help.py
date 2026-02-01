# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Ben Coleman, 2026. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import

helps["pim"] = """
    type: group
    short-summary: Manage Privileged Identity Management (PIM) group activations.
    long-summary: |
        Commands to manage access to Privileged Identity Management (PIM) groups in Microsoft Entra ID.
        Allows users to list eligible groups, view active and pending activations, and request group activation.
"""

helps["pim list"] = """
    type: command
    short-summary: List all eligible PIM groups for the current user.
    long-summary: |
        List all PIM groups that the current user is eligible to activate, along with their roles.
    examples:
        - name: List all eligible PIM groups
          text: az pim list
"""

helps["pim active"] = """
    type: command
    short-summary: List all active PIM group activations for the current user.
    long-summary: |
        Display all currently active PIM group role activations, including expiration times and time remaining.
    examples:
        - name: List active PIM group activations
          text: az pim active
"""

helps["pim pending"] = """
    type: command
    short-summary: List all pending PIM group activation requests.
    long-summary: |
        Display all pending PIM group activation requests that are awaiting approval.
    examples:
        - name: List pending activation requests
          text: az pim pending
"""

helps["pim status"] = """
    type: command
    short-summary: List both active and pending PIM group activations.
    long-summary: |
        Display a combined view of all active PIM group activations and pending activation requests.
    examples:
        - name: Show current PIM status
          text: az pim status
"""

helps["pim request"] = """
    type: command
    short-summary: Request activation for a PIM group with a specified role.
    long-summary: |
        Submit an activation request for an eligible PIM group. Requires specifying the group name,
        a reason for activation, and optionally the duration and role type.
    examples:
        - name: Request activation for a PIM group as Member for 8 hours
          text: az pim request --name "My-PIM-Group" --reason "Incident response" --duration 8
        - name: Request activation as Owner with default 12-hour duration
          text: az pim request -n "My-PIM-Group" -r "Admin tasks" --role Owner
        - name: Request activation for 30 minutes
          text: az pim request -n "My-PIM-Group" -r "Quick check" -d 0.5
"""
