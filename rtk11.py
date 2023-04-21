import os
import shutil
import sqlite3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLineEdit,
                             QMainWindow, QTableWidget, QTableWidgetItem,
                             QTabWidget, QToolBar)

from binary_parser.binary_parser import BinaryParser
from constants import *


class TableGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROTK XI Editor")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(800, 600)

        filter_toolbar = QToolBar(self)
        filter_toolbar.setWindowTitle("Filter")
        self.addToolBar(filter_toolbar)

        self.search_box = QLineEdit()
        self.search_box.returnPressed.connect(self.filter_table)
        filter_toolbar.addWidget(self.search_box)

        filter_action = QAction("Filter", self)
        filter_action.triggered.connect(self.filter_table)
        filter_toolbar.addAction(filter_action)

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

        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        self.tables = []

        self.sorting_order = Qt.AscendingOrder

        self.open_database()

    def create_table_widget(self, headers, data, table_widget):
        table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))
        table_widget.setSortingEnabled(True)
        for i in range(len(data)):
            for j in range(len(headers)):
                cell_data = str(data[i][j])
                if cell_data.isnumeric():
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, float(cell_data))
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    table_widget.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(cell_data)
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    table_widget.setItem(i, j, item)

        self.tables.append(table_widget)

    def sort_table(self, logical_index):
        table_widget = self.tables[-1]

        if self.sorting_order == Qt.AscendingOrder:
            self.sorting_order = Qt.DescendingOrder
        else:
            self.sorting_order = Qt.AscendingOrder

        table_widget.sortItems(logical_index, self.sorting_order)

        # Update sorting_order attribute
        self.sorting_order = table_widget.horizontalHeader().sortIndicatorOrder()

    def filter_table(self):
        search_text = self.search_box.text().lower()

        for table in self.tables:
            table.setSortingEnabled(False)

            for i in range(table.rowCount()):
                match_found = False

                for j in range(table.columnCount()):
                    cell_text = table.item(i, j).text().lower()

                    if search_text in cell_text:
                        match_found = True
                        break

                table.setRowHidden(i, not match_found)

            table.setSortingEnabled(True)
            table.sortByColumn(0, self.sorting_order)

    def open_database(self):
        self.old_scen_path, _ = QFileDialog.getOpenFileName(
            self, "Open Scenario File", "", "Scenario Files (*.s11)")
        if not self.old_scen_path:
            return

        # Get the temporary folder path based on the operating system
        if os.name == 'posix':  # Linux/Mac
            tmp_folder = '/tmp'
        elif os.name == 'nt':  # Windows
            tmp_folder = os.environ['TEMP']
        else:
            raise OSError('Unsupported operating system')

        # Create a db file in the temporary folder
        self.db_path = os.path.join(tmp_folder, 'rtk11.db')
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
            if table_name == "sqlite_sequence":
                continue

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

        if not os.path.exists(self.new_scen_path):
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


def main():
    app = QApplication(sys.argv)
    gui = TableGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
