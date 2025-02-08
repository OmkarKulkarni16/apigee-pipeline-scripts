variables = {
    "categories": {
        "low": ["VAPI", "ML"],
        "JOSE-MediumWithDS": ["AM-captureRespErrorCodes", "AM-commonLogging", "AM-RequestPayloadToBackendLog", "AM-responsePayloadFromBackendLog", "AM-responseToClientBefore_Enc", "AM-responseToClientLog", "AM-setErrorResponsePayload", "AM-setErrorRespPayload", "AM-SetPayload", "AM-setPayloadResponse", "AM-setSuccessFlag", "DC-captureResponseFields", "EV-setconsentRequestLogs", "EV-setResponseErrorCodeLogs", "FC-faultRules", "FC-joseDecryption", "FC-joseEncryption", "FC-Logging", "FC-preFlow", "FC-setResponseHeaders", "FC-ThreatProtection", "RF-faultResponseMethodNotAllowed", "RF-faultResponseNotFound", "RF-responsePayloadValidation"],
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

