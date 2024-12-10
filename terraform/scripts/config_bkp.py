# Python dictionary equivalent of the Terraform variables
variables = {
    "gcp_project_id": "booming-pride-432710-j9",
    "proxy_category": "low",
    "proxy_bundle_directory": "proxies_export",
    "categories": {
        "low": ["VAPI", "ML"],
        "medium": ["VAPI", "QP", "ML"],
        "high": [
            "AM-commonLogging", "AM-requestFromClientLog", "AM-RequestPayloadToBackendLog", 
            "AM-responsePayloadFromBackendLog", "AM-responseToClientBefore_Enc", 
            "AM-responseToClientLog", "AM-setErrorResponsePayload", "AM-SetPayload", 
            "AM-setPayloadResponse", "AM-setSuccessFlag", "EV-RequestLogs", 
            "EV-ResponseErrorCodeLogs", "FC-faultRules", "FC-joseDecryption", 
            "FC-joseEncryption", "FC-preFlow", "FC-ThreatProtection", 
            "RF-faultResponseMethodNotAllowed", "RF-faultResponseNotFound", 
            "RF-responsePayloadValidation"
        ],
        "critical": ["VAPI", "QP", "SA", "JT", "ML"]
    },
    "proxy_name": "apiproxy",
    "target_server_name": "mocktarget-server",
    "gcp_access_token": "ya29.a0AeDClZAU3v-egCNBwN5v8o4_PPrr89uvFSfSwU3xbJb6u0iRfdzfL-MRyT1TS6zyub_N545UAKiYOiLaH5X9D5yPW8ragmnjJI-SvvwIcH4dZ_KWs-fOWP9o-AAEv-3B1jvwAU9S7nhjladJEQ-KI58CSBly8mN388B5YSuEGT6YvX2h2bKqItermnD-063vU8RrccQCy5-ZZ4_7eLfL5OusTe66ZdYfzYEe3Hy6w54iFjlRIRbU6yyA9HZtjBZo8wsmkDhBir81Uc9AJpkbmMog5kMUuZD99YgiZLvJMj0ZuM7fWBjOBUeTKHhJpsaZZhpJYHKCpPrYf6_fXjRST6gdFhTmcYxEdCLOZ81RUdScg674ZlGLJrwj-zmaAURdnjqlkiNJBc6Nc_7IC6L-WSIfcOJ4mg7JRx0waCgYKAYgSARESFQHGX2Mih2_7hbVzG7C85wX5oycLDg0427"  # Set this value securely
}

# Accessing the variables in Python
gcp_project_id = variables["gcp_project_id"]
proxy_category = variables["proxy_category"]
proxy_bundle_directory = variables["proxy_bundle_directory"]
categories = variables["categories"]
proxy_name = variables["proxy_name"]
proxy_base_path = variables["proxy_base_path"]
target_server_name = variables["target_server_name"]
gcp_access_token = variables["gcp_access_token"]

# Example usage of variables
print(f"GCP Project ID: {gcp_project_id}")
print(f"Proxy Name: {proxy_name}")
print(f"Proxy Bundle Directory: {proxy_bundle_directory}")
