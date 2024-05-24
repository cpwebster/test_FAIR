# This script will take a specified directory, which contains multiple nexus files,
# and construct a partitioned nexus file, where each partition is named as the
# first part of the individual nexus file names. For example, if an individual
# nexus file is named "LOC105032131.min4.nexus", the partition name will be
# "LOC105032131".

# USAGE:
# python create_master_nexus.py /path/to/nexus/files output_master_nexus_name.nexus

import os
import argparse

def create_and_manipulate_master_nexus(directory, output_file):
    nexus_files = [file for file in os.listdir(directory) if file.endswith('.nexus')]

    if not nexus_files:
        print("No Nexus files found in the specified directory.")
        return

    # Choose the first Nexus file as the source
    source_nexus_file = os.path.join(directory, nexus_files[0])

    # Read the content of the source Nexus file
    with open(source_nexus_file, 'r') as source_file:
        nexus_content = source_file.read()

    # Create the master Nexus file
    master_nexus_content = nexus_content + "\n\nBEGIN BLOCKS;\n"
    # Extract the partition name from the original file name
    partition_name = nexus_files[0].split('.')[0]

    # Extract the sequence data lines and count the number of characters for each taxon
    sequence_lines = nexus_content.split('\n')[4:-2]  # Exclude the header and "END;" lines
    taxon_ranges = []
    current_char_count = 1

    for line in sequence_lines:
        line = line.strip()
        if line == '':
            continue
        # Check if the line starts with a valid taxon name
        if line[0] != ' ':
            # Extract taxon name and reset sequence for a new taxon
            taxon_name = line.split()[0]
            sequence = ''
        else:
            # Concatenate sequence lines for the current taxon
            sequence += line

        # Calculate the number of characters for each taxon
        num_characters = len(sequence)
        taxon_range = f"{current_char_count}-{current_char_count + num_characters - 1}"
        taxon_ranges.append((taxon_name, taxon_range))
        current_char_count += num_characters

    # Add charset information to the master Nexus file
    for taxon_name, taxon_range in taxon_ranges:
        charset_line = f"\tcharset {taxon_name} = {taxon_range};"
        master_nexus_content += f"{charset_line}\n"

    master_nexus_content += "end;\n"

    # Save the master Nexus file
    master_file_path = os.path.join(directory, output_file)
    with open(master_file_path, 'w') as master_file:
        master_file.write(master_nexus_content)

    print(f"Master Nexus file created: {master_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create and manipulate a master Nexus file.")
    parser.add_argument("directory", help="Path to the directory containing Nexus files.")
    parser.add_argument("output_file", help="Name of the output master Nexus file.")
    args = parser.parse_args()

    create_and_manipulate_master_nexus(args.directory, args.output_file)






