import json
import os
import xml.etree.ElementTree as ET
# Could be used beautifulsoup + lxml for more convenient xml processing

def get_connection_info():
    with open('connection_info.json', 'r', encoding='utf-8') as f:
        connection_dict = json.load(f)
    if not (connection_dict.get('host') and connection_dict.get('user')):
        print("Please make sure you have your connection info in connection_info.json file!")
    return connection_dict

def get_students_file_path():
    print(f"Students path: {os.path.abspath('data/students.json')}")

def get_rooms_file_path():
    print(f"Rooms path: {os.path.abspath('data/rooms.json')}")

def upload_json():
    with open('data/students.json', 'r') as s:
        students_data = json.load(s)
    print("Uploaded student information from json files.")
    with open('data/rooms.json', 'r') as s:
        rooms_data = json.load(s)
    print("Uploaded room information from json files.")
    return rooms_data, students_data

def export_to_json(rows, output_file):
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(list(rows), f, indent=4, default=str)
        # Alternative: load only one row into mem to use less memory

def export_to_xml(rows : dict, root : str, item : str, output_file : str):
    root_el = ET.Element(root)
    tree = ET.ElementTree(root_el)
    for row in rows:
        item_el = ET.SubElement(root_el, item)
        for key, value in row.items():
            child = ET.SubElement(item_el, str(key))
            child.text = str(value) if value else ""
    ET.indent(tree,'    ', level =0)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)