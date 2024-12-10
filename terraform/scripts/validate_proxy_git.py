import argparse
import os
import subprocess

# Function to execute the PowerShell command
def execute_powershell_command(gcp_access_token, gcp_project_id, proxy_bundle_path):
    # Get the path to the scripts directory inside the GitHub repository
    script_dir = os.path.join(os.path.dirname(__file__))
    
    # Paths for the scripts and the zip file
    script_path = os.path.join(script_dir, "validate.ps1")
    
    # Ensure the PowerShell script exists before proceeding
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"The PowerShell script 'validate.ps1' was not found at {script_path}")

    # PowerShell command to run
    powershell_command = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",  # Set execution policy to bypass for the script execution
        "-File", script_path,
        "-Token", gcp_access_token,
        "-ApigeeBaseUrl", f"https://apigee.googleapis.com/v1/organizations/{gcp_project_id}",
        "-ProxyBundlePath", proxy_bundle_path
    ]
    
    # Execute the command and check for errors
    try:
        subprocess.run(powershell_command, check=True, capture_output=True, text=True)
        print("PowerShell script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing PowerShell script: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise  # Reraise the error to stop further execution in case of failure

# Main function to handle command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--gcp_access_token', required=True, help="GCP access token for authentication")
    parser.add_argument('--gcp_project_id', required=True, help="GCP project ID for Apigee environment")
    parser.add_argument('--proxy_bundle_path', required=True, help="Path to the proxy bundle to validate")
    
    args = parser.parse_args()
    
    # Validate the proxy bundle
    execute_powershell_command(
        args.gcp_access_token,
        args.gcp_project_id,
        args.proxy_bundle_path
    )
