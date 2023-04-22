import os
import shutil
import sqlite3
import sys
import tempfile

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
                             QTableWidget, QTableWidgetItem, QTabWidget)

from binary_parser.binary_parser import BinaryParser
from constants import *


class TableGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROTK XI Editor")
        self.setWindowIcon(QIcon("icon.png"))

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu("&File")

        # Add "Open Database" action
        self.open_file_action = QAction("&Open Database", self)
        self.open_file_action.setShortcut("Ctrl+O")
        self.open_file_action.triggered.connect(self.open_database)
        self.file_menu.addAction(self.open_file_action)

        # Add "Save Database" action
        self.save_file_action = QAction("&Save Database", self)
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.triggered.connect(self.save_database)
        self.save_file_action.setEnabled(False)
        self.file_menu.addAction(self.save_file_action)

        # Add "Save As Database" action
        self.save_as_file_action = QAction("Save &As Database", self)
        self.save_as_file_action.setShortcut("Ctrl+Shift+S")
        self.save_as_file_action.triggered.connect(self.save_as_database)
        self.save_as_file_action.setEnabled(False)
        self.file_menu.addAction(self.save_as_file_action)

        # Add "Exit" action
        self.exit_action = QAction("&Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        self.tables = []
        self.new_scen_path = None

    def open_database(self):
        """Opens a scenario file and parses the data into a database file for editing.
        """
        self.old_scen_path, _ = QFileDialog.getOpenFileName(
            self, "Open Scenario File", "", "Scenario Files (*.s11)")

        if not self.old_scen_path:
            return

        self.db_path = os.path.join(tempfile.gettempdir(), 'rtk11.db')

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        # This reads the data from the scenario file into the database
        with BinaryParser('rtk11.lyt') as self.bp:
            self.bp.parse_file(self.old_scen_path, self.db_path)

        conn = sqlite3.connect(self.db_path)

        # Retrieve the tables in the database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [x[0] for x in cursor.fetchall()]

        for table_name in table_names:
            table_widget = QTableWidget(self)
            table_widget.setObjectName(table_name)
            self.tab_widget.addTab(table_widget, table_name)
            self.tables.append(table_widget)

            # Retrieve the column names and data from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            headers = [x[0] for x in cursor.description]
            data = cursor.fetchall()

            # Populate the table widget with the data
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(data))
            for i in range(len(data)):
                for j in range(len(headers)):
                    item = QTableWidgetItem(str(data[i][j]))
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    table_widget.setItem(i, j, item)

        conn.close()
        self.save_file_action.setEnabled(True)
        self.save_as_file_action.setEnabled(True)

    def save_database(self):
        """
        Saves the current state of the database to the scenario file.
        Will first prompt for the path to save to if it doesn't exist yet
        """
        if not self.new_scen_path:
            self.save_as_database()
            return

        conn = sqlite3.connect(self.db_path)

        for table_widget in self.tables:
            table_name = table_widget.objectName()
            headers = [table_widget.horizontalHeaderItem(
                i).text() for i in range(table_widget.columnCount())]
            for i in range(table_widget.rowCount()):
                row = [table_widget.item(i, j).text()
                       for j in range(table_widget.columnCount())]
                placeholders = ','.join(['?'] * len(row))
                values = tuple(row)
                conn.execute(
                    f"INSERT OR REPLACE INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})", values)

        conn.commit()
        conn.close()

        # This writes the data from the database back to the scenario file
        with BinaryParser('rtk11.lyt') as self.bp:
            self.bp.write_back(self.new_scen_path, self.db_path)

    def save_as_database(self):
        """
        Prompts the user for a scenario file before calling the regular save function.
        """
        self.new_scen_path, _ = QFileDialog.getSaveFileName(
            self, "Save Scenario File", "", "Scenario Files (*.s11)")

        if not self.new_scen_path:
            return

        shutil.copyfile(self.old_scen_path, self.new_scen_path)
        self.save_database()


def main():
    app = QApplication(sys.argv)
    gui = TableGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
