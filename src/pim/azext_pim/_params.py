# --------------------------------------------------------------------------------------------
# Copyright (c) Ben Coleman, 2026. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------


def load_arguments(self, _):
    with self.argument_context("pim list") as c:
        pass

    with self.argument_context("pim active") as c:
        pass

    with self.argument_context("pim pending") as c:
        pass

    with self.argument_context("pim status") as c:
        pass

    with self.argument_context("pim request") as c:
        c.argument(
            "name",
            options_list=["--name", "-n"],
            help="Name of the PIM group to request activation for",
            required=True,
        )
        c.argument(
            "reason",
            options_list=["--reason", "-r"],
            help="Reason for requesting activation",
            required=True,
        )
        c.argument(
            "duration",
            options_list=["--duration", "-d"],
            type=float,
            help="Duration for the activation in hours (e.g., 0.5, 1, 2, 12)",
            default=12,
        )
        c.argument(
            "role",
            options_list=["--role"],
            help='Role name to activate (e.g., "Member", "Owner")',
            default="Member",
        )
