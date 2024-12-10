variable "gcp_project_id" {
  default = "apigee-payg-377208"
  type    = string
}

variable "proxy_category" {
  default = "low"
  type    = string
}

variable "proxy_bundle_directory" {
  type    = string
  default = "proxies_export"
}

variable "categories" {
  type = map(list(string))
  default = {
    "low" : ["VAPI", "ML"],
    "medium" : ["VAPI", "QP", "ML"],
    "high" : ["AM-commonLogging", "AM-requestFromClientLog", "AM-RequestPayloadToBackendLog", "AM-responsePayloadFromBackendLog", "AM-responseToClientBefore_Enc", "AM-responseToClientLog", "AM-setErrorResponsePayload", "AM-SetPayload", "AM-setPayloadResponse", "AM-setSuccessFlag", "EV-RequestLogs", "EV-ResponseErrorCodeLogs", "FC-faultRules", "FC-joseDecryption", "FC-joseEncryption", "FC-preFlow", "FC-ThreatProtection", "RF-faultResponseMethodNotAllowed", "RF-faultResponseNotFound", "RF-responsePayloadValidation"],
    "critical" : ["VAPI", "QP", "SA", "JT", "ML"],
  }
}

variable "proxy_name" {
  default = "apiproxy"
  type    = string
}

variable "proxy_base_path" {
  default = "/apiproxy"
  type    = string
}

variable "target_server_name" {
  default = "mocktarget-server"
  type    = string
}

variable "gcp_access_token" {
  type = string
  sensitive = true
}