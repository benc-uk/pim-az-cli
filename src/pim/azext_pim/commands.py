# --------------------------------------------------------------------------------------------
# Copyright (c) Ben Coleman, 2026. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------


def load_command_table(self, _):
    with self.command_group("pim") as g:
        g.custom_command(
            "list",
            "list_pim",
            table_transformer="[].{GroupName:groupName, Roles:roles}",
        )
        g.custom_command(
            "active",
            "active_pim",
            table_transformer="[].{GroupName:groupName, Role:role, MemberType:memberType, Expires:expires, TimeRemaining:timeRemaining, Status:status}",
        )
        g.custom_command(
            "pending",
            "pending_pim",
            table_transformer="[].{GroupName:groupName, Role:role, RequestedAt:requestedAt, Status:status}",
        )
        g.custom_command(
            "status",
            "status_pim",
            table_transformer="[].{GroupName:groupName, Role:role, Type:type, Expires:expires, TimeRemaining:timeRemaining, RequestedAt:requestedAt, Status:status}",
        )
        g.custom_command(
            "request",
            "request_pim",
            table_transformer="{GroupName:groupName, Role:role, Status:status, Reason:reason, Duration:duration}",
        )

    with self.command_group("pim", is_preview=True):
        pass
