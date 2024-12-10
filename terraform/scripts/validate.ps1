param (
    [string]$Token,
    [string]$ApigeeBaseUrl,
    [string]$ProxyBundlePath
)

# Set the authorization header
$Headers = @{
    "Authorization" = "Bearer $Token"
}

# Check if the file exists
if (-Not (Test-Path $ProxyBundlePath)) {
    Write-Output "FAIL: Proxy bundle file not found at $ProxyBundlePath"
    exit 1
}

# Prepare the body for sending the file
$Body = @{
    file = Get-Item -Path $ProxyBundlePath
}

# Send the request with the file in the body
try {
    $Response = Invoke-RestMethod -Uri "$ApigeeBaseUrl/apis?name=apiproxy&action=validate&validate=true" `
                                  -Method Post `
                                  -Headers $Headers `
                                  -Form $Body `
                                  -ErrorAction Stop
    Write-Output "PASS: HTTP Status Code: $($Response.StatusCode)"
} catch {
    Write-Output "FAIL: HTTP Status Code: $($_.Exception.Response.StatusCode)"
    exit 1
}
