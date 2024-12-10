import argparse
import os
import subprocess

# Function to execute the PowerShell command
def execute_powershell_command(gcp_access_token, gcp_project_id, proxy_bundle_path):
    # Paths for the scripts and the zip file
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "validate.ps1")
    
    # PowerShell command to run
    powershell_command = [
        "powershell.exe",
        "-Command",
        f"Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\" -Token \"{gcp_access_token}\" -ApigeeBaseUrl \"https://apigee.googleapis.com/v1/organizations/{gcp_project_id}\" -ProxyBundlePath \"{proxy_bundle_path}\"' -NoNewWindow -Wait"
    ]
    
    # Execute the command
    subprocess.run(powershell_command, check=True)

# Main function to handle command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--gcp_access_token', required=True)
    parser.add_argument('--gcp_project_id', required=True)
    parser.add_argument('--proxy_bundle_path', required=True)
    
    args = parser.parse_args()
    
    # Validate the proxy bundle
    execute_powershell_command(
        args.gcp_access_token,
        args.gcp_project_id,
        args.proxy_bundle_path
    )
