import subprocess  # nosec B404
import json
import os
import sys

def run_security_scan():
    print("🚀 Initializing SecureSphere SAST Scan...")
    
    # Define the command to run Bandit and output JSON
    # We exclude venv to keep the report clean
    cmd = [
        "bandit", 
        "-r", ".", 
        "--exclude", "./venv", 
        "-f", "json"
    ]
    
    try:
        # Run bandit and capture the output. We use nosec B603 because 
        # the command list is internally controlled and trusted.
        result = subprocess.run(cmd, capture_output=True, text=True) # nosec B603
        
        # Bandit returns non-zero exit codes if it finds issues, 
        # so we parse the stdout regardless of the return code.
        scan_results = json.loads(result.stdout)
        
        issues = scan_results.get("results", [])
        # Extract total counts from the metrics summary
        summary = scan_results.get("metrics", {}).get("_totals", {})
        
        # Calculate counts specifically for the 'Security Gate'
        high_issues = sum(1 for i in issues if i.get('issue_severity') == 'HIGH')
        medium_issues = sum(1 for i in issues if i.get('issue_severity') == 'MEDIUM')
        low_issues = sum(1 for i in issues if i.get('issue_severity') == 'LOW')

        print(f"✅ Scan Complete. Total issues: {len(issues)}")
        print(f"📊 Severity Breakdown: High: {high_issues}, Medium: {medium_issues}, Low: {low_issues}")
        
        # Save the full audit for logging purposes
        with open("security_audit.json", "w") as f:
            json.dump(issues, f, indent=4)
            
        # SECURITY GATE LOGIC:
        # We fail the build (exit 1) if High or Medium vulnerabilities are found.
        if high_issues > 0 or medium_issues > 0:
            print(f"🛑 Security Gate Failed: Found {high_issues} High and {medium_issues} Medium issues.")
            sys.exit(1)
        
        print("🟢 Security Gate Passed: No High or Medium vulnerabilities detected.")
        sys.exit(0)

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse Bandit output. Check if Bandit is installed correctly.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Automation Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_security_scan()