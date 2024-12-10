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

# Create the multipart form-data body for file upload
$Boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"  # Line feed
$ContentType = "multipart/form-data; boundary=$Boundary"
$FileContent = [System.IO.File]::ReadAllBytes($ProxyBundlePath)
$FileBase64 = [Convert]::ToBase64String($FileContent)

# Construct the form body
$Body = "--$Boundary$LF"
$Body += "Content-Disposition: form-data; name=`"file`"; filename=`"$ProxyBundlePath`"$LF"
$Body += "Content-Type: application/octet-stream$LF$LF"
$Body += "$FileBase64$LF"
$Body += "--$Boundary--$LF"

# Send the request with the file in the body
try {
    $Response = Invoke-RestMethod -Uri "$ApigeeBaseUrl/apis?name=apiproxy&action=validate&validate=true" `
                                  -Method Post `
                                  -Headers $Headers `
                                  -ContentType $ContentType `
                                  -Body $Body `
                                  -ErrorAction Stop
    Write-Output "PASS: HTTP Status Code: $($Response.StatusCode)"
} catch {
    Write-Output "FAIL: HTTP Status Code: $($_.Exception.Response.StatusCode)"
    exit 1
}
