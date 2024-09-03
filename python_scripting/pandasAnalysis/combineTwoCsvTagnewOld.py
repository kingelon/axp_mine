import csv

def read_csv_to_set(csv_file):
    """
    Read a CSV file and return a set of tuples containing (groupid, artifactid, version).
    """
    dependencies_set = set()
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dependencies_set.add((row['groupid'], row['artifactid'], row['version']))
    return dependencies_set

def compare_and_tag_dependencies(old_csv, new_csv, output_csv):
    # Read the old and new dependencies
    old_dependencies = read_csv_to_set(old_csv)
    new_dependencies = read_csv_to_set(new_csv)
    
    # Prepare the combined list with tags
    combined_dependencies = []
    
    # Add old dependencies, tagging them as "old"
    for dep in old_dependencies:
        combined_dependencies.append({
            'groupid': dep[0],
            'artifactid': dep[1],
            'version': dep[2],
            'status': 'old'
        })
    
    # Add new dependencies, tagging them as "new" only if they are not in the old dependencies
    for dep in new_dependencies:
        if dep not in old_dependencies:
            combined_dependencies.append({
                'groupid': dep[0],
                'artifactid': dep[1],
                'version': dep[2],
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
