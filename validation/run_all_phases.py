"""
Run All Validation Phases
Complete validation script for all 15 phases
"""

import subprocess
import sys
from pathlib import Path

phases = [
    ("2", "phase_2_sdk_validation.py", "SDK Installation Validation"),
    ("3", "phase_3_configure_client.py", "Client Configuration"),
    ("4", "phase_4_chat_completions.py", "Chat Completions Test"),
    ("5", "phase_5_vision.py", "Vision/Multimodal Test"),
    ("6", "phase_6_streaming.py", "Streaming Test"),
    ("7", "phase_7_responses_api.py", "Responses API Test"),
    ("8", "phase_8_function_calling.py", "Function Calling Test"),
    ("9", "phase_9_error_handling.py", "Error Handling Test"),
    ("10", "phase_10_resource_lifecycle.py", "Resource Lifecycle Test"),
    ("11", "phase_11_readiness.py", "Coding-Agent Readiness"),
    ("12", "phase_12_migration.py", "Legacy SDK Migration"),
    ("13", "phase_13_pin_version.py", "Version Pinning"),
]

def run_validation():
    """Run all validation phases."""
    print("=" * 70)
    print("AURORA MODELARK SDK VALIDATION")
    print("Running all 12 execution phases (1 & 14-15 are framework)")
    print("=" * 70)
    print()
    
    validation_dir = Path(__file__).parent
    results = {}
    
    for phase_num, script, description in phases:
        script_path = validation_dir / script
        
        if not script_path.exists():
            print(f"⚠ Phase {phase_num}: {description}")
            print(f"  Script not found: {script_path}")
            results[phase_num] = "MISSING"
            continue
        
        print(f"{'=' * 70}")
        print(f"PHASE {phase_num}: {description}")
        print(f"{'=' * 70}")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=validation_dir.parent,
                timeout=300,  # 5 minute timeout per phase
                capture_output=False,
            )
            
            if result.returncode == 0:
                print(f"\n✓ Phase {phase_num} PASSED\n")
                results[phase_num] = "PASSED"
            else:
                print(f"\n✗ Phase {phase_num} FAILED\n")
                results[phase_num] = "FAILED"
        
        except subprocess.TimeoutExpired:
            print(f"\n✗ Phase {phase_num} TIMEOUT\n")
            results[phase_num] = "TIMEOUT"
        
        except Exception as e:
            print(f"\n✗ Phase {phase_num} ERROR: {e}\n")
            results[phase_num] = "ERROR"
    
    # Print summary
    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print()
    
    passed = sum(1 for r in results.values() if r == "PASSED")
    failed = sum(1 for r in results.values() if r == "FAILED")
    errors = sum(1 for r in results.values() if r in ["TIMEOUT", "ERROR", "MISSING"])
    
    for phase_num, script, description in phases:
        status = results.get(phase_num, "UNKNOWN")
        symbol = "✓" if status == "PASSED" else "✗"
        print(f"{symbol} Phase {phase_num:2}: {description:40} [{status}]")
    
    print()
    print(f"Results: {passed} passed, {failed} failed, {errors} errors")
    print()
    
    if failed == 0 and errors == 0:
        print("=" * 70)
        print("✓ ALL PHASES PASSED")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("1. Review VALIDATION_REPORT.md")
        print("2. Check Phase 13 output for exact arkruntime version")
        print("3. Update requirements.txt with pinned version")
        print("4. Implement Aurora core using provider abstraction")
        print("5. Test with ModelArk provider")
        print("6. Plan for future provider support")
        print()
        return True
    else:
        print("=" * 70)
        print("✗ SOME PHASES FAILED")
        print("=" * 70)
        print()
        print("Review failed phases:")
        for phase_num, status in results.items():
            if status != "PASSED":
                print(f"  - Phase {phase_num}: {status}")
        print()
        print("Troubleshooting:")
        print("1. Check .env configuration")
        print("2. Verify ARK_API_KEY and ARK_MODEL are correct")
        print("3. Run individual phase scripts for detailed output")
        print("4. See VALIDATION_GUIDE.md for troubleshooting")
        print()
        return False

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
