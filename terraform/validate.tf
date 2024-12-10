resource "null_resource" "validate" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = <<EOT
      powershell.exe -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File ""${replace(abspath("${path.module}\\scripts\\validate.ps1"), "/", "\\")}"" -Token ""${var.gcp_access_token}"" -ApigeeBaseUrl ""https://apigee.googleapis.com/v1/organizations/${var.gcp_project_id}"" -ProxyBundlePath ""${replace(abspath("${path.module}\\proxies_export\\test1.zip"), "/", "\\")}""' -NoNewWindow -Wait"
    EOT
  }
}
