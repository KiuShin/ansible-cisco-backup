# Ansible Cisco Device Backup Automation

## Overview

This project automates the backup of Cisco network device configurations using Ansible. The goal is to create a reliable, repeatable, and testable backup workflow that can be validated even when network devices are offline.

Backups are saved as timestamped `.cfg` files to support versioning, auditability, and easy restoration.

This project is designed as a **portfolio-quality infrastructure automation project**, following best practices for documentation, testing, and incremental development.

---

## Key Objectives

* Automate the collection of Cisco device running configurations
* Store backups as timestamped configuration files
* Support offline development and validation
* Separate logic validation from artifact validation
* Use Ansible + Python together in a practical workflow

---

## Technologies Used

* **Ansible** (network automation)
* **Cisco IOS Ansible Collection** (`cisco.ios`)
* **Python 3** (test runner and validation)
* **WSL (Windows Subsystem for Linux)**
* **Visual Studio Code**
* **Git / GitHub**

---

## Project Structure

```
ansible_cisco_backup/
├── README.md              # Project documentation
├── backup_playbook.yml    # Ansible playbook for device backups
├── inventory.yml          # Ansible inventory
├── configs/               # Generated .cfg backup files
├── logs/                  # Backup execution logs
├── tests/                 # Python-based test scripts
│   └── run_tests.py
├── .gitignore             # Ignored files
└── tokens.yml             # **Ignored by Git** - stores secrets or tokens locally
```

---

## Recommended .gitignore

```
# Ansible artifacts
configs/*.cfg
logs/*.log

# Python
__pycache__/
*.pyc

# OS / Editor
.vscode/
.DS_Store

# Temporary files
*.tmp

# Secret token files
tokens.yml
```

---

## How the Backup Works

1. Ansible connects to Cisco devices using SSH
2. The running configuration is retrieved using Cisco IOS modules
3. Output is registered to a variable
4. Configuration is written to a timestamped `.cfg` file
5. Backup success or failure is logged

Each backup file is uniquely named using:

```
<hostname>_<YYYYMMDD>_<HHMMSS>.cfg
```

---

## Testing Strategy

This project uses **incremental tests**, each with a single responsibility.

### Test Breakdown

**Test 1 – Playbook Syntax Validation**
Validates YAML and Ansible syntax.

**Test 2 – Inventory Parsing**
Ensures Ansible can read the inventory and resolve hosts.

**Test 3 – Connectivity Attempt**
Confirms Ansible attempts SSH connections (expected to fail if devices are offline).

**Test 4 – Backup Logic Validation**
Validates backup task logic, variable registration, and task execution order.

**Test 5 – Backup Artifact Validation**
Confirms `.cfg` files are created in the expected directory.

Tests are implemented in Python to allow flexible validation outside of Ansible execution.

---

## Running the Tests

From the project root (inside WSL):

```bash
python3 tests/run_tests.py
```

Test results will display pass/fail output for each validation step.

---

## Offline Development Support

This project is intentionally designed to support development **without requiring live network devices**.

* Syntax and inventory tests run without devices
* Connectivity failures are treated as expected behavior when offline
* Artifact validation confirms correct filesystem behavior

This allows safe iteration and testing before deployment to production environments.

---

## Future Enhancements

* Validate backup file contents (non-empty and expected keywords)
* Add checksum or hash verification
* Support multiple device platforms
* Encrypt backups at rest
* Upload backups to cloud storage (S3, Azure Blob, etc.)
* Add CI pipeline integration

---

## Author Notes

This project was built with a focus on **clarity, testability, and real-world network automation practices**. The approach prioritizes reliability over shortcuts, reflecting how production automation systems are designed and validated.

---

## Disclaimer

This project is for educational and portfolio purposes. Do not store production credentials or sensitive data in this repository.
