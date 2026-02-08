# Rehydrate System

Automated context loader with PowerShell/Bash scripts to restore operational state and verify system integrity.

## Overview

The Rehydrate System is designed to automate the process of restoring an operational state for various systems. It leverages both PowerShell and Bash scripting to provide cross-platform compatibility and robust system integrity verification.

**NEW**: Version 2.0 introduces the **Global Rehydration System** - a unified, cross-platform coordinator that provides a single interface for all rehydration operations with state management and history tracking.

## Features

- **Global Rehydration Coordinator**: Unified Python-based interface that works across all platforms
- **Automated Context Loading**: Automatically loads necessary configurations and data to bring a system back to an operational state
- **Cross-Platform Scripting**: Utilizes PowerShell for Windows environments and Bash for Linux/Unix-like environments
- **Global State Management**: Tracks rehydration state across all environments with persistent storage
- **Rehydration History**: Complete audit trail of all rehydration operations
- **System Integrity Verification**: Includes checks to ensure the system is in a healthy and consistent state after rehydration
- **Automatic Platform Detection**: Automatically detects and uses the appropriate platform-specific scripts
- **Integration with Orchestrator System**: Designed to work seamlessly with the Orchestrator System for coordinated deployments and recovery

## Structure

```
rehydrate-system/
├── README.md
├── manifest.json
├── global_rehydrate.py          # Global rehydration coordinator
├── global_config.json           # Global configuration
├── global_state.json            # Global state (auto-generated)
├── scripts/
│   ├── powershell/
│   │   └── restore_state.ps1
│   └── bash/
│       └── restore_state.sh
└── docs/
    └── architecture.md
```

## Getting Started

### Prerequisites

- Python 3.6+ (for global rehydration coordinator)
- PowerShell (for Windows)
- Bash (for Linux/Unix)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/InfinityXOneSystems/rehydrate-system.git
   cd rehydrate-system
   ```

2. Make the global rehydration script executable (Linux/Unix):
   ```bash
   chmod +x global_rehydrate.py
   ```

3. (Optional) Configure global settings by editing `global_config.json`.

### Usage

#### Global Rehydration System (Recommended)

The global rehydration coordinator provides a unified interface that works on all platforms:

**Perform rehydration:**
```bash
python3 global_rehydrate.py rehydrate --environment=production --verify
```

**Check system status:**
```bash
python3 global_rehydrate.py status
```

**View rehydration history:**
```bash
python3 global_rehydrate.py history --limit=10
```

**Force rehydration:**
```bash
python3 global_rehydrate.py rehydrate --environment=staging --force
```

**Reset global state:**
```bash
python3 global_rehydrate.py reset --confirm
```

#### Direct Platform-Specific Scripts (Legacy)

You can still use the platform-specific scripts directly:

**Windows (PowerShell):**

```powershell
./scripts/powershell/restore_state.ps1 -Environment Production -VerifyIntegrity
```

**Linux/Unix (Bash):**

```bash
./scripts/bash/restore_state.sh --environment=staging --verify
```

## Integration with Orchestrator System

The Rehydrate System exposes a manifest file (`manifest.json`) that the Orchestrator System can consume to understand available rehydration routines and their parameters. The Orchestrator System can then invoke the appropriate scripts based on the desired operational state and target environment.

### Global Rehydration Integration

The global rehydration coordinator can be integrated into the Orchestrator System using the following approaches:

1. **Direct Python Integration**: Import and use the `GlobalRehydrationSystem` class directly
2. **CLI Integration**: Execute the `global_rehydrate.py` script via subprocess calls
3. **State Monitoring**: Read `global_state.json` to monitor rehydration status
4. **History Tracking**: Access rehydration history for audit and compliance purposes

## Configuration

The global rehydration system can be configured via `global_config.json`:

- `default_environment`: Default environment for rehydration operations
- `verify_integrity_by_default`: Whether to verify integrity by default
- `log_level`: Logging verbosity level
- `max_retry_attempts`: Maximum retry attempts for failed operations
- `timeout_seconds`: Operation timeout in seconds
- `environment_aliases`: Aliases for environment names

## Global State Management

The system maintains a `global_state.json` file that tracks:

- Current system status (uninitialized, hydrated, etc.)
- Active environments that have been rehydrated
- Timestamp of last rehydration
- Complete history of all rehydration operations

This state file enables:
- Prevention of duplicate rehydration operations
- Audit trails for compliance
- Recovery from failures
- Status monitoring by external systems

## Examples

For detailed usage examples, see [docs/usage-examples.md](docs/usage-examples.md).

## Contributing

Contributions are welcome! Please refer to the `CONTRIBUTING.md` (to be created) for guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` (to be created) file for details.
