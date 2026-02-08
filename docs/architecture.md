# Rehydrate System Architecture

## 1. Introduction

The Rehydrate System is a crucial component of the control-plane, responsible for restoring a system's operational state from a known baseline. It provides a standardized and automated way to load context, apply configurations, and verify system integrity. 

**Version 2.0** introduces the **Global Rehydration System** - a unified, cross-platform coordinator that provides centralized state management, history tracking, and a single interface for all rehydration operations across any platform.

This document outlines the architecture of both the platform-specific scripts and the new global rehydration coordinator.

## 2. Core Components

The system is composed of the following key components:

### 2.1 Global Rehydration Coordinator

**NEW in v2.0** - The `global_rehydrate.py` module provides:

- **Unified Interface**: Single CLI/API for all rehydration operations across platforms
- **State Management**: Persistent tracking of rehydration state in `global_state.json`
- **Configuration Management**: Centralized configuration via `global_config.json`
- **Platform Detection**: Automatic detection and selection of appropriate platform scripts
- **History Tracking**: Complete audit trail of all rehydration operations
- **Status Monitoring**: Real-time status queries for external systems

### 2.2 Platform-Specific Scripts

- **PowerShell Scripts** (`scripts/powershell/`): Windows-specific rehydration logic
- **Bash Scripts** (`scripts/bash/`): Linux/Unix rehydration logic

These scripts perform the actual platform-specific rehydration tasks and are invoked by the global coordinator.

### 2.3 Manifest

**Manifest (`manifest.json`)**: A JSON file that describes the rehydration capabilities of the system. It serves as a service contract for the Orchestrator System, detailing:
- Available platform-specific scripts and their parameters
- Global rehydration coordinator capabilities
- Integration points for external systems

### 2.4 State and Configuration Files

- **`global_state.json`**: Auto-generated file tracking system status, active environments, and rehydration history
- **`global_config.json`**: User-configurable settings for global rehydration behavior

## 3. Workflow

### 3.1 Global Rehydration Workflow (NEW - Recommended)

The global rehydration process follows this workflow:

1. **User/System Request**: A user or external system requests rehydration via the global coordinator CLI or API

2. **State Check**: The coordinator checks `global_state.json` to determine if the environment is already hydrated

3. **Configuration Loading**: Loads settings from `global_config.json` for default values and preferences

4. **Platform Detection**: Automatically detects the current platform (Windows/Linux/Darwin)

5. **Script Selection**: Reads `manifest.json` to identify the appropriate platform-specific script

6. **Pre-execution Validation**: Verifies script existence and required parameters

7. **Script Execution**: Invokes the platform-specific script with appropriate parameters

8. **State Tracking**: Records rehydration attempt with timestamp, environment, and status

9. **Result Processing**: Captures output, determines success/failure, and updates global state

10. **History Recording**: Appends operation to rehydration history in `global_state.json`

11. **Response**: Returns result to caller with success status and details

### 3.2 Legacy Platform-Specific Workflow

The original rehydration process (still supported) follows this workflow:

1. **Trigger**: The Orchestrator System, based on its own logic or a user request, decides to rehydrate a target system.

2. **Manifest Discovery**: The orchestrator fetches and parses the `manifest.json` of the Rehydrate System to identify the appropriate script and required parameters for the target platform and environment.

3. **Script Execution**: The orchestrator invokes the designated script (e.g., `restore_state.ps1` or `restore_state.sh`) with the necessary parameters.

4. **Context Loading**: The script begins by loading the required context. This could involve fetching configuration files, environment variables, or data from a secure store.

5. **State Restoration**: The script proceeds to restore the operational state. This may include tasks like:
    - Restarting services
    - Applying database migrations
    - Seeding caches
    - Restoring file systems from snapshots

6. **Integrity Verification (Optional)**: If requested, the script performs a series of checks to verify that the system is in a healthy and consistent state. This could involve:
    - Pinging critical services
    - Running health checks
    - Validating data consistency

7. **Completion**: The script reports the success or failure of the rehydration process back to the Orchestrator System.

## 4. Cross-Platform Strategy

To ensure broad compatibility, the Rehydrate System employs a dual-scripting strategy:

- **PowerShell**: For Windows-based environments, leveraging its deep integration with the Windows ecosystem.
- **Bash**: For Linux and Unix-like environments, providing a powerful and ubiquitous scripting solution.

This approach allows the same high-level rehydration logic to be applied across different operating systems, with platform-specific implementation details handled by the respective scripts.

## 5. Extensibility

The Rehydrate System is designed to be extensible. New rehydration routines can be added by:

1. Creating a new script (PowerShell or Bash) with the desired logic.
2. Adding a corresponding entry to the `manifest.json` file to expose the new script and its parameters to the Orchestrator System.

This modular design allows the Rehydrate System to evolve and adapt to new systems and recovery scenarios over time.

## 6. Global State Management

The global rehydration coordinator maintains persistent state in `global_state.json`:

### State Schema

```json
{
  "last_rehydration": "ISO8601 timestamp",
  "system_status": "uninitialized|hydrated|error",
  "active_environments": ["env1", "env2"],
  "rehydration_history": [
    {
      "timestamp": "ISO8601 timestamp",
      "environment": "production",
      "platform": "linux",
      "verify_integrity": true,
      "status": "success|failed|error",
      "returncode": 0,
      "output": "script output"
    }
  ]
}
```

### State Benefits

- **Idempotency**: Prevents redundant rehydration operations
- **Audit Trail**: Complete history for compliance and debugging
- **Status Monitoring**: External systems can query current state
- **Recovery**: Failed operations can be identified and retried
- **Coordination**: Multiple systems can coordinate via shared state

## 7. Integration Patterns

### 7.1 Python Integration

```python
from global_rehydrate import GlobalRehydrationSystem

grs = GlobalRehydrationSystem()
result = grs.rehydrate(environment="production", verify_integrity=True)
if result["success"]:
    print("Rehydration successful")
```

### 7.2 CLI Integration

```bash
python3 global_rehydrate.py rehydrate --environment=production --verify
```

### 7.3 State Monitoring

```python
import json

with open('global_state.json', 'r') as f:
    state = json.load(f)
    
if state['system_status'] == 'hydrated':
    print(f"System is hydrated for: {state['active_environments']}")
```
