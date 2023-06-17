import os
import shutil
import signal
import sys
import tempfile
from functools import reduce
from sqlite3 import connect

import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from binary_parser import BinaryParser
from constants import *
from enums import *


class Unimplemented(Exception):
    pass


def clean(str: str):
    # TODO: Check if values in DB are correctly overwritten
    return str.replace("\x00", "").strip()


class ROTKXIGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROTK XI Editor")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(800, 600)

        self.init_functions()
        self.init_menubar()

        # Create a toolbar
        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)

        # Create a spacer to push the button to the right side
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Create a button to toggle the visibility of the dynamic widget
        self.toggle_button = QPushButton("Hide/Show", self)
        self.toggle_button.setMaximumWidth(100)
        self.toggle_button.clicked.connect(self.toggle_dynamic_widget)

        # Add the spacer and button to the toolbar
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.toggle_button)

        # Create a splitter widget
        self.splitter = QSplitter(Qt.Horizontal, self)

        # Add the tab widget to the splitter
        self.tab_widget = QTabWidget(self)
        self.splitter.addWidget(self.tab_widget)

        # Add an empty widget to the splitter
        self.dynamic_widget = QWidget(self)
        self.dynamic_layout = QVBoxLayout(self.dynamic_widget)
        self.splitter.addWidget(self.dynamic_widget)
        self.dynamic_widget.hide()

        # Set the splitter as the central widget
        self.setCentralWidget(self.splitter)

        self.table_widgets = []
        self.table_datas = {}
        self.sorting_order = Qt.AscendingOrder

        self.new_scen_path = None
        self.is_initialized = False
        self.selection_made = pyqtSignal(int)

        self.open_file()

        self.showMaximized()

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

        # Add "View" menu
        self.view_menu = self.menubar.addMenu("&View")

        # Add "Theme" action
        self.theme_action = QAction("&Theme", self)
        self.theme_action.triggered.connect(self.select_theme)
        self.view_menu.addAction(self.theme_action)

        # Add "Help" menu
        self.help_menu = self.menubar.addMenu("&Help")

        # Add "About" action
        self.about_action = QAction("&About", self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

    def toggle_dynamic_widget(self):
        if self.dynamic_widget.isVisible():
            self.dynamic_widget.hide()
        else:
            self.dynamic_widget.show()

    def switch_dynamic_layout(self, layout):
        # Clear the existing layout of the dynamic widget
        while self.dynamic_layout.count():
            item = self.dynamic_layout.takeAt(0)
            if isinstance(item, QWidgetItem):
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
            elif isinstance(item, QLayoutItem):
                sub_layout = item.layout()
                while sub_layout.count():
                    sub_item = sub_layout.takeAt(0)
                    widget = sub_item.widget()
                    if widget is not None:
                        widget.setParent(None)
                        widget.deleteLater()

        # Add the provided layout to the dynamic widget's layout
        self.dynamic_layout.addLayout(layout)

        # Show the dynamic widget
        self.dynamic_widget.show()

    def select_theme(self):
        def set_light_theme():
            self.setStyleSheet(qdarkstyle.load_stylesheet(
                qt_api="pyqt5", palette=qdarkstyle.LightPalette))
            self.update()

        def set_dark_theme():
            self.setStyleSheet(qdarkstyle.load_stylesheet(
                qt_api="pyqt5", palette=qdarkstyle.DarkPalette))
            self.update()

        # Create buttons for theme selection
        light_button = QPushButton("Light Theme")
        light_button.clicked.connect(set_light_theme)

        dark_button = QPushButton("Dark Theme")
        dark_button.clicked.connect(set_dark_theme)

        # Create layout and add buttons
        layout = QHBoxLayout()
        layout.addWidget(light_button)
        layout.addWidget(dark_button)

        self.switch_dynamic_layout(layout)

    def show_about(self):
        about_text = "Available at https://github.com/rickt1998/rtk11edit"
        text_edit = QTextEdit()
        text_edit.setPlainText(about_text)

        # Add the QTextEdit to the layout of the dynamic widget
        layout = QVBoxLayout()
        layout.addWidget(text_edit)

        self.switch_dynamic_layout(layout)

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

    def init_cell(self, cell_data: int | str, table_name: str, col_name: str) -> QTableWidgetItem:
        """Initialises the contents of a cell item based on its column.
        """
        cell_item = QTableWidgetItem()
        cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        if col_name == "id":
            cell_text = int(cell_data)
        elif col_name == "colour":
            color = QColor(colour_map.get(cell_data))
            cell_text = cell_data
            cell_item.setBackground(QBrush(color))
        elif col_name == "specialty":
            cell_text = self.get_specialty_text_from_value(cell_data)
        elif col_name in ["alliance", "research", "goal", "target", "specifictarget"]:
            cell_text = "Edit"
        elif col_name in ["allegiance", "district"]:
            cell_text = self.get_district_ruler_by_district_id(cell_data)
        elif col_name == "force":
            cell_text = self.get_force_ruler_name_by_force_id(cell_data)
        elif col_name in officer_columns:
            cell_text = self.get_officer_name_by_id(cell_data)
        elif col_name == "country":
            cell_text = self.get_country_name_by_id(cell_data)
        elif col_name in col_map:
            cell_text = col_map[col_name].get(cell_data, "None")
        elif self.datatypes[table_name][col_name] == "int":
            cell_text = int(cell_data)
            cell_item.setFlags(cell_item.flags() | Qt.ItemIsEditable)
        elif self.datatypes[table_name][col_name] == "str":
            cell_text = clean(cell_data)
            cell_item.setTextAlignment(Qt.TextWrapAnywhere | Qt.AlignVCenter)
            cell_item.setTextAlignment(Qt.AlignVCenter)
            cell_item.setFlags(cell_item.flags() | Qt.ItemIsEditable)

        cell_item.setData(Qt.DisplayRole, cell_text)
        return cell_item

    def init_table_widget(self, table_name: str):
        """Initialises a table widget with the data read from the file.
        """
        col_names = self.table_datas[table_name]["col_names"]
        num_rows = self.table_datas[table_name]["num_rows"]

        table_widget = QTableWidget(self)
        table_widget.setObjectName(table_name)
        table_widget.setColumnCount(len(col_names))
        table_widget.setHorizontalHeaderLabels(col_names)
        table_widget.setRowCount(num_rows)
        table_widget.setSortingEnabled(True)
        table_widget.cellDoubleClicked.connect(self.on_cell_selected)
        table_widget.itemChanged.connect(self.on_cell_update)
        table_widget.keyPressEvent = self.on_key_pressed

        header = table_widget.horizontalHeader()
        header.sectionClicked.connect(self.sort_table)
        header.setSectionsClickable(True)

        for row_idx in range(num_rows):
            for col_idx, col_name in enumerate(col_names):
                cell_data = self.get_table_data(table_name, row_idx, col_idx)
                cell_item = self.init_cell(cell_data, table_name, col_name)
                table_widget.setItem(row_idx, col_idx, cell_item)

        for col_idx, col_name in enumerate(col_names):
            if any([substr in col_name for substr in ["relationship", "ingame", "ownerorcity"]]):
                table_widget.setColumnHidden(col_idx, True)

        self.tab_widget.addTab(table_widget, table_name)
        self.table_widgets.append(table_widget)

    def set_table_data(self, table_name: str, row_idx: int, col_idx: int, cell_data: str | int):
        """Sets the data of the internal table.
        """
        if self.is_initialized:
            print("SET", (table_name, row_idx, col_idx, cell_data))
        self.table_datas[table_name]["data"][row_idx][col_idx] = cell_data

    def get_table_data(self, table_name: str, row_idx: int, col_idx: int) -> str | int:
        """Retrieves data from the internal table.
        """
        table_data = self.table_datas[table_name]["data"][row_idx][col_idx]
        # if self.is_initialized:
        #     print("GET", (table_name, row_idx, col_idx, table_data))
        return table_data

    def get_num_rows(self, table_name):
        return self.table_datas[table_name]["num_rows"]

    def officer_names(self) -> list[str]:
        """Returns an up-to-date list of all officer names (family + given names).
        """
        return [self.get_officer_name_by_id(officer_id) for officer_id in range(self.get_num_rows("officer"))]

    def country_names(self) -> list[str]:
        """Returns an up-to-date list of all country names
        """
        return [self.get_country_name_by_id(country_id) for country_id in range(self.get_num_rows("country"))]

    def get_specialty_text_from_value(self, value: int) -> str:
        """Parses the specialty text given a city specialty value.
        """
        specialty_idx = specialty_hex.index(value)
        return specialty_options[specialty_idx]

    def get_specialty_value_from_text(self, text: str) -> int:
        """Returns the specialty value given its description.
        """
        return specialty_options.getr(text)

    def get_force_ruler_name_by_force_id(self, force_id: int) -> str:
        """Return the name of the force ruler given a force id.
        """
        if force_id == 0xFF:
            return "None"
        elif force_id >= self.get_num_rows("force"):
            return tribes[force_id]
        ruler_id = self.get_values_by_enum(Force.FORCERULER)[force_id]
        return self.get_officer_name_by_id(ruler_id)

    def get_force_id_by_force_ruler_name(self, ruler_name: str) -> int:
        """Returns the force id given its ruler"s name.
        """
        if ruler_name == "None":
            return 0xFF
        officer_id = self.officer_names().index(ruler_name)
        return self.get_values_by_enum(Force.FORCERULER).index(officer_id)

    def get_district_ruler_by_district_id(self, district_id: int) -> str:
        """Return the name of the district ruler given its district id.
        """
        if district_id == 0xFF:
            return "None"
        elif district_id >= self.get_num_rows("force"):
            return tribes[district_id]
        ruler_id = self.get_table_data(
            "district", district_id, District.DISTRICTRULER)
        return self.get_officer_name_by_id(ruler_id)

    def get_district_id_by_district_ruler_name(self, ruler_name: str) -> str:
        """Return the index of the district given its ruler"s name.
        """
        if ruler_name == "None":
            return 0xFF
        ruler_id = self.get_officer_id_by_name(ruler_name)
        return self.get_values_by_enum(District.DISTRICTRULER).index(ruler_id)

    def get_officer_name_by_id(self, officer_id: int) -> str:
        """Returns the name of an officer given its id.
        """
        if officer_id == 0xFFFF:
            return "None"
        elif officer_id >= self.get_num_rows("officer"):
            return "Shared Parent"
        officer_familyname = self.get_table_data(
            "officer", officer_id, Officer.FAMILYNAME)
        officer_givenname = self.get_table_data(
            "officer", officer_id, Officer.GIVENNAME)
        return clean(f"{officer_familyname} {officer_givenname}")

    def get_officer_id_by_name(self, officer_name: str) -> int:
        """Returns the id of an officer given its name.
        """
        if officer_name == "None":
            return 0xFFFF
        return self.officer_names().index(officer_name)

    def get_country_name_by_id(self, country_id: int) -> str:
        """Returns the name of a country given its id.
        """
        if country_id == 0xFF:
            return "None"
        elif country_id >= self.get_num_rows("country"):
            return "ERROR"
        return clean(self.get_table_data("country", country_id, Country.NAME))

    def get_country_id_by_name(self, country_name: int) -> int:
        """Returns the id of a country given its name
        """
        if country_name == "None":
            return 0xFF
        return self.country_names().index(country_name)

    def on_key_pressed(self, event: QKeyEvent):
        """Performs the appropriate action on a key-press event.
        """
        table_widget = self.tab_widget.currentWidget()
        item = table_widget.currentItem()
        if not item:
            return

        row = item.row()
        col = item.column()
        key = event.key()

        if key == Qt.Key_Return or key == Qt.Key_Enter:
            if not item.flags() & Qt.ItemIsEditable:
                self.on_cell_selected(row, col)
            else:
                table_widget.editItem(item)
        elif key == Qt.Key_Left and col > 0:
            table_widget.setCurrentCell(row, col - 1)
        elif key == Qt.Key_Right and col < table_widget.columnCount() - 1:
            table_widget.setCurrentCell(row, col + 1)
        elif key == Qt.Key_Up and row > 0:
            table_widget.setCurrentCell(row - 1, col)
        elif key == Qt.Key_Down and row < table_widget.rowCount() - 1:
            table_widget.setCurrentCell(row + 1, col)
        elif key == Qt.Key_Tab:
            # Tab: cycle to next tab
            index = (self.tab_widget.currentIndex() +
                     1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(index)
        elif key == Qt.Key_Tab + 1:
            # Shift+Tab: cycle to previous tab
            index = (self.tab_widget.currentIndex() -
                     1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(index)

    def set_item_owner_city(self, cell_item: QTableWidgetItem, col_name: str):
        """When either the owner or city of an item is set, the other value is set to None
        """
        table_widget = cell_item.tableWidget()
        table_widget.itemChanged.disconnect(self.on_cell_update)
        row_idx = cell_item.row()

        if col_name == "owner":
            other_col_name = "city"
            other_col_idx = Item.CITY
            other_cell_data = 0xFF
            ownerorcity_value = 0x01
        elif col_name == "city":
            other_col_name = "owner"
            other_col_idx = Item.OWNER
            other_cell_data = 0xFFFF
            ownerorcity_value = 0x00

        other_cell_item = self.init_cell(
            other_cell_data, "item", other_col_name)
        ownerorcity_item = self.init_cell(
            ownerorcity_value, "item", "ownerorcity")
        table_widget.setItem(row_idx, other_col_idx, other_cell_item)
        table_widget.setItem(row_idx, Item.OWNERORCITY, ownerorcity_item)
        self.set_table_data("item", row_idx, other_col_idx, other_cell_data)
        self.set_table_data(
            "item", row_idx, Item.OWNERORCITY, ownerorcity_value)
        table_widget.itemChanged.connect(self.on_cell_update)

    def get_items_by_value(self, table_name: str, col_idx: str, value: int | str):
        table = self.findChild(QTableWidget, table_name)
        return [
            table.item(row, col_idx)
            for row in range(table.rowCount())
            if table.item(row, col_idx).text() == str(value)]

    def update_officer_name(self, cell_item: QTableWidgetItem, col_name: str):
        row_idx = cell_item.row()
        col_idx = cell_item.column()
        item_text = cell_item.text()

        if col_name == "familyname":
            givenname = self.get_table_data(
                "officer", row_idx, Officer.GIVENNAME)
            new_officer_name = f"{item_text} {givenname}"
        else:
            familyname = self.get_table_data(
                "officer", row_idx, Officer.FAMILYNAME)
            new_officer_name = f"{familyname} {item_text}"
        new_officer_name = clean(new_officer_name)
        old_officer_name = self.get_officer_name_by_id(row_idx)

        for table_widget in self.table_widgets:
            table_widget.itemChanged.disconnect(self.on_cell_update)
            table_name = table_widget.objectName()
            for col_idx in range(table_widget.columnCount()):
                col_name = table_widget.horizontalHeaderItem(col_idx).text()
                if col_name not in officer_columns:
                    continue
                items: list[QTableWidgetItem] = self.get_items_by_value(
                    table_name, col_idx, old_officer_name)
                for item in items:
                    item.setText(new_officer_name)
            table_widget.itemChanged.connect(self.on_cell_update)

    def on_cell_update(self, cell_item: QTableWidgetItem):
        """Updates the data in the internal table when a cell in the table widgets is modified.
        """
        if not self.is_initialized:
            return
        row_idx = cell_item.row()
        col_idx = cell_item.column()
        table_widget = cell_item.tableWidget()
        table_name = table_widget.objectName()
        col_name = table_widget.horizontalHeaderItem(col_idx).text()
        cell_text = cell_item.text()

        if col_name in ["alliance", "research", "goal", "target", "specifictarget"]:
            # This is managed by on_cell_selected
            return
        elif col_name == "specialty":
            cell_data = self.get_specialty_value_from_text(cell_text)
        elif col_name in ["allegiance", "district"]:
            cell_data = self.get_district_id_by_district_ruler_name(cell_text)
        elif col_name == "force":
            cell_data = self.get_force_id_by_force_ruler_name(cell_text)
        elif "growth" in col_name:
            cell_data = growth_ability_map.getr(cell_text)
        elif col_name in officer_columns:
            if cell_text == "Shared Parent":
                return
            cell_data = self.get_officer_id_by_name(cell_text)
        elif col_name == "country":
            cell_data = self.get_country_id_by_name(cell_text)
        elif col_name in col_map:
            cell_data = col_map.get(col_name).getr(cell_text)
        elif self.datatypes[table_name][col_name] == "int":
            cell_data = int(cell_text)
        else:
            cell_data = cell_text

        if col_name in ["owner", "city"]:
            # Set the other value to None
            self.set_item_owner_city(cell_item, col_name)
        elif col_name in ["givenname", "familyname"]:
            self.update_officer_name(cell_item, col_name)

        self.set_table_data(table_name, row_idx, col_idx, cell_data)

        # Also set in-game year and month if either is changed
        if col_name == "year":
            self.set_table_data("scenario", 0, Scenario.INGAMEYEAR, cell_data)
        elif col_name == "month":
            self.set_table_data("scenario", 0, Scenario.INGAMEMONTH, cell_data)

    def get_force_ruler_options(self, include_none=False) -> list[str]:
        """Returns the list of all force rulers.
        """
        ruler_ids = self.get_values_by_enum(Force.FORCERULER)
        ruler_options = sorted([
            self.get_officer_name_by_id(ruler_id)
            for ruler_id in ruler_ids
            if ruler_id != 0xFFFF])
        if include_none:
            ruler_options += ["None"]
        return ruler_options

    def get_district_ruler_options(self, include_none=False) -> list[str]:
        """Returns the list of all district rulers for city and gates/ports ownership.
        """
        ruler_ids = self.get_values_by_enum(District.DISTRICTRULER)
        officer_names = self.officer_names()
        ruler_options = sorted([
            officer
            for officer in officer_names
            if officer_names.index(officer) in ruler_ids])
        if include_none:
            ruler_options += ["None"]
        return ruler_options

    def get_officer_options(self) -> list[str]:
        """Returns the sorted list of options for officers, ending on "None".
        """
        return sorted(self.officer_names()) + ["None"]

    def get_officer_names_by_sex(self, sex: int) -> list[str]:
        """Returns a list of officers for the given sex (0: Male, 1: Female)
        """
        officer_names = self.officer_names()
        officer_sexes = self.get_values_by_enum(Officer.SEX)
        return sorted([
            officer_name
            for officer_name, officer_sex in zip(officer_names, officer_sexes)
            if officer_sex == sex])

    def get_officer_names_by_allegiance(self, district_idx) -> list[str]:
        """Returns a list of officers for the given district idx
        """
        editing_force_ruler_id = self.get_table_data(
            'district', district_idx, District.FORCE)
        force_ruler_ids = self.get_values_by_enum(District.FORCE)
        district_ruler_ids = self.get_values_by_enum(District.DISTRICTRULER)
        force_district_ids = [
            force_district_id
            for force_district_id, force_ruler_id in enumerate(force_ruler_ids)
            if force_ruler_id == editing_force_ruler_id]
        officer_allegiances = self.get_values_by_enum(Officer.ALLEGIANCE)
        available_ids = [
            officer_id
            for officer_id, officer_allegiance in enumerate(officer_allegiances)
            if officer_allegiance in force_district_ids
            and officer_id not in district_ruler_ids]
        return sorted([self.get_officer_name_by_id(officer_id) for officer_id in available_ids])

    def get_country_options(self) -> list[str]:
        """Returns the sorted list of options for countries, ending on "None".
        """
        return sorted(self.country_names()) + ["None"]

    def select_parent(self):
        dialog = QDialog()

        button1 = QPushButton("Select existing officer")
        button2 = QPushButton("Select officers for shared parent")

        button1.clicked.connect(lambda: dialog.done(0))
        button2.clicked.connect(lambda: dialog.done(1))

        button_layout = QVBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        dialog.setLayout(button_layout)

        dialog.exec_()

        return dialog.result()

    def get_data_idx_from_table_idx(self, table: QTableWidget, row_idx: int):
        return table.item(row_idx, 0).data(Qt.DisplayRole) - 1

    def get_table_item_from_data_idx(self, table_name: str, data_idx: int, col_idx: int):
        table = self.findChild(QTableWidget, table_name)
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item.data(Qt.DisplayRole) - 1 == data_idx:
                row_idx = row
                break
        return table.item(row_idx, col_idx)

    def on_cell_selected(self, row_idx: int, col_idx: int):
        """Triggers upon doubleclicking a cell and calls the appropriate function depending on the column.
        """
        table = self.get_current_table()
        cell_item = table.item(row_idx, col_idx)
        col_name = table.horizontalHeaderItem(col_idx).text()
        data_idx = self.get_data_idx_from_table_idx(table, row_idx)

        if col_name in ["father", "mother"]:
            if self.select_parent():
                self.set_parents(data_idx, col_name)
                return
            sex = col_name == "mother"
            options = self.get_officer_names_by_sex(sex)
        elif col_name == "alliance":
            self.set_alliance(data_idx)
            return
        elif col_name == "research":
            self.set_research(data_idx)
            return
        elif col_name in ["goal", "target",  "specifictarget"]:
            self.set_behaviour_targets(data_idx, col_name)
            return
        elif "growth" in col_name:
            options = growth_ability_map.values()
        elif col_name == "specialty":
            options = specialty_options.values()
        elif col_name == "force":
            options = self.get_force_ruler_options(include_none=True)
        elif col_name == "districtruler":
            options = self.get_officer_names_by_allegiance(data_idx)
        elif col_name in ["allegiance", "district"]:
            options = self.get_district_ruler_options(include_none=True)
        elif col_name in officer_columns:
            options = self.get_officer_options()
        elif col_name == "country":
            options = self.get_country_options()
        elif col_name in col_map:
            options = col_map[col_name].values()
        else:
            print("Unimplemented")
            return

        self.choose_option(cell_item, options)

    def choose_option(self, cell_item: QTableWidgetItem, options: list[str]):
        """Opens a dialogue box with a drop-down menu given a list of options.
        """
        combo_box = QComboBox()
        combo_box.addItems(options)
        combo_box.setEditable(True)

        item, ok = QInputDialog.getItem(
            self, "Choose option", "Select an option:", options)

        if ok and item and item in options:
            cell_item.setText(item)

    def get_values_by_enum(self, enum_value):
        """Returns all values in the table for a column given an enum value representing that column.
        """
        return [row[enum_value] for row in self.table_datas[enum_value.__class__.__name__.lower()]["data"]]

    def set_parents(self, editing_officer_id: int, col_name: str):
        def make_unique_shared_parent_value(parent: int):
            # NOTE: Could theoretically overflow
            used_values = [
                value
                for value in self.get_values_by_enum(parent)
                if value >= 850 and value != 0xFFFF]
            n = 2000
            while True:
                if used_values.count(n) == 0:
                    return n
                n += 1

        table = self.get_current_table()
        table.itemChanged.disconnect(self.on_cell_update)

        parent_sex = Officer.FATHER if col_name == "father" else Officer.MOTHER

        dialog = QDialog()
        dialog.setWindowTitle("Set Shared Parent")

        layout = QVBoxLayout(dialog)

        shared_parent_list = QListWidget(dialog)
        shared_parent_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(shared_parent_list)

        parent_ids = self.get_values_by_enum(parent_sex)

        parent_value = parent_ids[editing_officer_id]

        if parent_value < 850 or parent_value == 0xFFFF:
            # We make a new available unique parent value
            parent_value = make_unique_shared_parent_value(parent_sex)
            shared_parent_ids = [editing_officer_id]
        else:
            shared_parent_ids = [
                officer_id
                for officer_id, parent_id in enumerate(parent_ids)
                if parent_id == parent_value]

        spo_names = [
            self.get_officer_name_by_id(officer_id)
            for officer_id in shared_parent_ids]

        for spo_name in spo_names:
            list_item = QListWidgetItem(spo_name)
            shared_parent_list.addItem(list_item)

        combobox = QComboBox(dialog)
        officer_names = self.officer_names()
        combobox.addItems(officer_names)
        combobox.setEditable(True)
        layout.addWidget(combobox)

        def add_value():
            selected_value = combobox.currentText()
            if selected_value not in officer_names or shared_parent_list.findItems(selected_value, Qt.MatchExactly):
                return
            list_item = QListWidgetItem(selected_value)
            shared_parent_list.addItem(list_item)

        def remove_value():
            selected_items = shared_parent_list.selectedItems()
            for item in selected_items:
                shared_parent_list.takeItem(shared_parent_list.row(item))

        buttons_layout = QHBoxLayout()

        add_button = QPushButton("Add Officer", dialog)
        add_button.clicked.connect(add_value)
        buttons_layout.addWidget(add_button)

        remove_button = QPushButton("Remove Officer(s)", dialog)
        remove_button.clicked.connect(remove_value)
        buttons_layout.addWidget(remove_button)

        layout.addLayout(buttons_layout)

        confirmation_buttons = self.make_confirmation_buttons(dialog)
        layout.addLayout(confirmation_buttons)

        dialog.setLayout(layout)

        if dialog.exec_() != QDialog.Accepted:
            table.itemChanged.connect(self.on_cell_update)
            return

        selected_officers = [
            shared_parent_list.item(i).text()
            for i in range(shared_parent_list.count())]

        removed_officers = [
            officer
            for officer in spo_names
            if officer not in selected_officers]

        for officer_name in removed_officers:
            # Set the value for removed officers to None
            officer_id = self.get_officer_id_by_name(officer_name)
            cell_item = self.get_table_item_from_data_idx(
                "officer", officer_id, parent_sex)
            self.set_table_data(
                "officer", officer_id, parent_sex, 0xFFFF)
            cell_item.setText("None")

        for officer_name in selected_officers:
            # Set the shared parent value for each selected officer
            officer_id = self.get_officer_id_by_name(officer_name)
            cell_item = self.get_table_item_from_data_idx(
                "officer", officer_id, parent_sex)
            self.set_table_data(
                "officer", officer_id, parent_sex, parent_value)
            cell_item.setText("Shared Parent")

        table.itemChanged.connect(self.on_cell_update)

    def set_behaviour_targets(self, row_idx: int, col_name: str):
        dialog = QDialog(self)
        dialog.setWindowTitle("Set District Behaviour and Target")
        layout = QVBoxLayout()
        behaviour_layout = QHBoxLayout()
        behaviour_label = QLabel("Behaviour:")
        behaviour_combo = QComboBox()
        target_layout = QHBoxLayout()
        target_label = QLabel("Target:")
        target_combo = QComboBox()

        def parse_goal_value(goal_value: int):
            target = (goal_value >> 8) & 0xFF
            behaviour = goal_value & 0xFF
            return behaviour, target

        def create_goal_value(behaviour: int, target: int):
            return ((target & 0xFF) << 8) | (behaviour & 0xFF)

        column_map, tablename, col_idx = {
            "goal": (force_behaviour_map, "force", Force.GOAL),
            "target": (district_behaviour_map, "district", District.TARGET),
            "specifictarget": (specific_behaviour_map, "district", District.SPECIFICTARGET)
        }.get(col_name)

        goal_value = self.get_table_data(tablename, row_idx, col_idx)
        behaviour_value, target_value = parse_goal_value(goal_value)

        def update_target_combo():
            behaviour_text = behaviour_combo.currentText()

            targets = {
                ("goal", "Conquer Region"): conquer_region_map.values,
                ("goal", "Conquer Province"): conquer_province_map.values,
                ("target", "Destroy Force"): self.get_force_ruler_options,
                ("target", "Conquer Region"): conquer_region_map.values,
                ("target", "Conquer Province"): conquer_province_map.values,
                ("target", "Conquer City/Gate/Port"): city_map.values,
                ("specifictarget", "Conquer City"): city_map.values,
                ("specifictarget", "Diplomacy"): self.get_force_ruler_options
            }.get((col_name, behaviour_text), lambda: [])()

            target_combo.clear()
            target_combo.addItems(targets)
            target_combo.setEnabled(bool(targets))

        target_text = {
            ("goal", 0x01): conquer_region_map.get,
            ("goal", 0x02): conquer_province_map.get,
            ("target", 0x00): self.get_force_ruler_name_by_force_id,
            ("target", 0x01): conquer_region_map.get,
            ("target", 0x02): conquer_province_map.get,
            ("target", 0x03): city_map.get,
            ("specifictarget", 0x03): city_map.get,
            ("specifictarget", 0x04): self.get_force_ruler_name_by_force_id
        }.get((col_name, behaviour_value), lambda _: "")(target_value)

        behaviour_layout.addWidget(behaviour_label)
        behaviour_combo.addItems(column_map.values())
        behaviour_combo.setCurrentText(column_map[behaviour_value])
        behaviour_combo.currentIndexChanged.connect(update_target_combo)
        behaviour_layout.addWidget(behaviour_combo)
        layout.addLayout(behaviour_layout)

        target_layout.addWidget(target_label)
        update_target_combo()
        target_combo.setCurrentText(target_text)
        target_layout.addWidget(target_combo)
        layout.addLayout(target_layout)

        buttons_layout = self.make_confirmation_buttons(dialog)
        layout.addLayout(buttons_layout)

        dialog.setLayout(layout)

        if dialog.exec_() != QDialog.Accepted:
            return

        target_text = target_combo.currentText()
        behaviour_text = behaviour_combo.currentText()
        new_behaviour_value = column_map.getr(behaviour_text)

        new_target_value = {
            ("goal", 0x01): conquer_region_map.getr,
            ("goal", 0x02): conquer_province_map.getr,
            ("target", 0x00): self.get_force_id_by_force_ruler_name,
            ("target", 0x01): conquer_region_map.getr,
            ("target", 0x02): conquer_province_map.getr,
            ("target", 0x03): city_map.getr,
            ("specifictarget", 0x03): city_map.getr,
            ("specifictarget", 0x04): self.get_force_id_by_force_ruler_name
        }.get((col_name, new_behaviour_value), lambda _: 0xF)(target_text)

        new_goal_value = create_goal_value(
            new_behaviour_value, new_target_value)
        self.set_table_data(tablename, row_idx, col_idx, new_goal_value)

    def set_research(self, editing_force_id: int):
        """Opens a dialogue box with sliders for each individual research level.
        """

        def parse_research_value(research_value: int):
            return [(research_value >> (28 - i * 4)) & 0x0F for i in range(8)]

        def create_research_value(research_levels: list[int]):
            return sum(research_level_values[level] << (28 - i * 4) for i, level in enumerate(research_levels))

        dialog = QDialog(self)
        dialog.setWindowTitle("Research Levels")

        research_value = self.get_table_data(
            "force", editing_force_id, Force.RESEARCH)
        research_levels = parse_research_value(research_value)

        sliders_layout = QGridLayout()
        sliders = []
        for i, label in enumerate(research_labels):
            research_level = research_level_values.index(research_levels[i])
            slider_label = QLabel(label)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(4)
            slider.setValue(research_level)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(1)
            slider.setSingleStep(1)
            slider_value_label = QLabel(str(research_level))
            slider_value_label.setAlignment(Qt.AlignRight)
            sliders_layout.addWidget(slider_label, i, 0)
            sliders_layout.addWidget(slider, i, 1)
            sliders_layout.addWidget(slider_value_label, i, 2)
            sliders.append(slider)
            slider.valueChanged.connect(
                lambda value: slider_value_label.setText(str(value)))

        buttons_layout = self.make_confirmation_buttons(dialog)

        main_layout = QVBoxLayout()
        main_layout.addLayout(sliders_layout)
        main_layout.addLayout(buttons_layout)

        dialog.setLayout(main_layout)

        if dialog.exec_() != QDialog.Accepted:
            return

        new_research_levels = [slider.value() for slider in sliders]
        new_research_value = create_research_value(new_research_levels)
        self.set_table_data(
            "force", editing_force_id, Force.RESEARCH, new_research_value)

    def set_alliance(self, editing_force_id: int):
        """Opens a dialogue box with checkboxes for all rulers to create alliances between them.
        """

        def create_alliance_value(force_ids: list[int], exclude_force_id: int):
            return reduce(
                lambda x, y: x | (1 << y)
                if y != exclude_force_id
                else x, force_ids, 0
            )

        def parse_alliance_value(alliance_value: int):
            return [i for i in range(self.get_num_rows("force")) if alliance_value & (1 << i)]

        dialog = QDialog(self)
        dialog.setWindowTitle("Alliances")

        main_layout = QVBoxLayout()

        checkboxes_widget = QWidget()
        checkboxes_layout = QVBoxLayout(checkboxes_widget)

        alliance_value = self.get_table_data(
            "force", editing_force_id, Force.ALLIANCE)
        force_ids = parse_alliance_value(alliance_value)
        alliance_values = self.get_values_by_enum(Force.ALLIANCE)
        force_rulers = self.get_values_by_enum(Force.FORCERULER)

        checkboxes: list[QCheckBox] = []

        for force_id, ruler in enumerate(force_rulers):
            ruler_name = self.get_officer_name_by_id(ruler)
            checkbox = QCheckBox(f"{ruler_name}")

            if force_id in force_ids:
                checkbox.setChecked(True)

            checkboxes.append(checkbox)

            # We only show actually used rulers
            if ruler_name != "None" and force_id != editing_force_id:
                checkboxes_layout.addWidget(checkbox)

        checkboxes_widget.setLayout(checkboxes_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(checkboxes_widget)

        buttons_layout = self.make_confirmation_buttons(dialog)

        def clear_all_checkboxes():
            """Clears all the checkboxes in the list.
            """
            for checkbox in checkboxes:
                checkbox.setChecked(False)

        clear_button = QPushButton("Clear All")
        clear_button.clicked.connect(clear_all_checkboxes)
        buttons_layout.addWidget(clear_button)

        main_layout.addWidget(scroll_area)
        main_layout.addLayout(buttons_layout)

        dialog.setLayout(main_layout)

        if dialog.exec_() != QDialog.Accepted:
            return

        # We consider the force being edited as part of the included values.
        checked = [
            force_id for force_id, checkbox in enumerate(checkboxes)
            if checkbox.isChecked()] + [editing_force_id]

        for force_id, alliance_value in enumerate(alliance_values):
            # Create the new alliance value, excluding the current force_id
            new_alliance_value = create_alliance_value(checked, force_id)
            if force_id in checked:
                # This force takes part in the alliance
                self.set_table_data(
                    "force", force_id, Force.ALLIANCE, new_alliance_value)
            else:
                # We turn off the bits in the new alliance value for this force"s alliance in this case.
                self.set_table_data(
                    "force", force_id, Force.ALLIANCE, alliance_value & ~new_alliance_value)

    def make_confirmation_buttons(self, dialog: QDialog):
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: dialog.accept())
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: dialog.reject())
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        return buttons_layout

    def get_current_table(self):
        """Get the focused table of the current tab widget."""
        current_tab = self.tab_widget.currentIndex()
        current_table = self.table_widgets[current_tab]
        return current_table

    def sort_table(self, col_idx: int):
        """Sorts the table in ascending/descending order on a given column.
        """
        table = self.get_current_table()
        self.sorting_order = Qt.DescendingOrder if self.sorting_order == Qt.AscendingOrder else Qt.AscendingOrder
        table.sortItems(col_idx, self.sorting_order)

        # Update sorting_order attribute
        self.sorting_order = table.horizontalHeader().sortIndicatorOrder()

    def filter_table(self):
        """Callback function for filtering the table on a given string input.
        """
        search_text = self.search_box.text().lower()

        for table in self.table_widgets:
            table.setSortingEnabled(False)

            for row_idx in range(table.rowCount()):
                match_found = False

                for col_idx in range(table.columnCount()):
                    cell_text = table.item(row_idx, col_idx).text().lower()

                    if search_text in cell_text:
                        match_found = True
                        break

                if not match_found:
                    officer_name = self.get_officer_name_by_id(row_idx).lower()
                    if search_text in officer_name:
                        match_found = True

                table.setRowHidden(row_idx, not match_found)

            table.setSortingEnabled(True)
            table.sortByColumn(0, self.sorting_order)

    def open_file(self):
        """Opens a scenario file and parses the data into a database file for editing.
        """
        self.is_initialized = False
        self.old_scen_path, _ = QFileDialog.getOpenFileName(
            self, "Open Scenario File", "", "Scenario Files (*.s11 SAN11RES.BIN)")

        if not self.old_scen_path:
            return

        if self.old_scen_path.endswith("SAN11RES.BIN"):
            self.version = Version.PS2EN
            # List of scenario names
            item, ok = QInputDialog.getItem(
                self, "Select Scenario", "Select a scenario:", ps2_scenarios, 0, False)
            if ok:
                # Get the index of the selected item
                self.file_offset = ps2_scenarios[item]
            else:
                return

        else:
            self.version = Version.PCEN
            self.file_offset = 0

        self.tab_widget.clear()

        self.db_path = os.path.join(tempfile.gettempdir(), "rtk11.db")

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        # This reads the data from the scenario file into the database
        with BinaryParser("rtk11.lyt", encoding="shift-jis", file_offset=self.file_offset) as bp:
            bp.parse_file(self.old_scen_path, self.db_path)
            self.datatypes = {
                tablename: {
                    col_name: col_type
                    for section in tabledata["sections"]
                    for col_name, col_type, col_size in section["data"]
                }
                for tablename, tabledata in bp.data.items()
            }
            for table in self.datatypes.values():
                table["id"] = "int"

        with connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            table_names = [x[0] for x in cursor.fetchall()]

            # Retrieve the tables in the database
            for table_name in table_names:
                # Retrieve the column names and data from the table
                cursor.execute(f"SELECT * FROM {table_name}")
                col_names = [x[0] for x in cursor.description]
                table_data = [list(x) for x in cursor.fetchall()]
                self.table_datas[table_name] = {
                    "data": table_data,
                    "col_names": col_names,
                    "num_rows": len(table_data)
                }

        # Initialise table widgets``
        for table_name in table_names:
            if table_name == "sqlite_sequence":
                continue
            self.init_table_widget(table_name)

        self.save_file_action.setEnabled(True)
        self.save_as_file_action.setEnabled(True)
        self.is_initialized = True

    def save_file(self):
        """
        Saves the current state of the database to the scenario file.
        Will first prompt for the path to save to if it doesn"t exist yet
        """

        if not self.new_scen_path:
            self.save_as_file()
            return

        total = sum([len(table_data["col_names"])
                    for table_data in self.table_datas.values()])

        progress_dialog = QProgressDialog(
            "Saving scenario file...", "Cancel", 0, total, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setAutoClose(False)
        progress_dialog.setAutoReset(False)
        progress_dialog.setMinimumDuration(0)

        save_thread = SaveThread(
            db_path=self.db_path,
            scen_path=self.new_scen_path,
            table_datas=self.table_datas,
            file_offset=self.file_offset
        )
        save_thread.save_progress.connect(progress_dialog.setValue)
        save_thread.finished.connect(progress_dialog.close)
        save_thread.start()

        progress_dialog.exec_()

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
    app.setStyleSheet(qdarkstyle.load_stylesheet(
        qt_api="pyqt5", palette=qdarkstyle.DarkPalette))
    gui = ROTKXIGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # TODO: Deleteme
    main()
