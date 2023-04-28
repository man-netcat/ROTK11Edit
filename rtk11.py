import filecmp
import os
import shutil
import signal
import sqlite3
import sys
import tempfile
from pprint import pprint

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QInputDialog, QLineEdit, QMainWindow,
                             QStyledItemDelegate, QTableWidget,
                             QTableWidgetItem, QTabWidget, QToolBar)

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

        self.table_widgets: list[QTableWidget] = []
        self.table_data = {}
        self.sorting_order = Qt.AscendingOrder

        self.new_scen_path = None
        self.is_initialized = False

        self.open_file(testing)

    def init_cell(self, cell_data, column_name):
        cell_item = QTableWidgetItem()
        if column_name == "specialty":
            specialty_index = specialty_hex.index(cell_data)
            cell_text = specialty_options[specialty_index]
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        elif column_name in col_map:
            cell_text = col_map[column_name][cell_data]
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        else:
            cell_text = str(cell_data)
            cell_item.setFlags(cell_item.flags() | Qt.ItemIsEditable)
        cell_item.setText(cell_text)
        return cell_item

    def init_table_widget(self, table_name, headers, data):
        table_widget = QTableWidget(self)
        table_widget.setObjectName(table_name)
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))
        table_widget.setSortingEnabled(True)
        table_widget.cellDoubleClicked.connect(self.choose_option)
        table_widget.itemChanged.connect(self.cell_changed)

        header = table_widget.horizontalHeader()
        header.sectionClicked.connect(self.sort_table)
        header.setSectionsClickable(True)

        for row in range(len(data)):
            for col, column_name in enumerate(headers):
                if column_name == 'id' or self.datatypes[table_name][column_name]['type'] == 'int':
                    cell_data = int(data[row][col])
                elif self.datatypes[table_name][column_name]['type'] == 'str':
                    # Replace null bytes
                    cell_data = str(data[row][col].replace('\x00', ''))
                cell_item = self.init_cell(cell_data, column_name)
                table_widget.setItem(row, col, cell_item)

        self.tab_widget.addTab(table_widget, table_name)
        self.table_widgets.append(table_widget)

    def cell_changed(self, item):
        if not self.is_initialized:
            return
        row = item.row()
        col = item.column()
        table_widget = item.tableWidget()
        table_name = table_widget.objectName()
        column_name = table_widget.horizontalHeaderItem(col).text()
        cell_data = item.text()
        print(
            f"Cell ({row}, {col}) in {table_name} with column name {column_name} was modified with new value {cell_data}")

        def reverse(d): return {v: k for k, v in d.items()}
        if column_name == 'specialty':
            pass
        elif column_name in col_map:
            cell_data = reverse(col_map[column_name])[cell_data]
        elif column_name == 'id' or self.datatypes[table_name][column_name]['type'] == 'int':
            cell_data = int(cell_data)

        self.table_data[table_name][row][col] = cell_data

    def choose_option(self, row, col):
        current_tab = self.tab_widget.currentIndex()
        current_table = self.table_widgets[current_tab]
        cell_item = current_table.item(row, col)
        column_name = current_table.horizontalHeaderItem(col).text()

        if column_name == 'specialty':
            options = specialty_options.values()
        elif column_name in col_map:
            options = col_map[column_name].values()
        else:
            return

        combo_box = QComboBox()
        combo_box.addItems(options)
        combo_box.setEditText(cell_item.text())
        combo_box.setInsertPolicy(QComboBox.NoInsert)

        current_text = cell_item.text()
        current_index = list(options).index(current_text)
        item, ok = QInputDialog.getItem(
            self, "Choose option", "Select an option:", options, current=current_index)

        if ok and item:
            cell_item.setText(item)

    def sort_table(self, logical_index):
        table_widget = self.table_widgets[-1]
        self.sorting_order = Qt.DescendingOrder if self.sorting_order == Qt.AscendingOrder else Qt.AscendingOrder
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
        with BinaryParser('rtk11.lyt', encoding='shift-jis') as bp:
            bp.parse_file(self.old_scen_path, self.db_path)
            self.datatypes = {
                tablename: {
                    column[0]: {
                        'type': column[1],
                        'size': column[2]
                    }
                    for section in tabledata['sections']
                    for column in section['data']
                }
                for tablename, tabledata in bp.data.items()
            }

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
        self.is_initialized = True

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
        with BinaryParser('rtk11.lyt', encoding='shift-jis') as bp:
            bp.write_back(self.new_scen_path, self.db_path)

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
    gui = ROTKXIGUI(False)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
