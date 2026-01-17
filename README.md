Ansible Cisco Configuration Backup – Test-Driven Automation
Overview

This project implements a test-driven workflow for validating and automating Cisco device configuration backups using Ansible and Python.

The focus of this repository is not monitoring or alerting, but verifying backup logic correctness before wiring it into automated workflows. The test suite validates syntax, inventory parsing, backup file creation, naming conventions, and inventory-to-backup correlation.

This project is designed to be run offline or without live devices, making it suitable for development, CI pipelines, and learning environments.

Project Goals

Validate Ansible backup logic before production use

Ensure backups are created with correct naming conventions

Correlate inventory hosts to generate backup files

Detect missing or orphaned backups

Practice modular, test-driven infrastructure automation

Project Structure
ansible-cisco-backup/
├── backup_playbook.yml          # Main backup playbook
├── test_backup_logic.yml        # Offline logic validation playbook
├── inventory.yml                # Ansible inventory
├── test_backup_playbook.py      # Python test harness
├── configs/                     # Generated .cfg backups
├── logs/                        # Backup logs (if enabled)
├── .gitignore                   # Ignores tokens, secrets, artifacts
└── README.md

Requirements

Python 3.9+

Ansible

PyYAML

Linux / WSL recommended (tested in WSL)

Install dependencies:

pip install pyyaml

Test Suite Overview

The test harness is implemented in test_backup_playbook.py and executed as a single script.

Test Coverage
Test	Description
Test 1	Ansible playbook syntax validation
Test 2	Inventory parsing and host iteration
Test 3	Connectivity test (ping)
Test 4	Offline backup logic execution
Test 5	Backup file existence check
Test 6	Backup file validation (naming, empty files)
Test 7	Inventory ↔ backup correlation (missing/orphan backups)

⚠️ Connectivity failures are treated as warnings, not failures, to support offline testing.

Running the Tests

From the project root:

python3 test_backup_playbook.py


Expected output includes clear [PASS], [FAIL], and [WARN] markers for each test stage.

Backup File Naming Convention

Backups are expected to follow this format:

<hostname>_YYYYMMDD_HHMMSS.cfg


Example:

router1_20240110_153045.cfg


This ensures uniqueness and traceability.

Design Philosophy

Test logic, not state
This project validates backup correctness, not backup health monitoring.

Offline-first
Tests can be run without powered-on devices.

Incremental automation
Backup automation is validated before scheduling or CI integration.

Future Improvements (Optional)

CI integration (GitHub Actions)

Modular test files with a main runner

Encrypted secret handling

Device-specific platform expansion

Disclaimer

This project is for learning and validation purposes and should be adapted and secured before production use.

Author

Built as part of hands-on infrastructure automation practice using Ansible, Python, and Cisco tooling.

## Disclaimer

This project is for educational and portfolio purposes. Do not store production credentials or sensitive data in this repository.

