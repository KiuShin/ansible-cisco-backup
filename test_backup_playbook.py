import subprocess
import sys
import os
import re
from glob import glob
import yaml



# Config
playbook ="backup_playbook.yml"
inventory = "inventory.yml"

def run_command(command):
    """Run a shell command and return output, exit code"""
    try:
        result = subprocess.run(
            command, shell=True, check=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def test_syntax():
    print("\n[TEST 1] Syntax Check")
    cmd = f"ansible-playbook {playbook} --syntax-check -i {inventory}"
    out, err, code = run_command(cmd)
    print(out)
    if code != 0:
        print("[ERROR] Syntax check failed:\n", err)
    else:
        print("[PASS] Syntax looks good!")

def test_inventory():
    print("\n[TEST 2] Inventory + Host Iteration Test")
    cmd = f"ansible all -i inventory.yml -m debug -a \"msg='Hello from {{ inventory_hostname }}'\""

    out, err, code = run_command(cmd)
    print(out)
    if code != 0:
        print("[ERROR] Inventory parsing failed:\n", err)
    else:
        print("[PASS] Inventory parsed successfully!")

def test_connectivity():
    print("[TEST 3] Connectivity Test (Ping)")
    cmd = f"ansible all -i {inventory} -m ping"
    out, err, code = run_command(cmd)
    print(out)
    if code !=0:
        print("[WARN] Some hosts may be unreachable:\n", err)
    else:
        print("[PASS] Connectivity test completed!")

def test_backup_logic():
    print("\n[TEST 4] Backup Logic Test (Offline)")
    cmd = "ansible-playbook test_backup_logic.yml"
    out, err, code = run_command(cmd)

    print(out)
    if code !=0:
        print("[ERROR] Backup logic test failed:")
        print(err)
    else:
        print("[PASS] Backup logic executed successfully")


def test_cfg_exists():
    print("\n[TEST 5] Back up File Validation (.cfg)")

    config_dir ="./configs"

    if not os.path.exists(config_dir):
        print("[FAIL] configs/ directory does not exist")
        return False

    cfg_files =[
        f for f in os.listdir(config_dir)
        if f.endswith("cfg")
    ]

    if not cfg_files:
        print("[FAIL] No .cfg backup files found in configs/")
        return False

    print(f"[PASS] Found {len(cfg_files)} backup file(s):")
    for f in cfg_files:
        print(f" -{f}")

    return True

def test_backup_files():
    CONFIG_DIR ="./configs/"
    results = {"missing_files":[], "empty_files":[], "bad_names":[], "basic_keywords":[]}

    filename_pattern = re.compile(r'^[\w-]+_\d{8}_\d{6}\.cfg$')
    required_keywords = ["hostname", "interface", "version"]

    cfg_files = glob(os.path.join(CONFIG_DIR, "*.cfg"))

    if not cfg_files:
        print("[FAIL] No backup files found!")
        return
    for file_path in cfg_files:
        filename = os.path.basename(file_path)

    #validate filename
    if not filename_pattern.match(filename):
        results["bad_names"].append(filename)

    #validate file is not empty
    if os.path.getsize(file_path) == 0:
        results["empty_files"].append(filename)

    #print results
    if any(results.values()):
        print("[FAIL] Issues found with backup files:")
        for key, filens in nresults.items():
            if files:
                print(f"  {key}: {files}")
    else:
        print("[Pass] All backup files exist, non empty and valid.")

def extract_hosts(inventory_section, hosts=None):
    if hosts is None:
        hosts = set()

    # Collect hosts at this level
    if "hosts" in inventory_section:
        hosts.update(inventory_section["hosts"].keys())

    # Recurse into children groups
    if "children" in inventory_section:
        for child in inventory_section["children"].values():
            extract_hosts(child, hosts)

    return hosts

def load_inventory_hosts(inventory_file="inventory.yml"):
    with open(inventory_file) as f:
        inventory = yaml.safe_load(f)

    return sorted(extract_hosts(inventory.get("all", {})))

def extract_backup_hosts(cfg_files):
    hosts = {}
    for path in cfg_files:
        filename = os.path.basename(path)
        host = filename.split("_")[0]  # extract hostname
        if host in hosts:
            hosts[host].append(filename)
        else:
            hosts[host] = [filename]
    return hosts

def test_inventory_backup_correlation():
    inventory_hosts = load_inventory_hosts()
    cfg_files = glob("configs/*cfg")
    backup_hosts = extract_backup_hosts(cfg_files)

    missing_backups = [
        host for host in inventory_hosts if host not in backup_hosts
    ]

    if missing_backups:
        print("[ FAIL ] Inventory hosts missing backups:")
        for host in missing_backups:
            print(f"  -{host}")
    else:
        print("[PASS] All inventory host have backups")

    # warn about orphan backups
    orphan_files = []
    for host, files in backup_hosts.items():
        if host not in inventory_hosts:
            orphan_files.extend(files)  # add all filenames for that orphan host

    if orphan_files:
        print("[WARN] Orphan backup files found:")
        for filename in orphan_files:
            print(f"  - {filename}")


def run_all_test():
    test_syntax()
    test_inventory()
    test_connectivity()
    test_backup_logic()
    test_cfg_exists()
    test_backup_files()
    test_inventory_backup_correlation()
    print("\n[INFO] ALL tests attempted. Review above for pass/fail details.")
    


if __name__ == "__main__":
    run_all_test()