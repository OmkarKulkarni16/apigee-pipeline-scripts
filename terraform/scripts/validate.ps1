param (
    [string]$Token,
    [string]$ApigeeBaseUrl,
    [string]$ProxyBundlePath
)

$Headers = @{
    "Authorization" = "Bearer $Token"
}

# Send the request and get the HTTP status code
$HttpStatusCode = (Invoke-RestMethod -Uri "$ApigeeBaseUrl/apis?name=apiproxy&action=validate&validate=true" `
                    -Method Post -Headers $Headers -Form @{ file = Get-Item $ProxyBundlePath } `
                    -ErrorAction Stop).StatusCode

if ($HttpStatusCode -ne 200) {
    Write-Output "FAIL HTTP_STATUS_CODE --> $HttpStatusCode"
    exit 1
} else {
    Write-Output "PASS HTTP_STATUS_CODE --> $HttpStatusCode"
}
