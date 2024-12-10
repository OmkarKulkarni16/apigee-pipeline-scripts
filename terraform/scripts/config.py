variables = {
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
}

categories = variables["categories"]

print(categories)

