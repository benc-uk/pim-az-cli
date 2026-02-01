Microsoft Azure CLI 'pim' Extension
==========================================

An Azure CLI extension for managing Privileged Identity Management (PIM) group activations in Microsoft Entra ID.

This extension provides commands to list, activate, and manage your PIM-eligible groups directly from the Azure CLI.

Installation
------------

Install the extension directly from the built wheel package:

.. code-block:: bash

    az extension add --source https://github.com/benc-uk/pim-az-cli/releases/download/0.0.1/pim-0.0.1-py3-none-any.whl



Features
--------

* **List eligible groups** - View all PIM groups you can activate
* **View active activations** - See currently active group memberships with expiration times
* **Check pending requests** - Monitor activation requests awaiting approval
* **Request activation** - Submit activation requests with custom duration and justification
* **Combined status view** - See both active and pending activations together

Commands
--------

az pim list
~~~~~~~~~~~

List all PIM groups that you're eligible to activate.

.. code-block:: bash

    az pim list

Output shows group names with their available roles and member types.

az pim active
~~~~~~~~~~~~~

Display all currently active PIM group role activations.

.. code-block:: bash

    az pim active

Shows group names, roles, expiration times, time remaining, and activation status.

az pim pending
~~~~~~~~~~~~~~

List pending activation requests awaiting approval.

.. code-block:: bash

    az pim pending

Displays group names, roles, request times, and current status.

az pim status
~~~~~~~~~~~~~

Combined view of both active and pending activations.

.. code-block:: bash

    az pim status

Shows all active groups and pending requests in a single output.

az pim request
~~~~~~~~~~~~~~

Request activation for an eligible PIM group.

.. code-block:: bash

    az pim request --name <group-name> --reason <justification> [--duration <hours>] [--role <Member|Owner>]

Parameters:
    * ``--name, -n`` (required): Name of the PIM group to activate
    * ``--reason, -r`` (required): Justification for the activation request
    * ``--duration, -d`` (optional): Duration in hours (default: 12). Supports decimals (e.g., 0.5 for 30 minutes)
    * ``--role`` (optional): Role to activate - "Member" or "Owner" (default: Member)

Examples
--------

List all eligible PIM groups:

.. code-block:: bash

    az pim list

View active activations:

.. code-block:: bash

    az pim active

Check pending requests:

.. code-block:: bash

    az pim pending

Request activation as Member for 12 hours (default):

.. code-block:: bash

    az pim request -n "My-PIM-Group" -r "Incident response"

Request activation as Owner for 8 hours:

.. code-block:: bash

    az pim request -n "My-PIM-Group" -r "Admin tasks" --role Owner -d 8

Request activation for 30 minutes:

.. code-block:: bash

    az pim request -n "My-PIM-Group" -r "Quick check" -d 0.5

Using with Azure CLI output formatting:

.. code-block:: bash

    # Table format
    az pim list --output table
    az pim active --output table
    
    # JSON format
    az pim status --output json
    
    # Query specific fields
    az pim active --query "[].{Group:groupName, Expires:expires}"

Authentication
--------------

The extension uses your existing Azure CLI authentication (``az login``). 

It accesses:
    * **Azure RBAC PIM API** (``api.azrbac.mspim.azure.com``) - for PIM operations
    * **Microsoft Graph API** - for user information only

No additional permissions or configuration are required beyond standard Azure CLI login.

Implementation Notes
--------------------

* This extension is a Python port of the Go-based `pim-cli-go <https://github.com/benc-uk/pim-cli>`_
* Uses the Azure RBAC PIM API instead of Microsoft Graph for PIM operations
* Works with standard Azure credentials obtained via ``az login``
* Supports all output formats provided by Azure CLI (JSON, table, YAML, TSV, etc.)

Troubleshooting
---------------

If you don't see any groups:
    * Ensure you're logged in: ``az login``
    * Verify you have PIM-eligible groups in your Microsoft Entra ID tenant
    * Check with your Microsoft Entra ID administrator about PIM access

If activation fails:
    * Verify the group name matches exactly (case-sensitive)
    * Ensure you're eligible for the specified role (Member or Owner)
    * Check that the group isn't already active
    * Verify the duration doesn't exceed maximum allowed by your organization's policies

License
-------

MIT License. See LICENSE file for details.

Links
-----

* Source code: https://github.com/benc-uk/pim-az-cli
* Original Go version: https://github.com/benc-uk/pim-cli
* Azure PIM documentation: https://docs.microsoft.com/azure/active-directory/privileged-identity-management/