locals {
  xml_indent             = 4
  source_tmpl_directory  = "${path.module}\\templates\\bundle\\apiproxy"
  proxy_bundle_directory = "${var.proxy_bundle_directory}\\${var.proxy_name}\\apiproxy"
  policies_list          = var.categories[var.proxy_category]

  policies_tmpl = indent(
    local.xml_indent,
    join("\n", [for k in local.policies_list : "<Policy>${k}</Policy>"])
  )

  proxies_tmpl = indent(
    local.xml_indent,
    join("\n", [for k in local.policies_list : "<Step>\n  <Name>${k}</Name>\n</Step>"])
  )
}

resource "local_file" "proxy_root" {
  content = templatefile("${local.source_tmpl_directory}\\git.xml", {
    proxy_name      = var.proxy_name,
    proxy_base_path = var.proxy_base_path,
    policies        = local.policies_tmpl
  })
  filename = "${path.module}\\${local.proxy_bundle_directory}\\${var.proxy_name}.xml"
}

resource "local_file" "policies" {
  for_each = toset(local.policies_list)
  content  = file("${path.module}\\templates\\policies\\${each.key}.xml")
  filename = "${path.module}\\${local.proxy_bundle_directory}\\policies\\${each.key}.xml"
}

resource "local_file" "proxy_endpoint" {
  content = templatefile("${local.source_tmpl_directory}\\proxies\\default.xml", {
    proxy_base_path = var.proxy_base_path,
    proxy_steps     = local.proxies_tmpl,
    proxy_name      = var.proxy_name
  })
  filename = "${path.module}\\${local.proxy_bundle_directory}\\proxies\\default.xml"
}


resource "local_file" "target_endpoint" {
  content = templatefile("${local.source_tmpl_directory}\\targets\\default.xml", {
    target_server_name = var.target_server_name
  })
  filename = "${path.module}\\${local.proxy_bundle_directory}\\targets\\default.xml"
}


data "archive_file" "proxy_bundle_zip" {
  type        = "zip"
  source_dir  = "${var.proxy_bundle_directory}\\${var.proxy_name}"
  output_path = "${var.proxy_bundle_directory}\\${var.proxy_name}.zip"
  depends_on = [
    local_file.proxy_root,
    local_file.policies,
    local_file.proxy_endpoint,
    local_file.target_endpoint
  ]
}

output "name" {
  value = local_file.proxy_root.content
}
