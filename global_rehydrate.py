#!/usr/bin/env python3
"""
Global Rehydration System

A cross-platform global rehydration coordinator that manages system state restoration
across multiple environments and platforms. This module provides a unified interface
for rehydration operations regardless of the underlying platform.
"""

import json
import os
import subprocess
import sys
import platform
import argparse
from datetime import datetime, timezone
from pathlib import Path


class GlobalRehydrationSystem:
    """
    Main coordinator for global rehydration operations.
    
    This class manages the rehydration process across different platforms,
    maintains global state, and provides a unified interface for all rehydration operations.
    """
    
    def __init__(self, config_path=None):
        """Initialize the global rehydration system."""
        self.base_path = Path(__file__).parent
        self.config_path = config_path or self.base_path / "global_config.json"
        self.state_path = self.base_path / "global_state.json"
        self.manifest_path = self.base_path / "manifest.json"
        
        self.config = self._load_config()
        self.state = self._load_state()
        self.manifest = self._load_manifest()
        
    def _load_config(self):
        """Load global configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "default_environment": "development",
            "verify_integrity_by_default": True,
            "log_level": "INFO",
            "max_retry_attempts": 3,
            "timeout_seconds": 300
        }
    
    def _load_state(self):
        """Load global state."""
        if self.state_path.exists():
            with open(self.state_path, 'r') as f:
                return json.load(f)
        return {
            "last_rehydration": None,
            "rehydration_history": [],
            "active_environments": [],
            "system_status": "uninitialized"
        }
    
    def _load_manifest(self):
        """Load system manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_state(self):
        """Save global state to disk."""
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _save_config(self):
        """Save global configuration to disk."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _detect_platform(self):
        """Detect the current platform."""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system in ["linux", "darwin"]:
            return "linux"
        else:
            return "linux"  # Default to linux for unknown platforms
    
    def _get_script_for_platform(self, platform_name):
        """Get the appropriate script for the given platform."""
        for script in self.manifest.get("scripts", []):
            if script["platform"] == platform_name:
                return script
        return None
    
    def _execute_platform_script(self, script_info, environment, verify_integrity):
        """Execute the platform-specific rehydration script."""
        script_path = self.base_path / script_info["path"]
        
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        # Build command based on platform
        if script_info["platform"] == "windows":
            cmd = [
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-File", str(script_path),
                "-Environment", environment
            ]
            if verify_integrity:
                cmd.append("-VerifyIntegrity")
        else:  # linux/unix
            cmd = [
                "bash",
                str(script_path),
                f"--environment={environment}"
            ]
            if verify_integrity:
                cmd.append("--verify")
        
        # Execute script
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    def rehydrate(self, environment=None, verify_integrity=None, force=False):
        """
        Perform global rehydration.
        
        Args:
            environment: Target environment (defaults to config default)
            verify_integrity: Whether to verify system integrity (defaults to config default)
            force: Force rehydration even if already hydrated
        
        Returns:
            dict: Rehydration result with success status and details
        """
        # Use defaults from config if not specified
        if environment is None:
            environment = self.config.get("default_environment", "development")
        if verify_integrity is None:
            verify_integrity = self.config.get("verify_integrity_by_default", True)
        
        print(f"\n=== Global Rehydration System ===")
        print(f"Environment: {environment}")
        print(f"Verify Integrity: {verify_integrity}")
        print(f"Platform: {self._detect_platform()}")
        print("=" * 35 + "\n")
        
        # Check if already hydrated
        if not force and self.state.get("system_status") == "hydrated":
            if environment in self.state.get("active_environments", []):
                print(f"Warning: Environment '{environment}' is already hydrated.")
                print("Use --force to rehydrate anyway.")
                return {
                    "success": True,
                    "message": "Already hydrated",
                    "skipped": True
                }
        
        # Detect platform and get appropriate script
        current_platform = self._detect_platform()
        script_info = self._get_script_for_platform(current_platform)
        
        if not script_info:
            raise ValueError(f"No script found for platform: {current_platform}")
        
        # Record rehydration start
        rehydration_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": environment,
            "platform": current_platform,
            "verify_integrity": verify_integrity,
            "status": "in_progress"
        }
        
        try:
            # Execute platform-specific script
            result = self._execute_platform_script(script_info, environment, verify_integrity)
            
            # Update rehydration record
            rehydration_record["status"] = "success" if result["success"] else "failed"
            rehydration_record["returncode"] = result["returncode"]
            rehydration_record["output"] = result["stdout"]
            
            if result["success"]:
                # Update global state
                self.state["last_rehydration"] = datetime.now(timezone.utc).isoformat()
                self.state["system_status"] = "hydrated"
                
                if environment not in self.state.get("active_environments", []):
                    self.state.setdefault("active_environments", []).append(environment)
                
                print("\n✓ Global rehydration completed successfully!")
            else:
                print(f"\n✗ Global rehydration failed!")
                print(f"Error: {result['stderr']}")
            
            # Save rehydration record to history
            self.state.setdefault("rehydration_history", []).append(rehydration_record)
            self._save_state()
            
            return {
                "success": result["success"],
                "message": "Rehydration completed" if result["success"] else "Rehydration failed",
                "details": rehydration_record
            }
            
        except Exception as e:
            rehydration_record["status"] = "error"
            rehydration_record["error"] = str(e)
            self.state.setdefault("rehydration_history", []).append(rehydration_record)
            self._save_state()
            
            print(f"\n✗ Error during rehydration: {e}")
            return {
                "success": False,
                "message": f"Error: {e}",
                "details": rehydration_record
            }
    
    def get_status(self):
        """Get current global rehydration status."""
        return {
            "system_status": self.state.get("system_status", "uninitialized"),
            "active_environments": self.state.get("active_environments", []),
            "last_rehydration": self.state.get("last_rehydration"),
            "total_rehydrations": len(self.state.get("rehydration_history", []))
        }
    
    def get_history(self, limit=10):
        """Get rehydration history."""
        history = self.state.get("rehydration_history", [])
        return history[-limit:] if limit else history
    
    def reset(self):
        """Reset global state."""
        self.state = {
            "last_rehydration": None,
            "rehydration_history": [],
            "active_environments": [],
            "system_status": "uninitialized"
        }
        self._save_state()
        print("Global state reset successfully.")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Global Rehydration System - Unified cross-platform rehydration coordinator"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Rehydrate command
    rehydrate_parser = subparsers.add_parser("rehydrate", help="Perform global rehydration")
    rehydrate_parser.add_argument(
        "--environment", "-e",
        help="Target environment (e.g., production, staging, development)"
    )
    rehydrate_parser.add_argument(
        "--verify", "-v",
        action="store_true",
        help="Verify system integrity after rehydration"
    )
    rehydrate_parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip system integrity verification"
    )
    rehydrate_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force rehydration even if already hydrated"
    )
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get current system status")
    
    # History command
    history_parser = subparsers.add_parser("history", help="View rehydration history")
    history_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="Number of history entries to display (default: 10)"
    )
    
    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset global state")
    reset_parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirm reset operation"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize global rehydration system
    grs = GlobalRehydrationSystem()
    
    # Execute command
    if args.command == "rehydrate":
        verify_integrity = None
        if args.verify:
            verify_integrity = True
        elif args.no_verify:
            verify_integrity = False
        
        result = grs.rehydrate(
            environment=args.environment,
            verify_integrity=verify_integrity,
            force=args.force
        )
        
        return 0 if result["success"] else 1
        
    elif args.command == "status":
        status = grs.get_status()
        print("\n=== Global Rehydration Status ===")
        print(f"System Status: {status['system_status']}")
        print(f"Active Environments: {', '.join(status['active_environments']) or 'None'}")
        print(f"Last Rehydration: {status['last_rehydration'] or 'Never'}")
        print(f"Total Rehydrations: {status['total_rehydrations']}")
        print("=" * 35 + "\n")
        return 0
        
    elif args.command == "history":
        history = grs.get_history(limit=args.limit)
        print(f"\n=== Rehydration History (last {args.limit}) ===")
        
        if not history:
            print("No rehydration history available.")
        else:
            for i, record in enumerate(history, 1):
                print(f"\n{i}. {record['timestamp']}")
                print(f"   Environment: {record['environment']}")
                print(f"   Platform: {record['platform']}")
                print(f"   Status: {record['status']}")
                if record.get('error'):
                    print(f"   Error: {record['error']}")
        
        print("=" * 35 + "\n")
        return 0
        
    elif args.command == "reset":
        if not args.confirm:
            print("Warning: This will reset all global state.")
            print("Use --confirm to proceed with reset.")
            return 1
        
        grs.reset()
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
