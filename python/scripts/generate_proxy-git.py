import sys
import os
import string
from zipfile import ZipFile
import argparse
import json

# Get the current script's directory (the root of the repository)
repo_directory = os.path.dirname(os.path.abspath(__file__))  

# Define the path for the templates and proxy bundle directories
source_tmpl_directory = os.path.join(repo_directory, '..', 'templates', 'bundle', 'apiproxy')  
proxy_bundle_directory = os.path.join(repo_directory, '..', 'proxies_export')  
apiproxy_directory = os.path.join(proxy_bundle_directory, 'apiproxy')  
policies_tmpl_directory = os.path.join(repo_directory, '..', 'templates', 'policies')  

sys.path.append(os.path.join(repo_directory, '..', 'scripts'))  

from config import variables

# Function to generate the policies template
def generate_policies_template(policies_list, xml_indent=4):
    return "\n".join([f"<Policy>{policy}</Policy>" for policy in policies_list]).rjust(xml_indent)

# Function to generate the proxies template
def generate_proxies_template(policies_list, xml_indent=4):
    return "\n".join([f"<Step>\n  <Name>{policy}</Name>\n</Step>" for policy in policies_list]).rjust(xml_indent)

# Function to render templates (similar to templatefile in Terraform)
def render_template(template_path, **kwargs):
    with open(template_path, 'r') as f:
        template = f.read()
    return string.Template(template).substitute(kwargs)

def parse_variable_mappings(variable_string):
    """Parses a variable mapping string into a dictionary of {var_name: json_path}."""
    mappings = {}
    
    if not variable_string.strip():
        return mappings  # Return empty dict if no data provided
    
    pairs = variable_string.split('/')  # Split by '/'
    
    for pair in pairs:
        if '=' in pair:
            var_name, json_path = pair.split('=', 1)  # Split on first '='
            var_name = var_name.strip()
            json_path = json_path.strip()

            # Ensure JSON path starts with "$."
            if not json_path.startswith("$."):
                json_path = f"$.{json_path}"

            mappings[var_name] = json_path

    return mappings

# Function to dynamically modify policy files
def modify_policy_file(policy_name, variables_json, policy_type):
    policy_path = os.path.join(policies_tmpl_directory, f"{policy_name}.xml")

    if not os.path.exists(policy_path):
        print(f"Warning: Policy file {policy_path} not found! Skipping modification.")
        return

    with open(policy_path, 'r') as f:
        policy_content = f.read()

    try:
        variables_dict = json.loads(variables_json)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format for {policy_name}. Skipping modification.")
        return

    variable_entries = "\n".join([
        f'        <Variable name="{var_name}">\n            <JSONPath>{json_path}</JSONPath>\n        </Variable>'
        for var_name, json_path in variables_dict.items()
    ])

    modified_policy_content = policy_content.replace(
        '<JSONPayload>',
        f'<JSONPayload>\n{variable_entries}'
    )

    modified_policy_content = modified_policy_content.replace(
        '<Source clearPayload="false">request</Source>',
        f'<Source clearPayload="false">{policy_type}</Source>'
    )

    with open(policy_path, 'w') as f:
        f.write(modified_policy_content)

    print(f"? Successfully updated {policy_name} with user-defined variables.")

# Function to generate the proxy bundle
def generate_proxy_bundle(proxy_category, proxy_name, proxy_base_path, target_server_name, gcp_project_id, gcp_access_token, request_variables_string, response_variables_string):
    categories = variables["categories"]  
    policies_list = categories.get(proxy_category, [])

        # ✅ Parse request and response variable mappings
    request_variables_dict = parse_variable_mappings(request_variables_string)
    response_variables_dict = parse_variable_mappings(response_variables_string)

    # ✅ Convert to JSON format for modifying policies
    request_variables_json = json.dumps(request_variables_dict, indent=2)
    response_variables_json = json.dumps(response_variables_dict, indent=2)
    
    # ? Modify specific policy files dynamically
    modify_policy_file("EV-setconsentRequestLogs", request_variables_json, "request")
    modify_policy_file("EV-setResponseErrorCodeLogs", response_variables_json, "response")

