import os
import subprocess
import json
import sys

dry_run = "--dry-run" in sys.argv

#-----Start of the functions zone-----

def get_gpu_info():
    result = subprocess.run(["lspci"], capture_output=True, text=True)
    output = result.stdout

    gpus= []

    for line in output.splitlines():
        if "VGA" in line:
            if "NVIDIA" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'NVIDIA', 'Model': model})
            elif "AMD" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'AMD', 'Model': model})
            elif "Intel" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'Intel', 'Model': model})
            pass
    return gpus

def get_distro_info():
    if not os.path.exists('/etc/os-release'):
        return None

    info = {}

    with open('/etc/os-release') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                info[key] = value
    return info

def get_package_manager(distro_info):
    if not distro_info:
        return "Unknown distribution"

    distro_name = distro_info.get('NAME', '').strip('"')
    
    package_managers = {
        "Ubuntu": "apt",
        "Debian": "apt",
        "Fedora Linux": "dnf",
        "CentOS": "yum",
        "Arch Linux": "pacman",
        "openSUSE": "zypper",
        "Linux Mint": "apt",
        "Omarchy": "pacman",
        "CachyOS": "pacman"
    }
    return package_managers.get(distro_name, "Unknown package manager")

def get_recommended_nvidia_driver():
    result_recommended = subprocess.run(["ubuntu-drivers", "devices"], capture_output=True, text=True)
    output_recommended = result_recommended.stdout

    for line in output_recommended.splitlines():
        if "recommended" in line:
            driver = line.split(":")[1].split()[0]
            return driver
    return None

#-----End of the functions zone-----

#-----Main logic-----

if getattr(sys, '_MEIPASS', None):
    config_path = os.path.join(sys._MEIPASS, "config.json")
else:
    config_path = "config.json"

with open(config_path) as f:
    config = json.load(f)

needed_packages = config["needed_packages"]
gpu_drivers = config["gpu_drivers"]
pm_commands = config["pm_commands"]

to_install = []

distro_info = get_distro_info()

package_manager = get_package_manager(distro_info)

gpu_info = get_gpu_info()

print(f"Detected package manager: {package_manager}")
print("----------------------------------------")

for i, gpu in enumerate(gpu_info, start=1):
    print(f"GPU{i}: {gpu['Vendor']}, {gpu['Model']}")
    print("----------------------------------------")

for package in needed_packages.get(package_manager, []):
    command = pm_commands.get(package_manager, {}).get("query", []) + [package]
    check = subprocess.run(command)
    if check.returncode != 0:
        to_install.append(package)

for gpu in gpu_info:
    vendor = gpu['Vendor']
    driver = gpu_drivers.get(vendor, {}).get(package_manager, None)
    
    if driver:
        if vendor == "NVIDIA" and package_manager == "apt":
            recommended = get_recommended_nvidia_driver()
            if recommended:
                driver = recommended
        driver_command = pm_commands.get(package_manager, {}).get("query", []) + [driver]
        check_driver = subprocess.run(driver_command)
        if check_driver.returncode != 0:
            to_install.append(driver)

if to_install:
    if dry_run:
        print(f"Will install: {to_install}")
    else:
        print(f"Installing: {to_install}")
        subprocess.run(pm_commands.get(package_manager, {}).get("install", []) + to_install)
