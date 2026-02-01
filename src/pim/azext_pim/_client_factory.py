# --------------------------------------------------------------------------------------------
# Copyright (c) Ben Coleman, 2026. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------


def _graph_client_factory(cli_ctx, **_):
    """Create a Microsoft Graph client."""
    from azure.cli.command_modules.role._msgrpah import GraphClient

    return GraphClient(cli_ctx)
