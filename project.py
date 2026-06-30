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
class ConversionWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, in_p, out_p):
        super().__init__()
        self.in_p = in_p
        self.out_p = out_p

    def run(self):
        try:
            convert_data(self.in_p, self.out_p)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class ConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter plików - Task 8")
        self.setGeometry(100, 100, 400, 200)
        self.input_file = ""
        self.output_file = ""

        self.label_in = QLabel("Nie wybrano pliku wejściowego", self)
        self.btn_in = QPushButton("Wybierz plik wejściowy", self)
        self.btn_in.clicked.connect(self.select_in)

        self.label_out = QLabel("Nie wybrano pliku wyjściowego", self)
        self.btn_out = QPushButton("Wybierz plik docelowy", self)
        self.btn_out.clicked.connect(self.select_out)

        self.btn_run = QPushButton("Konwertuj", self)
        self.btn_run.clicked.connect(self.run_conversion)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_in)
        layout.addWidget(self.label_in)
        layout.addWidget(self.btn_out)
        layout.addWidget(self.label_out)
        layout.addWidget(self.btn_run)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_in(self):
        file, _ = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "Formaty (*.json *.yml *.yaml *.xml)")
        if file:
            self.input_file = file
            self.label_in.setText(os.path.basename(file))

    def select_out(self):
        file, _ = QFileDialog.getSaveFileName(self, "Zapisz jako", "", "JSON (*.json);;YAML (*.yml);;XML (*.xml)")
        if file:
            self.output_file = file
            self.label_out.setText(os.path.basename(file))
def run_conversion(self):
        if not self.input_file or not self.output_file:
            QMessageBox.warning(self, "Błąd", "Wybierz oba pliki!")
            return

        self.btn_run.setEnabled(False)
        self.btn_run.setText("Konwertowanie...")

        self.worker = ConversionWorker(self.input_file, self.output_file)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self):
        self.btn_run.setEnabled(True)
        self.btn_run.setText("Konwertuj")
        QMessageBox.information(self, "Sukces", "Konwersja asynchroniczna zakończona sukcesem!")

    def on_error(self, err):
        self.btn_run.setEnabled(True)
        self.btn_run.setText("Konwertuj")
        QMessageBox.critical(self, "Błąd", f"Błąd w tle: {err}")

def main():
    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        if not os.path.exists(input_path):
            print("Błąd: Plik wejściowy nie istnieje.")
            sys.exit(1)
        convert_data(input_path, output_path)
        print("Sukces! Konwersja zakończona powodzeniem.")
    elif len(sys.argv) == 1:
        app = QApplication(sys.argv)
        window = ConverterApp()
        window.show()
        sys.exit(app.exec())
    else:
        print("Błąd: Niepoprawna liczba argumentów!")
        print("Użycie: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

if __name__ == "__main__":
    main()
