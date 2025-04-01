import os
import subprocess
import sys

print(" Starting diamond comparison...")

def run_diamond_analysis(db1_dmnd, db2_fasta, output_file):
    command = [
        "diamond", "blastp",
        "--db", db1_dmnd,
        "--query", db2_fasta,
        "--out", output_file,
        "--outfmt", "6",
        "qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", 
        "qstart", "qend", "sstart", "send", "evalue", "bitscore", 
        "qlen", "qseq", "stitle", "slen", "sseq",
        "--threads", "6",
        "--log",
        "--very-sensitive"
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Comparison completed for {db1_dmnd} vs {db2_fasta}. Results saved in {output_file}.")
        add_column_headers(output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error during analysis of {db1_dmnd} and {db2_fasta}: {e}")

def add_column_headers(output_file):
    headers = "qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\tqlen\tqseq\tstitle\tslen\tsseq"
    with open(output_file, 'r') as f:
        content = f.readlines()
    
    with open(output_file, 'w') as f:
        f.write(headers + "\n")
        f.writelines(content)
    print(f"Headers added to {output_file}.")

def compare_databases(db_folder, fasta_folder, output_folder, reference_db):
    fasta_files = [f for f in os.listdir(fasta_folder) if f.endswith(".fasta")]
    db_files = [f for f in os.listdir(db_folder) if f.endswith(".dmnd")]

    if reference_db.lower() == "all":
        for db1 in db_files:
            db1_dmnd = os.path.join(db_folder, db1)
            db1_name = os.path.splitext(db1)[0]
            for db2_fasta in fasta_files:
                db2_fasta_path = os.path.join(fasta_folder, db2_fasta)
                db2_name = os.path.splitext(db2_fasta)[0]
                output_folder_db = os.path.join(output_folder, db1_name)
                os.makedirs(output_folder_db, exist_ok=True)
                output_file = os.path.join(output_folder_db, f"{db1_name}_{db2_name}_diamond.tsv")
                run_diamond_analysis(db1_dmnd, db2_fasta_path, output_file)
    else:
        db1_dmnd = os.path.join(db_folder, f"{reference_db}.dmnd")
        if not os.path.exists(db1_dmnd):
            print(f"Reference database {reference_db}.dmnd not found.")
            return
        
        reference_folder = os.path.join(output_folder, reference_db)
        os.makedirs(reference_folder, exist_ok=True)

        for db2_fasta in fasta_files:
            db2_fasta_path = os.path.join(fasta_folder, db2_fasta)
            db2_name = os.path.splitext(db2_fasta)[0]
            output_file = os.path.join(reference_folder, f"{reference_db}_{db2_name}_diamond.tsv")
            run_diamond_analysis(db1_dmnd, db2_fasta_path, output_file)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_diamond_analysis.py <reference_db>")
        print("       <reference_db> can be 'all' or specific database name (without .dmnd extension)")
        sys.exit(1)
    
    reference_db = sys.argv[1]

    # Expand user paths and ensure they exist
    db_folder = os.path.expanduser('~/Desktop/Databases_analysis_diamond/DMND_files_db')
    fasta_folder = os.path.expanduser('~/Desktop/Databases_analysis_diamond/Cleaned_sequences_db')
    output_folder = os.path.expanduser('~/Desktop/Databases_analysis_diamond/Comparison_results')

    if not os.path.exists(db_folder):
        print(f"Error: Database folder {db_folder} does not exist!")
        sys.exit(1)
    if not os.path.exists(fasta_folder):
        print(f"Error: FASTA folder {fasta_folder} does not exist!")
        sys.exit(1)

    compare_databases(db_folder, fasta_folder, output_folder, reference_db)

    print("diamond comparison completed.")

if __name__ == "__main__":
    main()
