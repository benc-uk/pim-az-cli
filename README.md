# PIM Azure CLI Extension

An Azure CLI extension for managing Privileged Identity Management (PIM) group activations in Microsoft Entra ID.

This greatly simplifies the process of activating and managing your PIM-eligible groups directly from the command line, without needing to use the Azure Portal and carry out manual steps.

This extension provides a convenient way to list, activate, and manage your PIM-eligible groups directly from the Azure CLI, without needing to navigate the Azure Portal.

## Features

- 🔍 **List eligible groups** - View all PIM groups you can activate
- ✅ **View active activations** - See currently active group memberships with expiration times
- ⏳ **Check pending requests** - Monitor activation requests awaiting approval
- 🚀 **Request activation** - Submit activation requests with custom duration and justification
- 📊 **Combined status view** - See both active and pending activations together

## Installation

Install the extension from the published wheel file:

```bash
az extension add --source https://github.com/benc-uk/pim-az-cli/releases/download/0.0.1/pim-0.0.1-py3-none-any.whl
```

## Quick Start

### Prerequisites

- Azure CLI installed (`az` command available)
- Active Microsoft Entra ID account with PIM-eligible groups
- Authenticated with Azure CLI (`az login`)

### Basic Usage

```bash
# List all eligible PIM groups
az pim list

# View active activations
az pim active

# Request activation for a group
az pim request -n "My-PIM-Group" -r "Incident response"

# Check status (active + pending)
az pim status
```

## Available Commands

| Command          | Description                                       |
| ---------------- | ------------------------------------------------- |
| `az pim list`    | List all eligible PIM groups for the current user |
| `az pim active`  | List all active PIM group activations             |
| `az pim pending` | List pending activation requests                  |
| `az pim status`  | Combined view of active and pending activations   |
| `az pim request` | Request activation for a PIM group                |

## Examples

### List Eligible Groups

```bash
az pim list --output table
```

### Request Activation

```bash
# Default: 12 hours as Member
az pim request -n "Production-Access" -r "Deploy hotfix"

# Custom duration: 8 hours as Owner
az pim request -n "Admin-Group" -r "Emergency maintenance" --role Owner -d 8

# Short activation: 30 minutes
az pim request -n "ReadOnly-Access" -r "Quick check" -d 0.5
```

### View Active Activations

```bash
az pim active --output table
```

### Check Status

```bash
az pim status --output table
```

### Query Specific Information

You can use JMESPath queries to filter and format output. For example:

```bash
# Get just group names and expiration times
az pim active --query "[].{Group:groupName, Expires:expires}" --output table

# Find PIM groups containing "Readers"
az pim list --query "[?contains(groupName, 'Readers')]" --output table
```

## Command Reference

### `az pim request`

Request activation for an eligible PIM group.

**Required Parameters:**

- `--name, -n` - Name of the PIM group to activate
- `--reason, -r` - Justification for the activation request

**Optional Parameters:**

- `--duration, -d` - Duration in hours (default: 12). Supports decimals (e.g., 0.5 for 30 minutes)
- `--role` - Role to activate: "Member" or "Owner" (default: Member)

## Authentication

The extension uses your existing Azure CLI authentication. No additional configuration required.

Simply ensure you're logged in:

```bash
az login
```

The extension accesses:

- **Azure RBAC PIM API** (`api.azrbac.mspim.azure.com`) - for PIM operations
- **Microsoft Graph API** - for user information only

## Development

### Project Structure

```
├── src/pim/                   # Extension source code
│   ├── azext_pim/             # Main extension package
│   │   ├── custom.py          # Command implementations
│   │   ├── pim.py             # PIM API client
│   │   ├── _help.py           # Command help text
│   │   ├── _params.py         # Command parameters
│   │   └── commands.py        # Command registration
│   ├── setup.py               # Package setup
│   ├── README.rst             # Extension documentation
│   └── HISTORY.rst            # Release history
└── makefile                   # Build automation
```

### Building & Working Locally

You need to create Python virtual environment and install dependencies:

```bash
make venv
```

Then, add the extension to your local Azure CLI installation with the `azdev` tool:

```bash
azdev extension repo add .
azdev extension add pim
```

Building the extension wheel file can be done with:

```bash
make build
```

## Background

This extension is a Python port of the original [pim-cli-go](https://github.com/benc-uk/pim-cli) tool, given that the tool already required the Azure CLI for authentication, a native integration made sense.

### Why This Extension?

- **Native Azure CLI integration** - Works seamlessly with existing `az` commands
- **Consistent authentication** - Uses your existing `az login` credentials
- **Standard output formats** - Supports `--output table`, `--output json`, `--query`, etc.
- **No additional tools** - No need to install separate CLI tools

### Differences from pim-cli-go

- Uses Azure CLI's output formatting instead of custom table rendering
- Leverages Azure CLI authentication framework
- Follows Azure CLI extension conventions and patterns
- Integrated help system (`az pim --help`)

## Troubleshooting

### No eligible groups found

- Ensure you're logged in: `az login`
- Verify you have PIM-eligible groups in your Microsoft Entra ID tenant
- Check with your Microsoft Entra ID administrator about PIM access

### Activation request fails

- Verify the group name matches exactly (case-sensitive)
- Ensure you're eligible for the specified role (Member or Owner)
- Check that the group isn't already active
- Verify duration doesn't exceed your organization's maximum allowed duration

## Documentation

- [Detailed README](src/pim/README.rst) - Complete extension documentation
- [Release History](src/pim/HISTORY.rst) - Version history and changelog
- [Azure PIM Documentation](https://docs.microsoft.com/azure/active-directory/privileged-identity-management/)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Links

- **Repository**: https://github.com/benc-uk/pim-az-cli
- **Original Go Version**: https://github.com/benc-uk/pim-cli
- **Azure CLI Extensions**: https://docs.microsoft.com/cli/azure/azure-cli-extensions-overview

---

**Note**: This extension manages PIM group activations only. For Azure role activations, please use the Azure Portal or other Microsoft-provided tools.
