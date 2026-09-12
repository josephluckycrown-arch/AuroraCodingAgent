"""
PHASE 13: PIN VERSION
Lock arkruntime version after validation
"""

import subprocess
import sys

def get_installed_version(package_name):
    """Get the installed version of a package."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                return line.split(':', 1)[1].strip()
    except Exception:
        pass
    return None

def phase_13_pin_version():
    """
    Phase 13: Pin exact arkruntime version after validation.
    
    Records:
    - Python version
    - arkruntime exact version
    - OS/runtime
    - Model ID
    - ModelArk endpoint
    """
    print("=" * 60)
    print("PHASE 13 — PIN VERSION")
    print("=" * 60)
    
    # Get Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"\nPython version: {python_version}")
    
    # Get arkruntime version
    arkruntime_version = get_installed_version('arkruntime')
    if arkruntime_version:
        print(f"arkruntime version: {arkruntime_version}")
    else:
        print("⚠ arkruntime not currently installed")
        print("  Run: python -m pip install --upgrade arkruntime")
        return False
    
    # Other info
    import platform
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Platform: {platform.platform()}")
    
    # Environment info
    import os
    model = os.environ.get("ARK_MODEL", "not set")
    endpoint = os.environ.get(
        "ARK_ENDPOINT",
        "https://ark.ap-southeast.bytepluses.com/api/v3"
    )
    
    print(f"Model ID: {model}")
    print(f"Endpoint: {endpoint}")
    
    # Generate requirements entry
    print("\n" + "=" * 60)
    print("REQUIREMENTS.TXT ENTRY")
    print("=" * 60)
    pinned_entry = f"arkruntime=={arkruntime_version}"
    print(f"\nPinned: {pinned_entry}")
    
    print("\n[RECOMMENDATION]")
    print(f"""
Update requirements.txt:

FROM:
  arkruntime>=0.5.0

TO:
  arkruntime=={arkruntime_version}

This ensures reproducible builds and consistent behavior.

After validation passes, commit this exact version.
Do not use >= or < ranges unless testing new versions.
""")
    
    print("\n" + "=" * 60)
    print("VALIDATION METADATA")
    print("=" * 60)
    
    metadata = f"""
Python: {python_version}
arkruntime: {arkruntime_version}
OS: {platform.system()}
Model: {model}
Endpoint: {endpoint}

This metadata should be recorded in VALIDATION_REPORT.md
"""
    print(metadata)
    
    return True

if __name__ == "__main__":
    success = phase_13_pin_version()
    print("\n" + "=" * 60)
    if success:
        print("Phase 13 complete. Ready for Phase 14.")
    else:
        print("Phase 13 failed - install arkruntime first.")
    print("=" * 60)
    sys.exit(0 if success else 1)
