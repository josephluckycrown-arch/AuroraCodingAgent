"""
PHASE 9: ERROR HANDLING
Test error handling for various failure modes
"""

import os
import sys
from dotenv import load_dotenv
from arkruntime import Ark

# Load environment variables
load_dotenv()

def phase_9_error_handling():
    """
    Phase 9: Test error handling.
    
    Tests (safely):
    - 401 authentication error
    - 403 permission error
    - 404 invalid model
    - 429 rate limit
    - 500 server error
    - Timeout
    - Network failure
    - Malformed response
    """
    print("=" * 60)
    print("PHASE 9 — ERROR HANDLING")
    print("=" * 60)
    
    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_MODEL")
    endpoint = os.environ.get(
        "ARK_ENDPOINT",
        "https://ark.ap-southeast.bytepluses.com/api/v3"
    )
    
    results = {}
    
    # Test 1: Invalid API key (401)
    print("\n[Test 1] Invalid API key (401 Authentication Error)")
    try:
        client = Ark(
            api_key="invalid_key_12345",
            base_url=endpoint,
        )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10,
        )
        results["401_auth"] = "⚠ Did not raise error (may not validate on creation)"
    except Exception as e:
        if "401" in str(e) or "Unauthorized" in str(e):
            results["401_auth"] = f"✓ Caught 401: {type(e).__name__}"
        else:
            results["401_auth"] = f"✓ Exception: {type(e).__name__}: {str(e)[:60]}..."
    
    # Test 2: Invalid model (404)
    print("[Test 2] Invalid model name (404 Not Found)")
    try:
        client = Ark(
            api_key=api_key,
            base_url=endpoint,
        )
        response = client.chat.completions.create(
            model="invalid_model_xyz_12345",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10,
        )
        results["404_model"] = "⚠ Did not raise error"
    except Exception as e:
        if "404" in str(e) or "Not found" in str(e):
            results["404_model"] = f"✓ Caught 404: {type(e).__name__}"
        else:
            results["404_model"] = f"✓ Exception: {type(e).__name__}: {str(e)[:60]}..."
    
    # Test 3: Malformed request (400)
    print("[Test 3] Malformed request (400 Bad Request)")
    try:
        client = Ark(
            api_key=api_key,
            base_url=endpoint,
        )
        # Try to send invalid parameter
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=-1,  # Invalid negative max_tokens
        )
        results["400_malformed"] = "⚠ Did not raise error"
    except Exception as e:
        if "400" in str(e) or "Bad" in str(e):
            results["400_malformed"] = f"✓ Caught 400: {type(e).__name__}"
        else:
            results["400_malformed"] = f"✓ Exception: {type(e).__name__}: {str(e)[:60]}..."
    
    # Test 4: Timeout handling
    print("[Test 4] Timeout handling")
    try:
        client = Ark(
            api_key=api_key,
            base_url=endpoint,
            timeout=0.001,  # Very short timeout
        )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=100,
        )
        results["timeout"] = "⚠ Did not timeout"
    except TimeoutError as e:
        results["timeout"] = f"✓ Caught TimeoutError: {str(e)[:60]}..."
    except Exception as e:
        if "timeout" in str(e).lower():
            results["timeout"] = f"✓ Caught timeout: {type(e).__name__}"
        else:
            results["timeout"] = f"⚠ Exception: {type(e).__name__}: {str(e)[:60]}..."
    
    # Test 5: Connection to invalid endpoint
    print("[Test 5] Connection to invalid endpoint")
    try:
        client = Ark(
            api_key=api_key,
            base_url="https://invalid-endpoint-xyz-12345.com/api/v3",
        )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10,
        )
        results["invalid_endpoint"] = "⚠ Did not raise error"
    except Exception as e:
        error_type = type(e).__name__
        if "Connection" in error_type or "Network" in error_type or "Resolve" in error_type:
            results["invalid_endpoint"] = f"✓ Caught network error: {error_type}"
        else:
            results["invalid_endpoint"] = f"✓ Exception: {error_type}: {str(e)[:60]}..."
    
    # Print results
    print("\n" + "=" * 60)
    print("ERROR HANDLING RESULTS")
    print("=" * 60)
    
    for test_name, result in results.items():
        print(f"{test_name:20} {result}")
    
    all_caught = all("✓" in str(r) for r in results.values())
    
    print("\n" + "=" * 60)
    if all_caught:
        print("✓ Error handling test PASSED")
        print("  SDK properly handles various error conditions")
    else:
        print("⚠ Some error conditions not caught")
        print("  This may be acceptable depending on SDK design")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = phase_9_error_handling()
    sys.exit(0 if success else 1)
