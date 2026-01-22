import os
import requests
import argparse
import sys
import json

def get_scan_scorecard():
    """
    Reads the Bandit results and returns a formatted string with severity counts.
    """
    try:
        with open("security_audit.json", "r") as f:
            issues = json.load(f)
        
        # Calculate counts for each severity level
        high = sum(1 for i in issues if i.get('issue_severity') == 'HIGH')
        medium = sum(1 for i in issues if i.get('issue_severity') == 'MEDIUM')
        low = sum(1 for i in issues if i.get('issue_severity') == 'LOW')

        if not issues:
            return "🛡️ Security Status: 100% Clean. No issues identified."

        return (
            f"🛡️ Security Scorecard:\n"
            f"🔴 High: {high}\n"
            f"🟡 Medium: {medium}\n"
            f"🟢 Low: {low}"
        )
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback if the scan file is missing or corrupted
        return "🛡️ Security Status: Scan completed (details in logs)."

def send_post(base_message, commit_url=None):
    # Retrieve secrets from Environment Variables
    access_token = os.environ.get('LINKEDIN_TOKEN') #nosec
    user_urn = os.environ.get('LINKEDIN_URN') #nosec

    if not access_token or not user_urn:
        print("❌ Error: Missing LINKEDIN_TOKEN or LINKEDIN_URN environment variables.")
        sys.exit(1)

    # Generate the scorecard data
    scorecard = get_scan_scorecard()

    # Build the full message with the URL included
    full_message = (
        f"{base_message}\n\n"
        f"{scorecard}\n\n"
        f"🛠️ Tech Stack: Python | Bandit SAST | GitHub Actions"
    )

    if commit_url:
        full_message += f"\n🔗 View Change: {commit_url}"

    full_message += f"\n\n#DevSecOps #SecureSphere #CyberSecurity #BuildInPublic"

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
                    "text": full_message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=post_data, timeout=10)
        response.raise_for_status()
        print(f"✅ Success! Post live: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        # Safeguard: printing response.text only if it exists
        if hasattr(e, 'response') and e.response is not None:
             print(f"Details: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SecureSphere Automated LinkedIn Poster")
    parser.add_argument("--message", required=True, help="The content of the LinkedIn post")
    parser.add_argument("--commit-url", help="Link to the specific GitHub commit") # Added this
    
    args = parser.parse_args()
    send_post(args.message, args.commit_url)