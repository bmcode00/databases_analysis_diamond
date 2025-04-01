import os
import subprocess

print("Creating DMND files using diamond...")

def check_diamond_installed():
    try:
        subprocess.run(["diamond", "version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("diamond is not installed!")
        return False
    except subprocess.CalledProcessError:
        print("Error while checking diamond version!")
        return False

def create_dmnd_database(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".fasta"):
            input_file_path = os.path.join(input_folder, filename)
            db_name = filename.replace(".fasta", "").split(".")[0]
            output_db_path = os.path.join(output_folder, f"{db_name}.dmnd")

            command = [
                "diamond", "makedb",
                "--in", input_file_path,
                "--db", output_db_path
            ]
            
            try:
                subprocess.run(command, check=True)
                print(f" DMND database created for file {filename}.")
            except subprocess.CalledProcessError as e:
                print(f" Error creating DMND database for file {filename}: {e}")

input_folder = os.path.expanduser("~/Desktop/Databases_analysis_diamond/Cleaned_sequences_db")
output_folder = os.path.expanduser("~/Desktop/Databases_analysis_diamond/DMND_files_db")

if check_diamond_installed():
    create_dmnd_database(input_folder, output_folder)

print("DMND files creation completed, results saved in 'DMND_files_db' subfolder.")

if __name__ == "__main__":
    pass
