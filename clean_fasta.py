import os

print("Cleaning FASTA files...")

def clean_sequence(sequence):
    valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
    sequence = sequence.replace(" ", "").replace("\t", "")
    return ''.join([aa for aa in sequence if aa in valid_amino_acids])

def clean_fasta_file(input_file, output_file):
    total_sequences = 0
    cleaned_sequences = 0
    sequence = []
    previous_header = None

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                total_sequences += 1
                if previous_header and sequence:
                    outfile.write(f">{previous_header}\n")
                    outfile.write(''.join(sequence) + '\n')
                    cleaned_sequences += 1
                previous_header = line[1:]
                sequence = []
            elif previous_header:
                cleaned_sequence = clean_sequence(line)
                if cleaned_sequence:
                    sequence.append(cleaned_sequence)
        if previous_header and sequence:
            outfile.write(f">{previous_header}\n")
            outfile.write(''.join(sequence) + '\n')
            cleaned_sequences += 1

    return total_sequences, cleaned_sequences

def save_stats(stats_file, db_name, total, cleaned):
    file_exists = os.path.exists(stats_file)
    
    with open(stats_file, 'a') as stats:
        if not file_exists:
            stats.write("Database\tTheoretical Sequences\tObtained Sequences\n")
        stats.write(f"{db_name}\t{total}\t{cleaned}\n")

input_folder = os.path.expanduser("~/Desktop/Databases_analysis_diamond/Sequences_db")
output_folder = os.path.expanduser("~/Desktop/Databases_analysis_diamond/Cleaned_sequences_db")
stats_file = os.path.expanduser("~/Desktop/Databases_analysis_diamond/Cleaned_sequences_db/Cleaned_stats.tsv")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, filename)
    output_file_path = os.path.join(output_folder, f"{filename}.fasta")

    total_sequences, cleaned_sequences = clean_fasta_file(input_file_path, output_file_path)
    save_stats(stats_file, filename, total_sequences, cleaned_sequences)

   
print("Cleaning completed, results saved in 'Cleaned_sequences_db' subfolder. \n"
      f"The cleaning statistics file has been saved in the Cleaned_sequences_db subfolder as Cleaned_stats.tsv\n"
      f"(do not move this file as it is needed for calculating DAIRId and IDAIRId).")

if __name__ == "__main__":
    pass
