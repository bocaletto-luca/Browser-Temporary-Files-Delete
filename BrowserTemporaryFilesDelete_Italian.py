# Software Name: Browser Temporary Files Delete
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it
# License: GPLv3

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QMessageBox, QMenuBar, QAction, QDialog
from PyQt5 import QtCore
import getpass

# Definizione della classe per la finestra About
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Imposta il titolo della finestra di dialogo
        self.setWindowTitle("About Browser Temporary Files Delete")
        self.setGeometry(200, 200, 300, 100)

        # Crea un layout verticale per la finestra di dialogo
        layout = QVBoxLayout()

        # Aggiungi un QLabel con le informazioni sull'applicazione
        about_label = QLabel("Browser Temporary Files Delete - \n\nAuthor: Bocaletto Luca", self)
        layout.addWidget(about_label)

        # Imposta il layout per la finestra di dialogo
        self.setLayout(layout)

# Definizione della classe principale dell'applicazione
class BrowserCacheCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ottieni il nome utente dell'utente attualmente loggato
        self.yourusername = getpass.getuser()

        # Elenco dei percorsi delle cache dei browser
        self.browsers = [
            {"name": "Google Chrome", "path": f"C:/Users/{self.yourusername}/AppData/Local/Google/Chrome/User Data/Default/Cache"},
            {"name": "Mozilla Firefox", "path": f"C:/Users/{self.yourusername}/AppData/Local/Mozilla/Firefox/Profiles/xxxxxxxx.default/cache2"},
            {"name": "Microsoft Edge", "path": f"C:/Users/{self.yourusername}/AppData/Local/Microsoft/Edge/User Data/Default/Cache"},
            {"name": "Opera", "path": f"C:/Users/{self.yourusername}/AppData/Roaming/Opera Software/Opera Stable/Cache"},
            {"name": "Safari", "path": f"C:/Users/{self.yourusername}/AppData/Local/Apple Computer/Safari/Cache"}
        ]

        # Inizializza l'interfaccia utente
        self.initUI()

    def initUI(self):
        # Imposta il titolo della finestra
        self.setWindowTitle("Browser Temporary Files Delete")
        self.setGeometry(100, 100, 400, 300)

        # Crea una barra del menu in alto
        menubar = self.menuBar()
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        menubar.addAction(about_action)

        # Crea un widget centrale per la finestra
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crea un layout verticale per organizzare gli elementi dell'interfaccia utente
        layout = QVBoxLayout()

        # Aggiungi un QLabel per il titolo
        title_label = QLabel("Browser Temporary Files Delete", central_widget)
        title_label.setAlignment(QtCore.Qt.AlignCenter)  # Allinea il testo al centro
        layout.addWidget(title_label)

        # Crea un gruppo di caselle di controllo per selezionare i browser
        group_box = QGroupBox("Seleziona i Browser da pulire", central_widget)
        group_layout = QVBoxLayout()

        self.checkboxes = []

        # Crea caselle di controllo per selezionare i browser
        for browser in self.browsers:
            checkbox = QCheckBox(browser["name"], self)
            self.checkboxes.append(checkbox)
            group_layout.addWidget(checkbox)

        group_box.setLayout(group_layout)

        layout.addWidget(group_box)

        # Etichetta per visualizzare il risultato
        self.result_label = QLabel("", central_widget)
        layout.addWidget(self.result_label)

        # Pulsante per avviare la scansione
        scan_button = QPushButton("Avvia Scan", central_widget)
        scan_button.clicked.connect(self.scan_and_display)
        layout.addWidget(scan_button)

        # Pulsante per eliminare i file
        delete_button = QPushButton("Elimina File", central_widget)
        delete_button.clicked.connect(self.delete_files)
        layout.addWidget(delete_button)

        # Imposta il layout per il widget centrale
        central_widget.setLayout(layout)

    # Funzione per mostrare la finestra di dialogo "About"
    def show_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    # Funzione per eseguire la scansione e visualizzare il numero di file trovati
    def scan_and_display(self):
        num_files_found = 0
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                browser = self.browsers[i]
                cache_path = browser["path"]
                num_files = self.count_files_in_directory(cache_path)
                num_files_found += num_files
        self.result_label.setText(f"Numero totale di file trovati: {num_files_found}")

    # Funzione per eliminare i file
    def delete_files(self):
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                browser = self.browsers[i]
                cache_path = browser["path"]
                self.clean_browser_cache(cache_path, browser["name"])
        QMessageBox.information(self, "Eliminazione completata", "Eliminazione file completata.")

    # Funzione per contare i file in una directory
    def count_files_in_directory(self, path):
        num_files = 0
        for root, dirs, files in os.walk(path):
            num_files += len(files)
        return num_files

    # Funzione per pulire la cache di un browser
    def clean_browser_cache(self, path, browser_name):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Impossibile eliminare {file_path}: {e}")
            print(f"Cache di {browser_name} è stato pulito.")
        except Exception as e:
            print(f"Si è verificato un errore durante la pulizia {browser_name} cache: {e}")

# Punto di ingresso dell'applicazione
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrowserCacheCleanerApp()
    window.show()
    sys.exit(app.exec_())
