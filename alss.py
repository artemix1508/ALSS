import os

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
print(f"Detected package manager: {package_manager}")

