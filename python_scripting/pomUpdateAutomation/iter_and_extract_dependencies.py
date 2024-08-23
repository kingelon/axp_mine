import os
import xml.etree.ElementTree as ET
import csv
from glob import glob


# Function to remove namespace from XML tags
def remove_namespace(tree):
    for elem in tree.iter():
        if elem.tag.startswith('{'):
            elem.tag = elem.tag.split('}', 1)[1]


# Function to extract dependencies from a pom.xml file
def extract_dependencies_from_pom(pom_path):
    tree = ET.parse(pom_path)
    root = tree.getroot()

    remove_namespace(tree)

    dependencies = root.findall('.//dependency')

    csv_data = []

    for dependency in dependencies:
        group_id = dependency.find('groupId')
        artifact_id = dependency.find('artifactId')
        version = dependency.find('version')

        if group_id is not None and artifact_id is not None:
            csv_data.append({
                'groupId': group_id.text,
                'artifactId': artifact_id.text,
                'version': version.text if version is not None else 'N/A'
            })

    return csv_data


# Main function to process all poms in the folder
def process_poms_in_folder(input_folder, output_csv_path, output_txt_path):
    # Check if the input folder exists
    if not os.path.exists(input_folder):
        print(f"Input folder does not exist: {input_folder}")
        return

    print(f"Looking for pom.xml files in: {input_folder}")

    # Find all pom.xml files in the directory and subdirectories
    all_poms = glob(os.path.join(input_folder, '**', 'pom.xml'), recursive=True)

    if not all_poms:
        print(f"No pom.xml files found in {input_folder}")
        return

    combined_csv_data = []

    # Open the output txt file to list all pom.xml paths
    with open(output_txt_path, 'w') as txt_file:
        for pom_file in all_poms:
            print(f"Processing: {pom_file}")  # Debugging statement
            # Write the full path of the pom.xml file to the txt file
            txt_file.write(f"{os.path.abspath(pom_file)}\n")

            # Extract dependencies from the current pom.xml
            pom_data = extract_dependencies_from_pom(pom_file)
            combined_csv_data.extend(pom_data)

    # Write the combined data to the CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['groupId', 'artifactId', 'version']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in combined_csv_data:
            writer.writerow(row)


# Example usage
input_folder = r'C:\Users\vippa\OneDrive\Documents\git_KE\test_git_clones'  # Path to the folder containing multiple pom.xml files
output_csv_path = r'C:\Users\vippa\OneDrive\Documents\git_KE\axp_mine\python_scripting\data\output\dependencies.csv'  # Path to output CSV file
output_txt_path = r'C:\Users\vippa\OneDrive\Documents\git_KE\axp_mine\python_scripting\data\output\pom_paths.txt'  # Path to output text file with pom paths

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

process_poms_in_folder(input_folder, output_csv_path, output_txt_path)
