output "vm_public_ip_address" {
  description = "Exact public IP address of the created virtual machine."
  value       = azurerm_public_ip.vm.ip_address
}

output "web_interface_url" {
  description = "HTTP URL for the web interface."
  value       = "http://${azurerm_public_ip.vm.ip_address}:${var.web_port}"
}
