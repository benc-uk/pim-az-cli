# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def create_pim(cmd, resource_group_name, pim_name, location=None, tags=None):
    raise CLIError('TODO: Implement `pim create`')


def list_pim(cmd, resource_group_name=None):
    raise CLIError('TODO: Implement `pim list`')


def update_pim(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance