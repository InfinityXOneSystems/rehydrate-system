# Global Rehydration System - Usage Examples

This document provides practical examples of using the Global Rehydration System.

## Basic Usage

### 1. Check System Status

Before performing any rehydration, check the current system status:

```bash
python3 global_rehydrate.py status
```

**Expected Output:**
```
=== Global Rehydration Status ===
System Status: uninitialized
Active Environments: None
Last Rehydration: Never
Total Rehydrations: 0
===================================
```

### 2. Perform First Rehydration

Rehydrate the development environment with integrity verification:

```bash
python3 global_rehydrate.py rehydrate --environment=development --verify
```

**Expected Output:**
```
=== Global Rehydration System ===
Environment: development
Verify Integrity: True
Platform: linux
===================================

Executing: bash /path/to/restore_state.sh --environment=development --verify
✓ Global rehydration completed successfully!
```

### 3. Check Status After Rehydration

```bash
python3 global_rehydrate.py status
```

**Expected Output:**
```
=== Global Rehydration Status ===
System Status: hydrated
Active Environments: development
Last Rehydration: 2026-02-08T09:28:03.056893+00:00
Total Rehydrations: 1
===================================
```

## Advanced Usage

### 4. Rehydrate Multiple Environments

```bash
# Rehydrate staging
python3 global_rehydrate.py rehydrate --environment=staging --verify

# Rehydrate production
python3 global_rehydrate.py rehydrate --environment=production --verify

# Check status
python3 global_rehydrate.py status
```

**Expected Output:**
```
=== Global Rehydration Status ===
System Status: hydrated
Active Environments: development, staging, production
Last Rehydration: 2026-02-08T09:30:15.123456+00:00
Total Rehydrations: 3
===================================
```

### 5. Prevent Duplicate Rehydration

Attempting to rehydrate an already-hydrated environment will be prevented:

```bash
python3 global_rehydrate.py rehydrate --environment=production
```

**Expected Output:**
```
Warning: Environment 'production' is already hydrated.
Use --force to rehydrate anyway.
```

### 6. Force Rehydration

To force rehydration of an already-hydrated environment:

```bash
python3 global_rehydrate.py rehydrate --environment=production --force
```

### 7. Rehydrate Without Integrity Verification

Skip integrity verification for faster execution:

```bash
python3 global_rehydrate.py rehydrate --environment=development --no-verify
```

### 8. View Rehydration History

View the last 10 rehydration operations:

```bash
python3 global_rehydrate.py history
```

**Expected Output:**
```
=== Rehydration History (last 10) ===

1. 2026-02-08T09:27:56.049280+00:00
   Environment: production
   Platform: linux
   Status: success

2. 2026-02-08T09:28:18.433243+00:00
   Environment: production
   Platform: linux
   Status: success

3. 2026-02-08T09:28:28.289074+00:00
   Environment: staging
   Platform: linux
   Status: success
===================================
```

### 9. View Limited History

View only the last 3 operations:

```bash
python3 global_rehydrate.py history --limit=3
```

### 10. Reset Global State

To reset all global state (requires confirmation):

```bash
python3 global_rehydrate.py reset --confirm
```

**Warning:** This will clear all rehydration history and active environment tracking.

## Integration Examples

### Python Integration

```python
#!/usr/bin/env python3
from global_rehydrate import GlobalRehydrationSystem

# Initialize the system
grs = GlobalRehydrationSystem()

# Perform rehydration
result = grs.rehydrate(
    environment="production",
    verify_integrity=True,
    force=False
)

if result["success"]:
    print("✓ Rehydration successful")
    print(f"Details: {result['details']}")
else:
    print("✗ Rehydration failed")
    print(f"Error: {result['message']}")

# Check status
status = grs.get_status()
print(f"System Status: {status['system_status']}")
print(f"Active Environments: {status['active_environments']}")

# View history
history = grs.get_history(limit=5)
for record in history:
    print(f"- {record['timestamp']}: {record['environment']} [{record['status']}]")
```

### Bash Script Integration

```bash
#!/bin/bash

# Rehydrate and capture exit code
python3 global_rehydrate.py rehydrate --environment=production --verify
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Rehydration successful, proceeding with deployment..."
    # Continue with deployment steps
else
    echo "Rehydration failed, aborting deployment."
    exit 1
fi
```

### CI/CD Pipeline Integration

```yaml
# Example GitHub Actions workflow
name: Deploy with Rehydration

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      
      - name: Check Rehydration Status
        run: python3 global_rehydrate.py status
      
      - name: Rehydrate Environment
        run: |
          python3 global_rehydrate.py rehydrate \
            --environment=production \
            --verify \
            --force
      
      - name: View Rehydration History
        if: always()
        run: python3 global_rehydrate.py history --limit=5
```

## Configuration Examples

### Custom Configuration

Edit `global_config.json` to customize behavior:

```json
{
  "default_environment": "staging",
  "verify_integrity_by_default": true,
  "log_level": "DEBUG",
  "max_retry_attempts": 5,
  "timeout_seconds": 600,
  "environment_aliases": {
    "prod": "production",
    "dev": "development",
    "stage": "staging",
    "qa": "quality-assurance"
  }
}
```

### State Monitoring

Monitor state programmatically:

```python
import json
import time

def monitor_rehydration_status():
    """Monitor rehydration status in real-time."""
    with open('global_state.json', 'r') as f:
        state = json.load(f)
    
    print(f"Status: {state['system_status']}")
    print(f"Active: {', '.join(state['active_environments'])}")
    
    # Check if any recent failures
    recent = state.get('rehydration_history', [])[-5:]
    failures = [r for r in recent if r['status'] == 'failed']
    
    if failures:
        print(f"⚠ Warning: {len(failures)} recent failures detected")
        for failure in failures:
            print(f"  - {failure['timestamp']}: {failure['environment']}")

# Run monitoring
while True:
    monitor_rehydration_status()
    time.sleep(60)  # Check every minute
```

## Troubleshooting

### Issue: Permission Denied

**Error:** `Permission denied: './global_rehydrate.py'`

**Solution:**
```bash
chmod +x global_rehydrate.py
```

### Issue: Script Not Found

**Error:** `Script not found: /path/to/restore_state.sh`

**Solution:** Ensure you're running from the rehydrate-system directory:
```bash
cd /path/to/rehydrate-system
python3 global_rehydrate.py rehydrate --environment=dev
```

### Issue: State File Corruption

**Solution:** Reset and reinitialize:
```bash
python3 global_rehydrate.py reset --confirm
python3 global_rehydrate.py status
```

## Best Practices

1. **Always verify integrity in production:**
   ```bash
   python3 global_rehydrate.py rehydrate --environment=production --verify
   ```

2. **Monitor history regularly:**
   ```bash
   python3 global_rehydrate.py history --limit=20
   ```

3. **Use environment aliases** in `global_config.json` for convenience

4. **Integrate status checks** into deployment pipelines

5. **Back up state file** before major operations:
   ```bash
   cp global_state.json global_state.json.backup
   ```

6. **Review logs** after each rehydration to ensure success

7. **Test in non-production** environments first before production rehydration
