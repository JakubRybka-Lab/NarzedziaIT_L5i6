import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Błąd składni JSON w pliku {path}: {e}")
        sys.exit(1)

def save_json(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Błąd zapisu do pliku JSON: {e}")
        sys.exit(1)

def load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data is None:
                raise ValueError("Plik YAML jest pusty.")
            return data
    except yaml.YAMLError as e:
        print(f"Błąd składni YAML w pliku {path}: {e}")
        sys.exit(1)

def save_yaml(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)
    except Exception as e:
        print(f"Błąd zapisu do pliku YAML: {e}")
        sys.exit(1)

def xml_to_dict(element):
    subdict = {}
    for child in element:
        if len(child) > 0:
            subdict[child.tag] = xml_to_dict(child)
        else:
            subdict[child.tag] = child.text
    return subdict if subdict else element.text

def load_xml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        return {root.tag: xml_to_dict(root)}
    except ET.ParseError as e:
        print(f"Błąd składni XML w pliku {path}: {e}")
        sys.exit(1)

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    if isinstance(d, dict):
        for key, val in d.items():
            child = dict_to_xml(key, val)
            elem.append(child)
    else:
        elem.text = str(d)
    return elem

def save_xml(data, path):
    try:
        root_tag = list(data.keys())[0]
        root_element = dict_to_xml(root_tag, data[root_tag])
        tree = ET.ElementTree(root_element)
        ET.indent(tree, space="    ", level=0)
        tree.write(path, encoding='utf-8', xml_declaration=True)
    except Exception as e:S
        print(f"Błąd zapisu do pliku XML: {e}")
        sys.exit(1)

def convert_data(input_path, output_path):
    ext_in = os.path.splitext(input_path)[1].lower()
    ext_out = os.path.splitext(output_path)[1].lower()

    if ext_in == '.json': data = load_json(input_path)
    elif ext_in in ['.yml', '.yaml']: data = load_yaml(input_path)
    elif ext_in == '.xml': data = load_xml(input_path)

    if ext_out == '.json': save_json(data, output_path)
    elif ext_out in ['.yml', '.yaml']: save_yaml(data, output_path)
    elif ext_out == '.xml': save_xml(data, output_path)

def main():
    if len(sys.argv) != 3:
        print("Błąd: Niepoprawna liczba argumentów!")
        print("Użycie: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"Błąd: Plik '{input_path}' nie istnieje.")
        sys.exit(1)

    allowed = ['.json', '.yml', '.yaml', '.xml']
    ext_in = os.path.splitext(input_path)[1].lower()
    ext_out = os.path.splitext(output_path)[1].lower()

    if ext_in not in allowed or ext_out not in allowed:
        print(f"Błąd: Niedozwolony format pliku. Obsługiwane: {allowed}")
        sys.exit(1)

    print(f"Konwersja z {ext_in} do {ext_out}...")
convert_data(input_path, output_path)
 print("Sukces! Konwersja zakończona powodzeniem.")

if __name__ == "__main__":
    main()
