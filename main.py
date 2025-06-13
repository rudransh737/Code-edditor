import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QToolBar, QToolButton, QSplitter, QTabWidget,
    QStatusBar, QDockWidget, QListWidget, QListWidgetItem,
    QTabBar, QTreeView, QMenuBar, QMenu,QFileDialog,QPushButton,QInputDialog,QLineEdit
)
from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtCore import Qt, QSize, QDir, QModelIndex
from PySide6.QtWidgets import QFileSystemModel
from PySide6.QtWebEngineWidgets import QWebEngineView
import time
import os
import subprocess
import threading
from winpty import PTY
import re
# from ansi2html import Ansi2HTMLConverter

class ThreadedPTY():
    def __init__(self, pty):
        self.pty = pty
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            output = self.pty.read()
            if output:
                print(output.decode('utf-8', errors='ignore'), end='')

    def write(self, command):
        self.pty.write(command)

class ExplorerTreeView(QTreeView):
    def __init__(self, parent=None, open_file_callback=None):
        super().__init__(parent)
        self.open_file_callback = open_file_callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                model = self.model()
                if isinstance(model, QFileSystemModel):
                    file_path = model.filePath(index)
                    if os.path.isfile(file_path) and self.open_file_callback:
                        self.open_file_callback(file_path)
        super().mousePressEvent(event)

