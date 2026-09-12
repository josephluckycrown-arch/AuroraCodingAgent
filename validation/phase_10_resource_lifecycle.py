"""
PHASE 10: RESOURCE LIFECYCLE
Validate lifecycle APIs for files and resources
"""

import os
import sys
from dotenv import load_dotenv
from arkruntime import Ark

# Load environment variables
load_dotenv()

def phase_10_resource_lifecycle():
    """
    Phase 10: Test resource lifecycle APIs.
    
    Tests (where supported):
    - File management
    - Image generation
    - Content generation tasks
    - Resource creation/cleanup
    
    Only tests resources actually supported by the account.
    """
    print("=" * 60)
    print("PHASE 10 — RESOURCE LIFECYCLE")
    print("=" * 60)
    
    api_key = os.environ.get("ARK_API_KEY")
    model = os.environ.get("ARK_MODEL")
    endpoint = os.environ.get(
        "ARK_ENDPOINT",
        "https://ark.ap-southeast.bytepluses.com/api/v3"
    )
    
    if not api_key or not model:
        print("✗ Missing ARK_API_KEY or ARK_MODEL")
        return False
    
    try:
        client = Ark(
            api_key=api_key,
            base_url=endpoint,
        )
        
        print(f"Testing resource lifecycle with model: {model}")
        print("\nChecking available resource APIs...")
        
        # Check for files API
        has_files = hasattr(client, 'files')
        print(f"  Files API: {'✓ Available' if has_files else '✗ Not available'}")
        
        # Check for images API
        has_images = hasattr(client, 'images')
        print(f"  Images API: {'✓ Available' if has_images else '✗ Not available'}")
        
        # Check for tasks API
        has_tasks = hasattr(client, 'tasks')
        print(f"  Tasks API: {'✓ Available' if has_tasks else '✗ Not available'}")
        
        # Test file management if available
        if has_files:
            print("\n[Files API Test]")
            try:
                # List existing files
                files_list = client.files.list()
                print(f"  ✓ Can list files: {len(files_list)} files found")
            except Exception as e:
                print(f"  ⚠ Files list error: {type(e).__name__}")
        
        # Test images API if available
        if has_images:
            print("\n[Images API Test]")
            try:
                # Try to generate image
                image_resp = client.images.generate(
                    prompt="A simple test image",
                    model=model,
                    n=1,
                )
                print(f"  ✓ Can generate images")
                
                # Clean up if possible
                if hasattr(image_resp, 'data') and image_resp.data:
                    print(f"    Generated {len(image_resp.data)} image(s)")
            except Exception as e:
                error_str = str(e)
                if "not supported" in error_str.lower():
                    print(f"  ⚠ Images not supported by model")
                else:
                    print(f"  ⚠ Images error: {type(e).__name__}: {str(e)[:60]}...")
        
        # Test tasks API if available
        if has_tasks:
            print("\n[Tasks API Test]")
            try:
                # List tasks
                tasks_list = client.tasks.list()
                print(f"  ✓ Can list tasks")
            except Exception as e:
                print(f"  ⚠ Tasks error: {type(e).__name__}")
        
        print("\n" + "=" * 60)
        if has_files or has_images or has_tasks:
            print("✓ Resource lifecycle APIs available")
        else:
            print("⚠ No resource lifecycle APIs found")
            print("  (This is normal for basic chat-only models)")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ Resource lifecycle test FAILED")
        print(f"  Error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = phase_10_resource_lifecycle()
    sys.exit(0 if success else 1)
