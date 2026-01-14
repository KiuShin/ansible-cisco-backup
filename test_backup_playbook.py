import subprocess
import sys
import os

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

def run_all_test():
    #test_syntax()
    #test_inventory()
    #test_connectivity()
    #test_backup_logic()
    test_cfg_exists()
    print("\n[INFO] ALL tests attempted. Review above for pass/fail details.")
    


if __name__ == "__main__":
    run_all_test()