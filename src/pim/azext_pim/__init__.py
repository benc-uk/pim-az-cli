# --------------------------------------------------------------------------------------------
# Copyright (c) Ben Coleman, 2026. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader


class PimCommandsLoader(AzCommandsLoader):
    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType

        pim_custom = CliCommandType(operations_tmpl="azext_pim.custom#{}")
        super(PimCommandsLoader, self).__init__(
            cli_ctx=cli_ctx, custom_command_type=pim_custom
        )

    def load_command_table(self, args):
        from azext_pim.commands import load_command_table

        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_pim._params import load_arguments

        load_arguments(self, command)


COMMAND_LOADER_CLS = PimCommandsLoader
