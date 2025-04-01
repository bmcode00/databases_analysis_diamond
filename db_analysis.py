import os
import subprocess
import sys
import pandas as pd

# Function to clear the screen
def clear_screen():
    os.system("clear")

# Function to check and install dependencies (Linux only)
def check_and_install_dependencies():
    print("\n Checking dependencies (Linux)...\n")
    
    # Check if this is Linux
    if not sys.platform.startswith('linux'):
        print("This program only works on Linux")
        return False
    
    # Dependencies dictionary: [name, check command, install command]
    dependencies = {
        "Diamond": ["diamond --version", "sudo apt-get install -y diamond"],
        "R": ["Rscript --version", "sudo apt-get install -y r-base"],
        "R libraries (tidyverse, conflicted)": [
            "Rscript -e 'library(tidyverse); library(conflicted)'",
            "Rscript -e 'install.packages(c(\"tidyverse\", \"conflicted\"), repos=\"https://cloud.r-project.org\")'"
        ]
    }
    
    all_ok = True
    
    for name, commands in dependencies.items():
        try:
            # Check if dependency is installed
            subprocess.run(
                commands[0], 
                shell=True, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            print(f" {name} is installed")
        except subprocess.CalledProcessError:
            print(f" {name} is not installed")
            if input(f"Do you want to install {name}? (Y/n): ").lower() in ('y', ''):
                try:
                    print(f"Installing {name}...")
                    subprocess.run(commands[1], shell=True, check=True)
                    print(f" {name} was successfully installed")
                except subprocess.CalledProcessError as e:
                    print(f" Error installing {name}: {e}")
                    all_ok = False
            else:
                all_ok = False
    
    return all_ok

# Function to create folders
def create_folders():
    desktop_path = os.path.expanduser("~/Desktop")
    main_folder = os.path.join(desktop_path, "Databases_analysis_diamond")
    seq_folder = os.path.join(main_folder, "Sequences_db")
    functions_folder = os.path.join(main_folder, "Functions")

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    if not os.path.exists(seq_folder):
        os.makedirs(seq_folder)
    if not os.path.exists(functions_folder):
        os.makedirs(functions_folder)

    return main_folder, seq_folder, functions_folder

# Function to display menu
def show_menu():
    clear_screen()
    print("Databases Analysis diamond | 2025")
    print("Developed by: eng. Bogdan Marczak & dr. eng. Andrzej Lyskowski")
    print("Rzeszów University of Technology\n")
    print("1. Check dependencies (diamond, RStudio, libraries)")
    print("2. Create folders")
    print("3. Clean FASTA")
    print("4. Convert FASTA to DMND")
    print("5. Run diamond comparison")
    print("6. DAIRId & IDAIRId - currently unavailable")
    print("7. Visualize results (RStudio)")
    print("8. Exit\n")
    choice = input("Select option: ")
    return choice

# Function to run external scripts
def run_external_script(script_name, *args):
    try:
        if script_name.endswith(".py"):
            result = subprocess.run(["python3", script_name] + list(args), capture_output=True, text=True)
        elif script_name.endswith(".R"):
            result = subprocess.run(["Rscript", script_name] + list(args), capture_output=True, text=True)
        else:
            raise ValueError("Unsupported file type")

        print("\n" + result.stdout)
        if result.returncode != 0:
            print(f"\n Error: {result.stderr}\n")
        else:
            print("\n Script executed successfully\n")
    except Exception as e:
        print(f"\n Error: {e}\n")
    input("\n Press ENTER to continue...")

# Function to wait for key press
def wait_for_key():
    input("\n Press ENTER to continue...")

# Main program function
def main():
    clear_screen()
    
    # Path to functions folder
    desktop_path = os.path.expanduser("~/Desktop")
    main_folder = os.path.join(desktop_path, "Databases_analysis_diamond")
    functions_folder = os.path.join(main_folder, "Functions")

    while True:
        choice = show_menu()

        if choice == "1":
            if not check_and_install_dependencies():
                print("\n Some dependencies are missing. Some features may not work.")
            input("\n Press ENTER to continue...")
        elif choice == "2":
            main_folder, seq_folder, functions_folder = create_folders()
            print(f"\n Folders have been created or already exist.\n")
            print(f" Instructions:\n"
                  f"1. Paste the sequence files downloaded from databases (filename: e.g., APD) into the Sequences_db subfolder.\n"
                  f"2. Paste the functions (clean_fasta.py, convert_to_dmnd.py, run_diamond_comparison.py, DAIRId_IDAIRId.py, and visualize_rstudio.R) into the Function subfolder.")
            input("\n Press ENTER to continue...")
        elif choice == "3":
            run_external_script(os.path.join(functions_folder, "clean_fasta.py"))
        elif choice == "4":
            run_external_script(os.path.join(functions_folder, "convert_to_dmnd.py"))
        elif choice == "5":
            reference_db = input("Enter reference database (or 'all' to compare all databases): ")
            run_external_script(os.path.join(functions_folder, "run_diamond_comparison.py"), reference_db)
        elif choice == "7":
            data_folder = input("Enter reference database (or 'all' to compare all databases): ")
            max_length = input("Enter maximum peptide length for X axis (or 'auto' for automatic adjustment): ")
            run_external_script(os.path.join(functions_folder, "visualize_rstudio.R"), data_folder, max_length)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.\n")
            wait_for_key()

if __name__ == "__main__":
    # Check if pandas is installed
    try:
        import pandas as pd
    except ImportError:
        print("Missing pandas library. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pandas"], check=True)
        import pandas as pd
    
    main()