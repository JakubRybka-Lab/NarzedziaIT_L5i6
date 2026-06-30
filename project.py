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

if __name__ == "__main__":
    main()
