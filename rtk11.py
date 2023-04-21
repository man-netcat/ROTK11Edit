import os
import shutil
import sqlite3
import sys
from pathlib import Path

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

        open_file_action = QAction("&Open Database", self)
        open_file_action.setShortcut("Ctrl+O")
        open_file_action.triggered.connect(self.open_database)
        self.file_menu.addAction(open_file_action)

        save_file_action = QAction("&Save Database", self)
        save_file_action.setShortcut("Ctrl+S")
        save_file_action.triggered.connect(self.save_database)
        self.file_menu.addAction(save_file_action)

        self.tables = []

    def open_database(self):
        self.old_scen_path, _ = QFileDialog.getOpenFileName(
            self, "Open Scenario File", "", "Scenario Files (*.s11)")
        if not self.old_scen_path:
            return

        scenario_name = Path(self.old_scen_path).stem

        self.db_path = f'databases/{scenario_name}.db'
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

        # Create a table widget for each table in the database
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
            self.create_table_widget(headers, data, table_widget)

        conn.close()

    def save_database(self):
        self.new_scen_path, _ = QFileDialog.getSaveFileName(
            self, "Save Scenario File", "", "Scenario Files (*.s11)")
        if not self.new_scen_path:
            return

        shutil.copyfile(self.old_scen_path, self.new_scen_path)

        conn = sqlite3.connect(self.db_path)

        # Update the data in the database from the table widgets
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

    def create_table_widget(self, headers, data, table_widget):
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(headers)):
                item = QTableWidgetItem(str(data[i][j]))
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                table_widget.setItem(i, j, item)


def main():
    app = QApplication(sys.argv)
    gui = TableGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
