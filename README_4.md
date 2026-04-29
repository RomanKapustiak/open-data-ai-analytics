# Open Data AI Analytics: Azure Deployment (Terraform)
## Виконав: Капустяк Роман (ШІ-33) [repo link](https://github.com/RomanKapustiak/open-data-ai-analytics)

Ця частина проєкту містить конфігурацію для автоматичного розгортання системи в хмарі Microsoft Azure за допомогою Terraform та cloud-init.

## Вимоги
- Акаунт Microsoft Azure (наприклад, Azure for Students).
- Доступ до Azure Cloud Shell.

## Структура інфраструктури
Terraform створює:
- Linux VM (Ubuntu 22.04)
- Віртуальну мережу (VNet) та підмережу
- Публічну IP-адресу
- Правила безпеки (NSG) для портів 22 та 8000

## Інструкція з розгортання

1. **Відкрийте Azure Cloud Shell** (Bash).
2. **Згенеруйте SSH-ключ** (якщо немає):
```bash
ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa
 ```
    
3. Склонуйте репозиторій:

```bash
git clone [https://github.com/RomanKapustiak/open-data-ai-analytics](https://github.com/RomanKapustiak/open-data-ai-analytics)
cd open-data-ai-analytics/terraform
```
4. Ініціалізуйте Terraform:

```Bash
terraform init
```
5. Запустіть розгортання:

```Bash
terraform apply -var="admin_ssh_public_key=$(cat ~/.ssh/id_rsa.pub)" -var="location=westeurope" -var="vm_size=Standard_B2s_v2" -var="resource_group_name=open-data-ai-analytics-rg-v2"
```
Введіть yes для підтвердження.

## Перевірка результату
Після завершення (Apply complete!) зачекайте 5-7 хвилин для виконання сценаріїв cloud-init.
Додаток буде доступний за адресою:
http://<VM_PUBLIC_IP>:8000

## Видалення ресурсів
Щоб уникнути зайвих витрат кредитів Azure, видаліть інфраструктуру:

```Bash
terraform destroy -var="admin_ssh_public_key=$(cat ~/.ssh/id_rsa.pub)" -var="location=westeurope" -var="vm_size=Standard_B2s_v2" -var="resource_group_name=open-data-ai-analytics-rg-v2"
```
