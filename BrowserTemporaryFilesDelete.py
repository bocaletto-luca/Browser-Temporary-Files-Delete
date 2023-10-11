# Software Name: Browser Temporary Files Delete
# Author: Luca Bocaletto
# Website: https://www.elektronoide.it
# License: GPLv3

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QMessageBox, QMenuBar, QAction, QDialog
from PyQt5 import QtCore
import getpass

# Definition of the AboutDialog class
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()   

        # Set the title of the dialog window
        self.setWindowTitle("About Browser Temporary Files Delete")
        self.setGeometry(200, 200, 300, 100)

        # Create a vertical layout for the dialog window
        layout = QVBoxLayout()

        # Add a QLabel with application information
        about_label = QLabel("Browser Temporary Files Delete - \n\nAuthor: Luca Bocaletto", self)
        layout.addWidget(about_label)

        # Set the layout for the dialog
        self.setLayout(layout)

# Definition of the main application class
class BrowserCacheCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__() 

        # Get the username of the currently logged-in user
        self.yourusername = getpass.getuser()

        # List of browser cache paths
        self.browsers = [
            {"name": "Google Chrome", "path": f"C:/Users/{self.yourusername}/AppData/Local/Google/Chrome/User Data/Default/Cache"},
            {"name": "Mozilla Firefox", "path": f"C:/Users/{self.yourusername}/AppData/Local/Mozilla/Firefox/Profiles/xxxxxxxx.default/cache2"},
            {"name": "Microsoft Edge", "path": f"C:/Users/{self.yourusername}/AppData/Local/Microsoft/Edge/User Data/Default/Cache"},
            {"name": "Opera", "path": f"C:/Users/{self.yourusername}/AppData/Roaming/Opera Software/Opera Stable/Cache"},
            {"name": "Safari", "path": f"C:/Users/{self.yourusername}/AppData/Local/Apple Computer/Safari/Cache"}
        ]

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        # Set the title of the window
        self.setWindowTitle("Browser Temporary Files Delete")
        self.setGeometry(100, 100, 400, 300)

        # Create a menu bar at the top
        menubar = self.menuBar()
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        menubar.addAction(about_action)

        # Create a central widget for the window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout to organize the user interface elements
        layout = QVBoxLayout()

        # Add a QLabel for the title
        title_label = QLabel("Browser Temporary Files Delete", central_widget)
        title_label.setAlignment(QtCore.Qt.AlignCenter)  # Center-align the text
        layout.addWidget(title_label)

        # Create a group of checkboxes to select browsers
        group_box = QGroupBox("Select Browsers to Clean", central_widget)
        group_layout = QVBoxLayout()

        self.checkboxes = []

        # Create checkboxes to select browsers
        for browser in self.browsers:
            checkbox = QCheckBox(browser["name"], self)
            self.checkboxes.append(checkbox)
            group_layout.addWidget(checkbox)

        group_box.setLayout(group_layout)

        layout.addWidget(group_box)

        # Label to display the result
        self.result_label = QLabel("", central_widget)
        layout.addWidget(self.result_label)

        # Button to start the scan
        scan_button = QPushButton("Start Scan", central_widget)
        scan_button.clicked.connect(self.scan_and_display)
        layout.addWidget(scan_button)

        # Button to delete files
        delete_button = QPushButton("Delete Files", central_widget)
        delete_button.clicked.connect(self.delete_files)
        layout.addWidget(delete_button)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

    # Function to show the "About" dialog
    def show_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    # Function to perform the scan and display the number of files found
    def scan_and_display(self):
        num_files_found = 0
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                browser = self.browsers[i]
                cache_path = browser["path"]
                num_files = self.count_files_in_directory(cache_path)
                num_files_found += num_files
        self.result_label.setText(f"Total number of files found: {num_files_found}")

    # Function to delete files
    def delete_files(self):
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                browser = self.browsers[i]
                cache_path = browser["path"]
                self.clean_browser_cache(cache_path, browser["name"])
        QMessageBox.information(self, "Deletion Completed", "File deletion completed.")

    # Function to count the files in a directory
    def count_files_in_directory(self, path):
        num_files = 0
        for root, dirs, files in os.walk(path):
            num_files += len(files)
        return num_files

    # Function to clean the cache of a browser
    def clean_browser_cache(self, path, browser_name):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Unable to delete {file_path}: {e}")
            print(f"Cache of {browser_name} has been cleaned.")
        except Exception as e:
            print(f"An error occurred while cleaning {browser_name} cache: {e}")

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrowserCacheCleanerApp()
    window.show()
    sys.exit(app.exec_())
