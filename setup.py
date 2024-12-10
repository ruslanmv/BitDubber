import os
import subprocess

def configure_display():
    # Define the environment variable setup
    DISPLAY_CONFIG = "export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0"
    LIBGL_CONFIG = "export LIBGL_ALWAYS_INDIRECT=0"

    # Determine which shell configuration file to update
    bashrc_path = os.path.expanduser("~/.bashrc")
    zshrc_path = os.path.expanduser("~/.zshrc")

    # Check if the user uses .bashrc or .zshrc
    if os.path.exists(bashrc_path):
        shell_config_path = bashrc_path
    elif os.path.exists(zshrc_path):
        shell_config_path = zshrc_path
    else:
        print("No shell configuration file (.bashrc or .zshrc) found.")
        return

    # Add the DISPLAY configuration to the shell configuration file
    with open(shell_config_path, "a") as shell_config:
        shell_config.write(f"\n# Configure DISPLAY for WSL\n{DISPLAY_CONFIG}\n{LIBGL_CONFIG}\n")

    print(f"Added DISPLAY configuration to {shell_config_path}.")

    # Inform the user to source the file manually
    print("Please run the following command to apply the changes:")
    print(f"source {shell_config_path}")

# Example usage if imported from another script
def main():
    configure_display()

if __name__ == "__main__":
    main()