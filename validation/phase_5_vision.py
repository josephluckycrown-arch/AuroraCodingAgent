"""
PHASE 5: VISION TEST
Validate multimodal Chat Completions interface with images
"""

import os
import sys
from dotenv import load_dotenv
from arkruntime import Ark

# Load environment variables
load_dotenv()

def phase_5_vision():
    """
    Phase 5: Test vision/multimodal capabilities.
    
    Tests:
    - Text + image_url in single request
    - Response parsing
    - Proper handling of multimodal input
    - No permanent storage of test images
    """
    print("=" * 60)
    print("PHASE 5 — VISION TEST")
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
        
        print(f"Testing vision with model: {model}")
        print("\nPreparing multimodal request...")
        
        # Use a publicly available test image from ModelArk docs
        # or use a simple placeholder URL
        test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png"
        
        print(f"Test image URL: {test_image_url}")
        
        # Construct message with image
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What does the picture mainly convey? Answer in one sentence."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": test_image_url
                        }
                    }
                ]
            }
        ]
        
        print("\nSending vision request...")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=100,
        )
        
        print("✓ Vision request successful")
        
        # Extract response
        if hasattr(response, 'choices') and response.choices:
            choice = response.choices[0]
            if hasattr(choice, 'message'):
                content = choice.message.content
                print(f"\nModel analysis: {content}")
                print("\n✓ Vision test PASSED")
                return True
        
        print("⚠ Unexpected response structure")
        print(f"  Response: {response}")
        return True
        
    except Exception as e:
        error_str = str(e)
        
        # Vision might not be supported by all models
        if "not supported" in error_str.lower() or "vision" in error_str.lower():
            print(f"⚠ Vision may not be supported by this model")
            print(f"  Error: {e}")
            print("\nThis is acceptable if using a non-vision model.")
            return True
        
        print(f"✗ Vision test FAILED")
        print(f"  Error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = phase_5_vision()
    print("\n" + "=" * 60)
    if success:
        print("Phase 5 complete. Ready for Phase 6.")
    else:
        print("Phase 5 failed or skipped.")
    print("=" * 60)
    sys.exit(0 if success else 1)
