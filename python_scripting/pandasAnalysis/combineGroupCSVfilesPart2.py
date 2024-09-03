import csv

def read_csv_to_dict(csv_file):
    """
    Read a CSV file and return a dictionary with (groupid, artifactid) as keys and version as values.
    """
    dependencies_dict = {}
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['groupid'], row['artifactid'])
            dependencies_dict[key] = row['version']
    return dependencies_dict

def compare_and_tag_dependencies(old_csv, new_csv, output_csv):
    # Read the old and new dependencies
    old_dependencies = read_csv_to_dict(old_csv)
    new_dependencies = read_csv_to_dict(new_csv)
    
    # Prepare the combined list with tags
    combined_dependencies = []
    
    # Add old dependencies, tagging them as "old"
    for key, version in old_dependencies.items():
        combined_dependencies.append({
            'groupid': key[0],
            'artifactid': key[1],
            'version': version,
            'status': 'old'
        })
    
    # Add new dependencies, tagging them as "new" only if they are not in the old dependencies
    for key, version in new_dependencies.items():
        if key not in old_dependencies:
            combined_dependencies.append({
                'groupid': key[0],
                'artifactid': key[1],
                'version': version,
                'status': 'new'
            })
    
    # Write the combined dependencies to the output CSV
    with open(output_csv, mode='w', newline='') as file:
        fieldnames = ['groupid', 'artifactid', 'version', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for dep in combined_dependencies:
            writer.writerow(dep)

# Example usage
old_csv = 'path/to/old_dependencies.csv'  # Replace with the path to your old dependencies CSV
new_csv = 'path/to/new_dependencies.csv'  # Replace with the path to your new dependencies CSV
output_csv = 'path/to/combined_dependencies.csv'  # Replace with the desired output CSV path

compare_and_tag_dependencies(old_csv, new_csv, output_csv)
