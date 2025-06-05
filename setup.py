import json
import subprocess
import os

CONFIG_FILE = "setup-tts-dependencies.json"
REQUIREMENTS_FILE = "requirements.txt"
REQUIREMENTS_FLAG = ".requirements_installed"

def load_modules():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def show_modules(modules):
    print("\nAvailable TTS Modules:\n")
    for idx, mod in enumerate(modules):
        print(f"{idx+1}. {mod['name']} - {mod['description']}")
    print(f"{len(modules)+1}. Exit")

def install_requirements():
    if os.path.exists(REQUIREMENTS_FILE) and not os.path.exists(REQUIREMENTS_FLAG):
        print("\nInstalling requirements.txt dependencies...")
        subprocess.run(["pip", "install", "-r", REQUIREMENTS_FILE])
        with open(REQUIREMENTS_FLAG, "w") as f:
            f.write("installed")

def install_dependencies(mod):
    print(f"\nInstalling dependencies for {mod['name']}...")
    for dep in mod['dependencies']:
        print(f"Installing {dep}...")
        subprocess.run(["pip", "install", dep])

def main():
    install_requirements()
    modules = load_modules()
    while True:
        show_modules(modules)
        try:
            choice = int(input("\nSelect a TTS module to install (or exit): "))
            if choice == len(modules)+1:
                print("Exiting.")
                break
            elif 1 <= choice <= len(modules):
                install_dependencies(modules[choice - 1])
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

if __name__ == "__main__":
    main()
