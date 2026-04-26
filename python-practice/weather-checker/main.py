"""Weather Checker — demonstrating project setup."""
import requests

def check_setup():
    """Verify that all dependencies are properly installed."""
    print("=== Project Setup Verification ===")
    print(f"requests version: {requests.__version__}")
    
    # Make a simple HTTP request to verify requests works
    try:
        response = requests.get("https://httpbin.org/get", timeout=5)
        print(f"HTTP test: Status {response.status_code} (success!)")
    except requests.exceptions.RequestException as e:
        print(f"HTTP test failed: {e}")
    
    print("\nSetup is complete. You're ready to build!")

if __name__ == "__main__":
    check_setup()
