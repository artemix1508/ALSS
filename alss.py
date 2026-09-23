import os
import subprocess

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
        "Fedora": "dnf",
        "CentOS": "yum",
        "Arch Linux": "pacman",
        "openSUSE": "zypper",
        "Linux Mint": "apt",
        "Omarchy": "pacman",
        "CachyOS": "pacman"
    }
    return package_managers.get(distro_name, "Unknown package manager")

distro_info = get_distro_info()
package_manager = get_package_manager(distro_info)
gpu_info = get_gpu_info()
for i, gpu in enumerate(gpu_info, start=1):
    print(f"GPU{i}: {gpu['Vendor']}, {gpu['Model']}")
print(f"Detected package manager: {package_manager}")
