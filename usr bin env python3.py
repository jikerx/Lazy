#!/usr/bin/env python3

import subprocess
import sys
import os

# Function to run shell commands and capture output
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        sys.exit(1)

# Function to check sudo authentication
def check_sudo():
    print("Please log in with sudo privileges to proceed.")
    run_command("sudo -v")

# Function to detect the Linux distribution and package manager
def get_package_manager():
    # Check distribution from /etc/os-release
    distro_info = run_command("cat /etc/os-release")
    
    if "Ubuntu" in distro_info or "Linux Mint" in distro_info:
        return "apt"
    elif "Arch Linux" in distro_info:
        return "pacman"
    elif "Fedora" in distro_info or "CentOS" in distro_info:
        return "dnf"
    else:
        print("Unsupported distribution or unable to detect package manager.")
        sys.exit(1)

# Function to update the system
def update_system(package_manager):
    print("Starting system update...")
    if package_manager == "apt":
        run_command("sudo apt-get update")
    elif package_manager == "pacman":
        run_command("sudo pacman -Syu")
    elif package_manager == "dnf":
        run_command("sudo dnf update")
    print("System update completed successfully.")

# Function to list upgradable packages
def list_upgradable_packages(package_manager):
    print("Listing upgradable packages...")
    if package_manager == "apt":
        upgradable = run_command("sudo apt-get --just-print upgrade | grep 'Inst'")
    elif package_manager == "pacman":
        upgradable = run_command("sudo pacman -Qu")
    elif package_manager == "dnf":
        upgradable = run_command("sudo dnf list updates")
    print(upgradable)

# Function to upgrade the system
def upgrade_system(package_manager):
    print("Upgrading system packages...")
    if package_manager == "apt":
        run_command("sudo apt-get upgrade -y")
    elif package_manager == "pacman":
        run_command("sudo pacman -Syu --noconfirm")
    elif package_manager == "dnf":
        run_command("sudo dnf upgrade -y")
    print("System upgrade completed successfully.")

# Function to check if autoremove is needed (for apt and pacman)
def check_autoremove(package_manager):
    print("Checking for unused packages...")
    if package_manager == "apt":
        autoremove_output = run_command("sudo apt-get autoremove --dry-run")
        if "will be removed" in autoremove_output:
            print("The system has unused packages that can be removed.")
            print("Run 'sudo apt-get autoremove' to clean them up.")
    elif package_manager == "pacman":
        autoremove_output = run_command("sudo pacman -Rns $(pacman -Qdtq)")
        if autoremove_output.strip():
            print("The system has unused packages that can be removed.")
            print("Run 'sudo pacman -Rns' to clean them up.")
    else:
        print("Autoremove is not supported for this package manager.")

# Main function to run all tasks
def main():
    # Perform sudo authentication
    check_sudo()

    # Detect package manager
    package_manager = get_package_manager()

    # Update the system
    update_system(package_manager)

    # List upgradable packages
    list_upgradable_packages(package_manager)

    # Ask to continue with upgrade
    input("Press Enter to continue with the upgrade or Ctrl+C to cancel...")

    # Upgrade the system
    upgrade_system(package_manager)

    # Check for autoremove
    check_autoremove(package_manager)

if __name__ == "__main__":
    main()