class Code_Edditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Devloop IDE")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #252526; /* Dark background */
                color: #e0e0e0;          /* Light text */
            }
            QTextEdit {
                background-color: #1e1e1e; /* Darker text area background */
                color: #ffffff;
                border: 1px solid #333;
                font-family: 'Consolas', monospace; /* Use a monospace font */
                font-size: 14px;
            }
            QToolBar {
                background-color: #2d2d2d; /* Dark toolbar background */
                border-bottom: 1px solid #333;
                padding: 2px;
            }
            QToolButton {
                background-color: transparent;
                color: #b0b0b0;
                border: none;
                padding: 5px;
                min-width: 24px; /* Ensure buttons have a minimum size */
                height: 24px;
            }
            QToolButton:hover {
                background-color: #3e3e3e; /* Slightly lighter on hover */
                color: #ffffff;
            }
            QToolButton:pressed {
                background-color: #505050; /* Slightly lighter on press */
                color: #ffffff;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #b0b0b0;
                border-top: 1px solid #333;
                padding-left: 5px;
            }
            QTabWidget::pane { /* The area *around* the tabs */
                background-color: #1e1e1e;
                border: 1px solid #333;
                margin: 0px;
            }

            QTabWidget::tab-bar {
                left: 0px; /* position at the top */
                background-color: #2d2d2d;
                border-bottom: 1px solid #333;
            }

            QTabBar::tab {
                background-color: #2d2d2d;
                color: #b0b0b0;
                border: 1px solid #333;
                border-bottom-color: #1e1e1e; /* Make the bottom border the same as the pane. */
                padding: 8px 16px;
                min-width: 80px;
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: #1e1e1e;
                color: #ffffff;
                border-bottom-color: #1e1e1e; /* Selected tab bottom border */
            }

            QTabBar::tab:selected {
                font-weight: bold;
            }

            QSplitter::handle {
                background-color: #333; /* Dark splitter handle */
                width: 4px;
            }

            QSplitter::handle:hover {
                background-color: #444; /* Lighter on hover */
            }
            QDockWidget {
                background-color: #252526;
                color: #e0e0e0;
                border: 1px solid #333;
            }
            QDockWidget > QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }

            QDockWidget::title {
                background-color: #2d2d2d;
                color: #b0b0b0;
                padding: 5px;
                border-bottom: 1px solid #333;
            }
            QTreeView {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #333;
                font-size: 14px;
            }

            QTreeView::item {
                padding: 2px;
            }

            QTreeView::item:selected {
                background-color: #3e3e3e;
                color: #ffffff;
            }

            QTreeView::item:hover {
                background-color: #3e3e3e;
                color: #ffffff;
            }
            /* --- MENU BAR STYLES --- */
            QMenuBar {
                background-color: #2d2d2d; /* Dark background for the entire menu bar */
                color: #b0b0b0;          /* Light gray text for menu titles */
                border-bottom: 1px solid #3a3a3a; /* Subtle bottom border */
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                font-size: 13px;
                padding: 0px; /* Remove default padding for a tighter look */
            }

            /* Styles for individual menu titles on the menu bar (e.g., "File", "Edit") */
            QMenuBar::item {
                background-color: transparent; /* No background by default */
                color: #b0b0b0;
                padding: 8px 12px; /* Padding inside each menu item */
                margin: 0px 2px;   /* Small margin between menu items */
                border-radius: 3px; /* Slightly rounded corners */
            }

            /* When a menu bar item is hovered over or selected */
            QMenuBar::item:selected {
                background-color: #3e3e3e; /* Darker on hover */
                color: #ffffff;           /* White text on hover */
            }

            /* When a menu bar item is pressed down */
            QMenuBar::item:pressed {
                background-color: #505050; /* Even darker when pressed */
                color: #ffffff;
            }

            /* --- DROPDOWN MENU (QMenu) STYLES --- */
            QMenu {
                background-color: #252526; /* Dark background for the dropdown menu */
                border: 1px solid #3a3a3a; /* Border around the dropdown */
                border-radius: 4px;      /* Slightly rounded corners for the dropdown */
                padding: 5px;            /* Padding inside the dropdown */
            }

            /* Styles for individual items within the dropdown menu (e.g., "New File") */
            QMenu::item {
                background-color: transparent;
                color: #e0e0e0;
                padding: 6px 15px; /* Padding for each item in the dropdown */
                margin: 2px 0px;   /* Small vertical margin between items */
                border-radius: 3px;
            }

            /* When a dropdown menu item is hovered over */
            QMenu::item:selected {
                background-color: #3e3e3e; /* Darker on hover */
                color: #ffffff;           /* White text on hover */
            }

            /* When a dropdown menu item is disabled */
            QMenu::item:disabled {
                color: #777777; /* Gray out disabled items */
            }

            /* Styles for the separator lines in the dropdown menu */
            QMenu::separator {
                height: 1px;               /* Thin line */
                background-color: #3a3a3a; /* Dark gray line */
                margin: 5px 10px;          /* Margin above/below and horizontal padding */
            }
        """)
        self.create_file_explorer()
        self.integrated_browser()
        self.create_output_panel()
        self.create_code_area()
        self.create_menu_bar()
        self.create_status_bar()
        self.initialize_terminal()

    def create_file_explorer(self):
        self.explorer_panel = QDockWidget("Explorer", self)
        self.explorer_panel.setObjectName("ExplorerPanel")
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(f"C:/Users/Hp/Desktop")
        self.explorer_tree = ExplorerTreeView(open_file_callback=self.open_file_in_tab)
        self.explorer_tree.setModel(self.file_system_model)
        self.explorer_tree.setRootIndex(self.file_system_model.index(QDir.homePath()))
        self.explorer_panel.setWidget(self.explorer_tree)
        
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorer_panel)

        for i in range(1, self.file_system_model.columnCount()):
            self.explorer_tree.setColumnHidden(i, True)

    def open_file_in_tab(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        editor = QTextEdit()
        editor.setText(content)
        base_name = os.path.basename(file_path)
        self.tab_widget.addTab(editor, base_name)
        self.tab_widget.setCurrentWidget(editor)
    def integrated_browser(self):
        self.reload_button = QAction("R")
        self.reload_button.triggered.connect(self.reload)
        self.back_button = QAction(">")
        self.back_button.triggered.connect(self.back)
        self.forward_button = QAction("<")
        self.forward_button.triggered.connect(self.forward)
        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("background-color: #1e1e1e; color: #ffffff; border: 1px solid #333;")
        self.go_button = QAction("<")
        self.go_button.triggered.connect(self.change_url)
        self.nav_bar = QToolBar()
        self.nav_bar.addAction(self.reload_button)
        self.nav_bar.addAction(self.back_button)
        self.nav_bar.addAction(self.forward_button)
        self.nav_bar.addWidget(self.url_bar)
        self.webview_layout = QVBoxLayout()
        self.webview = QWebEngineView()
        self.webview.urlChanged.connect(self.update_url)
        self.webview_layout.addWidget(self.nav_bar)
        self.webview_layout.addWidget(self.webview)
        self.webview.setUrl("https://www.duckduckgo.com")
        self.webview_frame = QWidget()
        self.webview_frame.setLayout(self.webview_layout)
        self.integrated_browser_panel = QDockWidget("Browser",self)
        self.integrated_browser_panel.setObjectName("Browser")
        self.integrated_browser_panel.setWidget(self.webview_frame)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,self.integrated_browser_panel)
    def reload(self):
        self.webview.reload()
    def back(self):
        self.webview.back()
    def forward(self):
        self.webview.forward()
    def change_url(self):
        url = self.url_bar.text()
        self.webview.setUrl(url)
    def update_url(self,url):
        self.url_bar.setText(url.toString())
    def create_output_panel(self):
        self.output_panel = QDockWidget("Output", self)
        self.output_panel.setObjectName("OutputPanel")
        self.output_text = QTextEdit()
        self.input_area = QLineEdit()
        self.input_area.setFixedHeight(50)
        self.input_area.setStyleSheet("background-color: #1e1e1e; color: #ffffff; border: 1px solid #333;")
        self.input_area.setPlaceholderText("Enter your command here...")
        self.input_area.returnPressed.connect(self.execute_terminal_command)
        self.output_text.setReadOnly(True)
        self.combined_layout = QVBoxLayout()
        self.combined_layout.addWidget(self.output_text)
        self.combined_layout.addWidget(self.input_area)
        self.output_widget = QWidget()
        self.output_widget.setLayout(self.combined_layout)
        self.output_panel.setWidget(self.output_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.output_panel)

    def create_code_area(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)

    def create_menu_bar(self):
        # Create a QMenuBar instance
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar) # Set it as the main window's menu bar
        self.show_explorer_action = QAction("Show Explorer", self)
        self.show_explorer_action.setCheckable(True)
        self.show_explorer_action.setChecked(True)
        self.show_output_action = QAction("Show Output", self)
        self.show_output_action.setCheckable(True)
        self.show_output_action.setChecked(True)
        # Now add menus to your self.menu_bar object
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction("Open Folder", self.open_folder)
        self.file_menu.addAction("New File", self.create_new_file)
        self.edit_menu = self.menu_bar.addMenu("Edit")
        self.selection_menu = self.menu_bar.addMenu("Selection")
        self.view_menu = self.menu_bar.addMenu("View")
        self.view_menu.addAction(self.show_explorer_action)
        self.view_menu.addAction(self.show_output_action)
        self.go_menu = self.menu_bar.addMenu("Go")
        self.run_menu = self.menu_bar.addMenu("Run")
        self.terminal_menu = self.menu_bar.addMenu("Terminal")
        self.terminal_menu.addAction("New Terminal", self.create_output_panel)
        self.show_explorer_action.toggled.connect(self.explorer_panel.setVisible)
        self.show_output_action.toggled.connect(self.output_panel.setVisible)

    def close_tab(self,index):
        self.tab_widget.removeTab(index)
    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", QDir.homePath())
        if folder_path:
            self.file_system_model.setRootPath(folder_path)
            self.explorer_tree.setRootIndex(self.file_system_model.index(folder_path))
            self.explorer_tree.expandAll()
            self.explorer_panel.setWindowTitle(os.path.basename(folder_path))
    def create_status_bar(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.go_to_line_col = QPushButton("Go to Line/Col")
        self.go_to_line_col.setStyleSheet("background-color: #2d2d2d; color: #b0b0b0;")
        self.select_indentaion = QPushButton("Select Indentation")
        self.select_indentaion.setStyleSheet("background-color: #2d2d2d; color: #b0b0b0;")
        self.select_encoding = QPushButton("Select Encoding")
        self.select_encoding.setStyleSheet("background-color: #2d2d2d; color: #b0b0b0;")
        self.select_language_mode = QPushButton("Select Language Mode")
        self.select_language_mode.setStyleSheet("background-color: #2d2d2d; color: #b0b0b0;")
        self.notification = QPushButton("Notification")
        self.notification.setStyleSheet("background-color: #2d2d2d; color: #b0b0b0;")
        all_widgets = [self.go_to_line_col, self.select_indentaion, self.select_encoding, self.select_language_mode, self.notification]
        for widget in all_widgets:
            widget.setFixedHeight(25)
            self.status_bar.addPermanentWidget(widget)
    def execute_terminal_command(self):
        pass
    def initialize_terminal(self):
        pass
        

    


    def create_new_file(self):
        selected_folder = self.explorer_tree.currentIndex()
        if selected_folder.isValid():
            folder_path = self.file_system_model.filePath(selected_folder)
            file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
            if ok and file_name:
                new_file_path = os.path.join(folder_path, file_name)
                with open(new_file_path, 'w') as f:
                    pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    code_edditor = Code_Edditor()
    code_edditor.show()
    sys.exit(app.exec())