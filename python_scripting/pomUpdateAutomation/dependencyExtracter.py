import xml.etree.ElementTree as ET
import csv
import os

def remove_namespace(tree):
    for elem in tree.iter():
        if elem.tag.startswith('{'):
            elem.tag = elem.tag.split('}', 1)[1]

def extract_dependencies(input_pom_path, output_csv_path):
    tree = ET.parse(input_pom_path)
    root = tree.getroot()

    remove_namespace(tree)

    dependencies = root.findall('.//dependency')

    # Prepare the CSV data
    csv_data = []

    for dependency in dependencies:
        group_id = dependency.find('groupId')
        artifact_id = dependency.find('artifactId')
        version = dependency.find('version')

        # Ignore exclusions inside the dependency element
        if group_id is not None and artifact_id is not None:
            csv_data.append({
                'groupId': group_id.text,
                'artifactId': artifact_id.text,
                'version': version.text if version is not None else 'N/A'
            })

    # Write CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['groupId', 'artifactId', 'version']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)

# Example usage
input_pom_path = '../data/input/pom.xml'
output_csv_path = '../data/output/dependencies.csv'

extract_dependencies(input_pom_path, output_csv_path)
