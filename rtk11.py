import filecmp
import os
import shutil
import signal
import sqlite3
import sys
import tempfile

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QLineEdit, QMainWindow, QStyledItemDelegate,
                             QTableWidget, QTableWidgetItem, QTabWidget,
                             QToolBar)

from binary_parser.binary_parser import BinaryParser
from constants import *


class ROTKXIGUI(QMainWindow):
    def init_menubar(self):
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu("&File")

        # Add "Open Database" action
        self.open_file_action = QAction("&Open Database", self)
        self.open_file_action.setShortcut("Ctrl+O")
        self.open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_file_action)

        # Add "Save Database" action
        self.save_file_action = QAction("&Save Database", self)
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.triggered.connect(self.save_file)
        self.save_file_action.setEnabled(False)
        self.file_menu.addAction(self.save_file_action)

        # Add "Save As Database" action
        self.save_as_file_action = QAction("Save &As Database", self)
        self.save_as_file_action.setShortcut("Ctrl+Shift+S")
        self.save_as_file_action.triggered.connect(self.save_as_file)
        self.save_as_file_action.setEnabled(False)
        self.file_menu.addAction(self.save_as_file_action)

        # Add "Exit" action
        self.exit_action = QAction("&Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

    def init_functions(self):
        self.filter_toolbar = QToolBar(self)
        self.filter_toolbar.setWindowTitle("Filter")
        self.addToolBar(self.filter_toolbar)

        self.search_box = QLineEdit()
        self.search_box.returnPressed.connect(self.filter_table)
        self.filter_toolbar.addWidget(self.search_box)

        self.filter_action = QAction("Filter", self)
        self.filter_action.triggered.connect(self.filter_table)
        self.filter_toolbar.addAction(self.filter_action)

    def __init__(self, testing=False):
        super().__init__()
        self.setWindowTitle("ROTK XI Editor")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(800, 600)

        self.init_functions()
        self.init_menubar()

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.table_widgets = []
        self.table_data = {}
        self.sorting_order = Qt.AscendingOrder

        self.new_scen_path = None

        self.open_file(testing)

    def init_cell(self, cell_data, colname):
        cell_item = QTableWidgetItem()
        if colname == "specialty":
            specialty_index = specialty_hex.index(cell_data)
            cell_data = specialty_options[specialty_index]
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        elif colname in col_map.keys():
            cell_data = col_map[colname][cell_data]
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        else:
            cell_data = str(cell_data)
            cell_item.setFlags(cell_item.flags() | Qt.ItemIsEditable)
        cell_item.setText(cell_data)
        return cell_item

    def init_table_widget(self, table_name, headers, data):
        table_widget = QTableWidget(self)
        table_widget.setObjectName(table_name)
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))
        table_widget.setSortingEnabled(True)

        header = table_widget.horizontalHeader()
        header.sectionClicked.connect(self.sort_table)
        header.setSectionsClickable(True)

        for row in range(len(data)):
            for col, colname in enumerate(headers):
                cell_item = self.init_cell(data[row][col], colname)
                table_widget.setItem(row, col, cell_item)

        self.tab_widget.addTab(table_widget, table_name)
        self.table_widgets.append(table_widget)

    def sort_table(self, logical_index):
        table_widget = self.table_widgets[-1]

        if self.sorting_order == Qt.AscendingOrder:
            self.sorting_order = Qt.DescendingOrder
        else:
            self.sorting_order = Qt.AscendingOrder

        table_widget.sortItems(logical_index, self.sorting_order)

        # Update sorting_order attribute
        self.sorting_order = table_widget.horizontalHeader().sortIndicatorOrder()

    def filter_table(self):
        search_text = self.search_box.text().lower()

        for table in self.table_widgets:
            table.setSortingEnabled(False)

            for row in range(table.rowCount()):
                match_found = False

                for col in range(table.columnCount()):
                    cell_text = table.item(row, col).text().lower()

                    if search_text in cell_text:
                        match_found = True
                        break

                table.setRowHidden(row, not match_found)

            table.setSortingEnabled(True)
            table.sortByColumn(0, self.sorting_order)

    def open_file(self, testing=False):
        """Opens a scenario file and parses the data into a database file for editing.
        """
        if testing:
            self.old_scen_path = 'scenario/SCEN000.S11'
        else:
            self.old_scen_path, _ = QFileDialog.getOpenFileName(
                self, "Open Scenario File", "", "Scenario Files (*.s11)")

            if not self.old_scen_path:
                return

        self.tab_widget.clear()

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
            if table_name == 'sqlite_sequence':
                continue
            # Retrieve the column names and data from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            headers = [x[0] for x in cursor.description]
            data = [list(x) for x in cursor.fetchall()]
            self.init_table_widget(table_name, headers, data)
            self.table_data[table_name] = data

        conn.close()
        self.save_file_action.setEnabled(True)
        self.save_as_file_action.setEnabled(True)

        if testing:
            self.save_file(testing)

    def save_file(self, testing=False):
        """
        Saves the current state of the database to the scenario file.
        Will first prompt for the path to save to if it doesn't exist yet
        """
        if testing:
            self.new_scen_path = 'scenario/SCEN009.S11'

        if not self.new_scen_path:
            self.save_as_file()
            return

        conn = sqlite3.connect(self.db_path)

        for table_widget in self.table_widgets:
            table_name = table_widget.objectName()
            table_data = self.table_data[table_name]
            headers = [
                table_widget.horizontalHeaderItem(col).text()
                for col in range(table_widget.columnCount())
            ]
            placeholders = ','.join(['?'] * len(headers))
            for row in table_data:
                conn.execute(
                    f"INSERT OR REPLACE INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})", row)

        conn.commit()
        conn.close()

        # This writes the data from the database back to the scenario file
        with BinaryParser('rtk11.lyt') as self.bp:
            self.bp.write_back(self.new_scen_path, self.db_path)

        if testing:
            assert filecmp.cmp(self.old_scen_path, self.new_scen_path)
            print("Assertion complete")
            print(f"{self.old_scen_path} is equal to {self.new_scen_path}")
            exit()

    def save_as_file(self):
        """
        Prompts the user for a scenario file before calling the regular save function.
        """
        self.new_scen_path, _ = QFileDialog.getSaveFileName(
            self, "Save Scenario File", "", "Scenario Files (*.s11)")

        if not self.new_scen_path:
            return

        if self.old_scen_path != self.new_scen_path:
            shutil.copyfile(self.old_scen_path, self.new_scen_path)

        self.save_file()


def main():
    app = QApplication(sys.argv)
    gui = ROTKXIGUI(True)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