# Generate policies and proxies templates
    policies_tmpl = generate_policies_template(policies_list)
    proxies_tmpl = generate_proxies_template(policies_list)

    print("✅ Extracted Request Variables JSON:")
    print(request_variables_json)

    print("✅ Extracted Response Variables JSON:")
    print(response_variables_json)


    # Create the proxy root file (git.xml) inside the apiproxy folder
    proxy_root_content = render_template(
        os.path.join(source_tmpl_directory, "git.xml"),
        proxy_name=proxy_name,
        proxy_base_path=proxy_base_path,
        policies=policies_tmpl
    )
    proxy_root_path = os.path.join(apiproxy_directory, f"{proxy_name}.xml")
    os.makedirs(os.path.dirname(proxy_root_path), exist_ok=True)
    with open(proxy_root_path, "w") as f:
        f.write(proxy_root_content)

    # Create policy files inside the apiproxy/policies folder
    policies_folder = os.path.join(apiproxy_directory, "policies")
    os.makedirs(policies_folder, exist_ok=True)
    for policy in policies_list:
        policy_content = open(os.path.join(policies_tmpl_directory, f"{policy}.xml")).read()
        policy_path = os.path.join(policies_folder, f"{policy}.xml")
        with open(policy_path, "w") as f:
            f.write(policy_content)

    # Create proxy endpoint file (default.xml) inside the apiproxy/proxies folder
    proxies_folder = os.path.join(apiproxy_directory, "proxies")
    os.makedirs(proxies_folder, exist_ok=True)
    proxy_endpoint_content = render_template(
        os.path.join(source_tmpl_directory, "proxies", "default.xml"),
        proxy_base_path=proxy_base_path,
        proxy_steps=proxies_tmpl,
        proxy_name=proxy_name
    )
    proxy_endpoint_path = os.path.join(proxies_folder, "default.xml")
    with open(proxy_endpoint_path, "w") as f:
        f.write(proxy_endpoint_content)

    # Create target endpoint file (default.xml) inside the apiproxy/targets folder
    targets_folder = os.path.join(apiproxy_directory, "targets")
    os.makedirs(targets_folder, exist_ok=True)
    target_endpoint_content = render_template(
        os.path.join(source_tmpl_directory, "targets", "default.xml"),
        target_server_name=target_server_name
    )
    target_endpoint_path = os.path.join(targets_folder, "default.xml")
    with open(target_endpoint_path, "w") as f:
        f.write(target_endpoint_content)

    # Create a zip file containing the API name folder and its structure
    zip_file_path = os.path.join(proxy_bundle_directory, f"{proxy_name}.zip")
    with ZipFile(zip_file_path, 'w') as zipf:
        # Add the apiproxy folder and its content
        zipf.write(apiproxy_directory, os.path.relpath(apiproxy_directory, proxy_bundle_directory))  # Add the folder itself
        
        # Add all the files inside the apiproxy directory
        for root, dirs, files in os.walk(apiproxy_directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, proxy_bundle_directory))

    # Output the proxy root content (similar to Terraform output)
    print(proxy_root_content)

# Main function to handle command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--proxy_category', required=True)
    parser.add_argument('--proxy_name', required=True)
    parser.add_argument('--proxy_base_path', required=True)
    parser.add_argument('--target_server_name', required=True)
    parser.add_argument('--gcp_project_id', required=True)
    parser.add_argument('--gcp_access_token', required=True)
    parser.add_argument('--request_extract_variables', required=True)
    parser.add_argument('--response_extract_variables', required=True)

    args = parser.parse_args()
    
    generate_proxy_bundle(
        args.proxy_category,
        args.proxy_name,
        args.proxy_base_path,
        args.target_server_name,
        args.gcp_project_id,
        args.gcp_access_token,
        args.request_extract_variables,
        args.response_extract_variables
    )