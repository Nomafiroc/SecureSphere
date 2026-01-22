import subprocess   #nosec
import json
import os

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
        # Run bandit and capture the output
        result = subprocess.run(cmd, capture_output=True, text=True) #this will give a warning of low severity but it can be ignored as we are using a list for the command
        
        # Bandit returns non-zero exit codes if it finds issues, 
        # so we parse the stdout regardless of the return code.
        scan_results = json.loads(result.stdout)
        
        issues = scan_results.get("results", [])
        summary = scan_results.get("metrics", {}).get("_totals", {})
        
        print(f"✅ Scan Complete. Found {len(issues)} issues.")
        print(f"📊 Summary: {summary}")
        
        # Filter for only High and Medium issues for your 'Critical Report'
       # critical_issues = [i for i in issues if i['issue_severity'] in ['HIGH', 'MEDIUM']]
        
        # Save a clean version for your Notion logs
        with open("security_audit.json", "w") as f:
            json.dump(issues, f, indent=4)      #change to critical_issues to save only critical issues
            
        return issues      #change to critical_issues to save only critical issues

    except Exception as e:
        print(f"❌ Automation Error: {e}")
        return []

if __name__ == "__main__":
    run_security_scan()