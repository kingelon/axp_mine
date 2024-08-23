import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

# Define the input CSV file path
input_csv_path = r'C:\Users\vippa\OneDrive\Documents\git_KE\axp_mine\python_scripting\data\output\output_groupedfile.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(input_csv_path)

# Create the root element 'dependencyManagement'
dependency_management = Element('dependencyManagement')

# Create the 'dependencies' sub-element
dependencies = SubElement(dependency_management, 'dependencies')

# Iterate over the DataFrame rows to create 'dependency' elements
for _, row in df.iterrows():
    # Create a 'dependency' element for each row
    dependency = SubElement(dependencies, 'dependency')

    # Create 'groupId', 'artifactId', and 'version' sub-elements
    group_id = SubElement(dependency, 'groupId')
    group_id.text = row['groupId']

    artifact_id = SubElement(dependency, 'artifactId')
    artifact_id.text = row['artifactId']

    version = SubElement(dependency, 'version')
    version.text = row['version']

# Convert the XML structure to a string and prettify it
xml_str = tostring(dependency_management, 'utf-8')
pretty_xml_str = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="   ")

# Print the generated XML
print(pretty_xml_str)

# Optionally, save the XML to a file
output_xml_path = r'C:\Users\vippa\OneDrive\Documents\git_KE\axp_mine\python_scripting\data\output\output_bom1.xml'
with open(output_xml_path, 'w') as f:
    f.write(pretty_xml_str)
