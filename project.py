import json
import xml.etree.ElementTree as ET
import yaml

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Błąd składni JSON w pliku {path}: {e}")
        return None
    except Exception as e:
        print(f"Błąd odczytu pliku JSON: {e}")
        return None

def save_json(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Błąd zapisu do pliku JSON: {e}")
        return False

def load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Błąd odczytu pliku YAML: {e}")
        return None

def save_yaml(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)
        return True
    except Exception as e:
        print(f"Błąd zapisu do pliku YAML: {e}")
        return False

def load_xml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        return root
    except Exception as e:
        print(f"Błąd odczytu pliku XML: {e}")
        return None

def save_xml(root, path):
    try:
        tree = ET.ElementTree(root)
        tree.write(path, encoding='utf-8', xml_declaration=True)
        return True
    except Exception as e:
        print(f"Błąd zapisu do pliku XML: {e}")
        return False

if __name__ == "__main__":
    print("Program uruchomiony poprawnie.")
