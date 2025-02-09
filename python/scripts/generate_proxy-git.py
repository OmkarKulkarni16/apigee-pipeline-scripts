import sys
import os
import string
from zipfile import ZipFile
import argparse

# Get the current script's directory (the root of the repository)
repo_directory = os.path.dirname(os.path.abspath(__file__))

# Define paths
source_tmpl_directory = os.path.join(repo_directory, '..', 'templates', 'bundle', 'apiproxy') 
proxy_bundle_directory = os.path.join(repo_directory, '..', 'proxies_export') 
apiproxy_directory = os.path.join(proxy_bundle_directory, 'apiproxy')  
policies_tmpl_directory = os.path.join(repo_directory, '..', 'templates', 'policies')  

# Ensure required directories exist
os.makedirs(proxy_bundle_directory, exist_ok=True)
os.makedirs(apiproxy_directory, exist_ok=True)

# Import variables from config
sys.path.append(os.path.join(repo_directory, '..', 'scripts'))  
from config import variables  

# ✅ Function to sanitize proxy name (prevent encoding issues)
def clean_name(name):
    return name.replace(' ', '_').replace('\n', '').replace('\r', '').strip()

# ✅ Function to clean **all old XML files** before generating a new one
def clean_old_files():
    """Deletes all old XML files before generating a new one"""
    for filename in os.listdir(apiproxy_directory):
        if filename.endswith(".xml"):
            print(f"🗑️ Deleting old XML file: {filename}")  # Debugging
            os.remove(os.path.join(apiproxy_directory, filename))

# Function to generate policies template
def generate_policies_template(policies_list):
    return "\n".join([f"<Policy>{policy}</Policy>" for policy in policies_list])

# Function to generate proxies template
def generate_proxies_template(policies_list):
    return "\n".join([f"<Step>\n  <Name>{policy}</Name>\n</Step>" for policy in policies_list])

# Function to render templates (similar to Terraform templatefile)
def render_template(template_path, **kwargs):
    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()
    return string.Template(template).substitute(kwargs)

# Function to generate the proxy bundle
def generate_proxy_bundle(proxy_category, proxy_name, proxy_base_path, target_server_name, gcp_project_id, gcp_access_token):
    proxy_name = clean_name(proxy_name)  # Sanitize proxy name

    # ✅ Clean old XML files before generating new ones
    clean_old_files()

    # Fetch policies from the config file
    categories = variables.get("categories", {})  
    policies_list = categories.get(proxy_category, [])

    # Generate policy and proxy templates
    policies_tmpl = generate_policies_template(policies_list)
    proxies_tmpl = generate_proxies_template(policies_list)

    # ✅ Generate the main proxy XML file
    proxy_root_content = render_template(
        os.path.join(source_tmpl_directory, "git.xml"),
        proxy_name=proxy_name,
        proxy_base_path=proxy_base_path,
        policies=policies_tmpl
    )
    proxy_root_path = os.path.join(apiproxy_directory, f"{proxy_name}.xml")
    with open(proxy_root_path, "w", encoding="utf-8") as f:
        f.write(proxy_root_content)

    # ✅ Generate policies (only if they exist)
    policies_folder = os.path.join(apiproxy_directory, "policies")
    os.makedirs(policies_folder, exist_ok=True)
    for policy in policies_list:
        policy_path = os.path.join(policies_tmpl_directory, f"{policy}.xml")
        if os.path.exists(policy_path):  # Check if policy file exists before copying
            with open(policy_path, "r", encoding="utf-8") as f:
                policy_content = f.read()
            with open(os.path.join(policies_folder, f"{policy}.xml"), "w", encoding="utf-8") as f:
                f.write(policy_content)

    # ✅ Generate proxy endpoint file
    proxies_folder = os.path.join(apiproxy_directory, "proxies")
    os.makedirs(proxies_folder, exist_ok=True)
    proxy_endpoint_content = render_template(
        os.path.join(source_tmpl_directory, "proxies", "default.xml"),
        proxy_base_path=proxy_base_path,
        proxy_steps=proxies_tmpl,
        proxy_name=proxy_name
    )
    with open(os.path.join(proxies_folder, "default.xml"), "w", encoding="utf-8") as f:
        f.write(proxy_endpoint_content)

    # ✅ Generate target endpoint file
    targets_folder = os.path.join(apiproxy_directory, "targets")
    os.makedirs(targets_folder, exist_ok=True)
    target_endpoint_content = render_template(
        os.path.join(source_tmpl_directory, "targets", "default.xml"),
        target_server_name=target_server_name
    )
    with open(os.path.join(targets_folder, "default.xml"), "w", encoding="utf-8") as f:
        f.write(target_endpoint_content)

    # ✅ Create a zip file with only the correct structure
    zip_file_path = os.path.join(proxy_bundle_directory, f"{proxy_name}.zip")
    with ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(apiproxy_directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, proxy_bundle_directory))

    # ✅ Log generated proxy details
    print(f"✅ Proxy bundle generated: {zip_file_path}")
    print(f"✅ Proxy name: {proxy_name}")
    print(f"✅ Proxy base path: {proxy_base_path}")
    print(f"✅ Proxy category: {proxy_category}")

# ✅ Main function to handle command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--proxy_category', required=True)
    parser.add_argument('--proxy_name', required=True)
    parser.add_argument('--proxy_base_path', required=True)
    parser.add_argument('--target_server_name', required=True)
    parser.add_argument('--gcp_project_id', required=True)
    parser.add_argument('--gcp_access_token', required=True)
    
    args = parser.parse_args()
    
    # Generate proxy bundle
    generate_proxy_bundle(
        args.proxy_category,
        args.proxy_name,
        args.proxy_base_path,
        args.target_server_name,
        args.gcp_project_id,
        args.gcp_access_token
    )
