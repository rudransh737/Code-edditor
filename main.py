import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QToolBar, QToolButton, QSplitter, QTabWidget,
    QStatusBar, QDockWidget, QListWidget, QListWidgetItem, QTabBar, QTreeView
)
from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtCore import Qt, QSize, QDir
from PySide6.QtWidgets import QFileSystemModel
import tkinter as tk
from tkinter import filedialog

class VSCodeClone(QMainWindow):
    """
    A simplified clone of the VS Code user interface using PySide6.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VS Code Clone")
        self.setGeometry(100, 100, 1200, 800)  # Larger initial size

        self.create_actions()
        self.create_toolbars()
        self.create_status_bar()
        self.create_central_widget()
        self.create_panels()  # Create the side panels
        self.file_menu = self.menuBar().addMenu("File")  # Get the File menu
        self.file_menu.addAction(self.open_folder_action) # Add the new action

        # Apply a stylesheet for a more VSCode-like appearance.  This is basic,
        # and you'd likely want a more comprehensive one.
        self.setStyleSheet("""
            QMainWindow {
                background-color: #252526; /* Dark background */
                color: #e0e0e0;         /* Light text */
            }
            QTextEdit {
                background-color: #1e1e1e;  /* Darker text area background */
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

        """)

    def create_actions(self):
        """
        Creates the actions for the toolbar and menus.
        """
        self.new_action = QAction(QIcon("icons/new.png"), "New File", self)
        self.new_action.setShortcut("Ctrl+N")
        self.open_action = QAction(QIcon("icons/open.png"), "Open File", self)
        self.open_action.setShortcut("Ctrl+O")
        self.save_action = QAction(QIcon("icons/save.png"), "Save File", self)
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.open_folder_action = QAction("Open Folder...", self) # New Action

        self.cut_action = QAction(QIcon("icons/cut.png"), "Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action = QAction(QIcon("icons/copy.png"), "Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.paste_action = QAction(QIcon("icons/paste.png"), "Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.undo_action = QAction(QIcon("icons/undo.png"), "Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action = QAction(QIcon("icons/redo.png"), "Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")

        self.show_explorer_action = QAction("Show Explorer", self)
        self.show_explorer_action.setCheckable(True)
        self.show_explorer_action.setChecked(True)
        self.show_output_action = QAction("Show Output", self)
        self.show_output_action.setCheckable(True)
        self.show_output_action.setChecked(True)

        # Connect actions to methods (add these method definitions to the class)
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.exit_action.triggered.connect(self.close)
        self.open_folder_action.triggered.connect(self.open_folder) # Connect the new action
        self.cut_action.triggered.connect(self.text_cut)
        self.copy_action.triggered.connect(self.text_copy)
        self.paste_action.triggered.connect(self.text_paste)
        self.undo_action.triggered.connect(self.text_undo)
        self.redo_action.triggered.connect(self.text_redo)
        self.show_explorer_action.toggled.connect(self.toggle_explorer)
        self.show_output_action.toggled.connect(self.toggle_output)

    def create_toolbars(self):
        """
        Creates the toolbars.
        """
        self.file_toolbar = self.addToolBar("File")
        self.file_toolbar.setObjectName("FileToolbar")  # Set object name for CSS
        self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)

        self.edit_toolbar = self.addToolBar("Edit")
        self.edit_toolbar.setObjectName("EditToolbar")
        self.edit_toolbar.addAction(self.cut_action)
        self.edit_toolbar.addAction(self.copy_action)
        self.edit_toolbar.addAction(self.paste_action)
        self.edit_toolbar.addAction(self.undo_action)
        self.edit_toolbar.addAction(self.redo_action)

    def create_status_bar(self):
        """
        Creates the status bar.
        """
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

    def create_central_widget(self):
        """
        Creates the central widget (the text editor).
        """
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Enable close buttons on tabs
        self.tab_widget.tabCloseRequested.connect(self.close_tab) # Connect the signal
        self.text_edit_1 = QTextEdit()
        self.text_edit_2 = QTextEdit()
        self.tab_widget.addTab(self.text_edit_1, "Tab 1")
        self.tab_widget.addTab(self.text_edit_2, "Tab 2")
        self.setCentralWidget(self.tab_widget)

    def create_panels(self):
        """
        Creates the side panels (Explorer and Output) as dockable widgets.
        """
        self.explorer_panel = QDockWidget("Explorer", self)
        self.explorer_panel.setObjectName("ExplorerPanel") # For CSS
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(QDir.homePath()) # Start with the user's home directory
        self.explorer_tree = QTreeView()
        self.explorer_tree.setModel(self.file_system_model)
        self.explorer_tree.setRootIndex(self.file_system_model.index(QDir.homePath()))
        self.explorer_panel.setWidget(self.explorer_tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorer_panel)

        for i in range(1, self.file_system_model.columnCount()):
            self.explorer_tree.setColumnHidden(i, True)

        self.output_panel = QDockWidget("Output", self)
        self.output_panel.setObjectName("OutputPanel") # For CSS
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_panel.setWidget(self.output_text)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.output_panel)

        # Make the actions toggle the visibility of the panels
        self.show_explorer_action.triggered.connect(self.explorer_panel.setVisible)
        self.show_output_action.triggered.connect(self.toggle_output)
        # Add actions to View menu to show/hide panels
        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.show_explorer_action)
        view_menu.addAction(self.show_output_action)
        self.file_menu = self.menuBar().addMenu("File")  # Get the File menu
        self.file_menu.addAction(self.open_folder_action) # Add the new action


    # --- Slots for Actions ---
    def new_file(self):
        new_tab = QTextEdit()
        self.tab_widget.addTab(new_tab, f"Tab {self.tab_widget.count() + 1}")
        self.tab_widget.setCurrentWidget(new_tab)
        self.status_bar.showMessage("New Tab Created")

    def open_file(self):
        # In a real application, you'd use QFileDialog to get the file path
        # and then read the file content into a new tab.
        new_tab = QTextEdit()
        new_tab.setText("Opening file (simulated)...\nThis is a placeholder.")
        self.tab_widget.addTab(new_tab, f"File {self.tab_widget.count()}")  # Use a more descriptive tab title
        self.tab_widget.setCurrentWidget(new_tab)  # Switch to the new tab
        self.status_bar.showMessage("File Opened (simulated)")

    def save_file(self):
        # In a real application, you'd use QFileDialog
        self.status_bar.showMessage("File Saved")

    def text_cut(self):
        current_text_edit = self.tab_widget.currentWidget()
        if isinstance(current_text_edit, QTextEdit):
            current_text_edit.cut()
            self.status_bar.showMessage("Text Cut")

    def text_copy(self):
        current_text_edit = self.tab_widget.currentWidget()
        if isinstance(current_text_edit, QTextEdit):
            current_text_edit.copy()
            self.status_bar.showMessage("Text Copied")

    def text_paste(self):
        current_text_edit = self.tab_widget.currentWidget()
        if isinstance(current_text_edit, QTextEdit):
            current_text_edit.paste()
            self.status_bar.showMessage("Text Pasted")

    def text_undo(self):
        current_text_edit = self.tab_widget.currentWidget()
        if isinstance(current_text_edit, QTextEdit):
            current_text_edit.undo()
            self.status_bar.showMessage("Undo")

    def text_redo(self):
        current_text_edit = self.tab_widget.currentWidget()
        if isinstance(current_text_edit, QTextEdit):
            current_text_edit.redo()
            self.status_bar.showMessage("Redo")

    def toggle_explorer(self, visible):
        self.explorer_panel.setVisible(visible)
        self.status_bar.showMessage(f"Explorer Panel: {'Visible' if visible else 'Hidden'}")

    def toggle_output(self, visible):
        self.output_panel.setVisible(visible)
        self.status_bar.showMessage(f"Output Panel: {'Visible' if visible else 'Hidden'}")

    def close_tab(self, index):
        """
        Closes the tab at the given index.
        """
        self.tab_widget.removeTab(index)
        self.status_bar.showMessage(f"Tab {index + 1} Closed") # Human-readable tab index

    def open_folder(self):
        """
        Opens a folder using tkinter's filedialog and sets it as the root for the Explorer panel.
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        folder_path = filedialog.askdirectory(title="Open Folder")
        if folder_path:
            self.file_system_model.setRootPath(folder_path)
            self.explorer_tree.setRootIndex(self.file_system_model.index(folder_path))
            self.status_bar.showMessage(f"Opened folder: {folder_path}")
        else:
            self.status_bar.showMessage("No folder selected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vscode_clone = VSCodeClone()
    vscode_clone.show()
    sys.exit(app.exec())
