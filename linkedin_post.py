import os
import requests
import argparse
import sys

# Best Practice: Use a main function for professional scripts
def send_post(message):
    # Retrieve secrets from Environment Variables (Security)
    access_token = os.environ.get('LINKEDIN_TOKEN')
    user_urn = os.environ.get('LINKEDIN_URN')

    if not access_token or not user_urn:
        print("❌ Error: Missing LINKEDIN_TOKEN or LINKEDIN_URN environment variables.")
        sys.exit(1)

    url = "https://api.linkedin.com/v2/ugcPosts"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202512" 
    }
    
    post_data = {
        "author": user_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    # Error Handling: Use try-except for network issues
    try:
        response = requests.post(url, headers=headers, json=post_data)
        response.raise_for_status() # Automatically triggers error for 4xx/5xx codes
        print(f"✅ Success! Post live: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if response.text:
            print(f"Details: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    # Setup CLI Arguments
    parser = argparse.ArgumentParser(description="SecureSphere Automated LinkedIn Poster")
    parser.add_argument("--message", required=True, help="The content of the LinkedIn post")
    
    args = parser.parse_args()
    send_post(args.message)