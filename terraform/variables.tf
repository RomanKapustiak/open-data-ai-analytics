variable "location" {
  description = "Azure region for the lab deployment."
  type        = string
  default     = "westeurope"
}

variable "resource_group_name" {
  description = "Resource group name."
  type        = string
  default     = "open-data-ai-analytics-rg"
}

variable "vm_name" {
  description = "Virtual machine name."
  type        = string
  default     = "open-data-ai-analytics-vm"
}

variable "vm_size" {
  description = "Azure VM size."
  type        = string
  default     = "Standard_B1s"
}

variable "admin_username" {
  description = "Admin username for the Azure VM."
  type        = string
  default     = "azureuser"
}

variable "admin_ssh_public_key" {
  description = "SSH public key for Azure VM access."
  type        = string
}

variable "repository_url" {
  description = "Public GitHub repository URL to clone on the VM."
  type        = string
  default     = "https://github.com/RomanKapustiak/open-data-ai-analytics"
}

variable "repository_clone_path" {
  description = "Directory on the VM where the repo will be cloned."
  type        = string
  default     = "/opt/open-data-ai-analytics"
}

variable "web_port" {
  description = "External port exposed for the web application."
  type        = number
  default     = 8000
}

variable "data_dir" {
  description = "DATA_DIR value for the application .env file."
  type        = string
  default     = "/app/data"
}

variable "raw_data_dir" {
  description = "RAW_DATA_DIR value for the application .env file."
  type        = string
  default     = "/app/data/raw"
}

variable "reports_dir" {
  description = "REPORTS_DIR value for the application .env file."
  type        = string
  default     = "/app/reports"
}

variable "plots_dir" {
  description = "PLOTS_DIR value for the application .env file."
  type        = string
  default     = "/app/reports/plots"
}

variable "runtime_dir" {
  description = "RUNTIME_DIR value for the application .env file."
  type        = string
  default     = "/app/runtime"
}

variable "database_path" {
  description = "DATABASE_PATH value for the application .env file."
  type        = string
  default     = "/app/runtime/transport_registry.sqlite3"
}

variable "csv_name" {
  description = "CSV_NAME value for the application .env file."
  type        = string
  default     = "tz_opendata_z01012022_po01032022.csv"
}

variable "download_if_missing" {
  description = "DOWNLOAD_IF_MISSING value for the application .env file."
  type        = string
  default     = "true"
}

variable "web_host" {
  description = "WEB_HOST value for the application .env file."
  type        = string
  default     = "0.0.0.0"
}

variable "db_wait_timeout_seconds" {
  description = "DB_WAIT_TIMEOUT_SECONDS value for the application .env file."
  type        = string
  default     = "120"
}

variable "sample_plot_rows" {
  description = "SAMPLE_PLOT_ROWS value for the application .env file."
  type        = string
  default     = "10000"
}
