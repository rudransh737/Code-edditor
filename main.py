import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QToolBar, QToolButton, QSplitter, QTabWidget,
    QStatusBar, QDockWidget, QListWidget, QListWidgetItem,
    QTabBar, QTreeView, QMenuBar, QMenu,QFileDialog,QPushButton,QInputDialog,
    QLineEdit, # Added QLineEdit for terminal input
    QMessageBox # Added QMessageBox for error popups
)
from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtCore import Qt, QSize, QDir, QModelIndex
from PySide6.QtWidgets import QFileSystemModel
import os
import subprocess

class ExplorerTreeView(QTreeView):
    def __init__(self, parent=None, open_file_callback=None):
        super().__init__(parent)
        self.open_file_callback = open_file_callback

    def mousePressEvent(self, event):
        # Handle middle-click to open file
        if event.button() == Qt.MouseButton.MiddleButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                model = self.model()
                if isinstance(model, QFileSystemModel):
                    file_path = model.filePath(index)
                    # Check if it's a file and call the callback
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
                color: #e0e0e0;            /* Light text */
            }
            QTextEdit {
                background-color: #1e1e1e; /* Darker text area background */
                color: #ffffff;
                border: 1px solid #333;
                font-family: 'Consolas', monospace; /* Use a monospace font */
                font-size: 14px;
            }
            QLineEdit { /* Style for the new QLineEdit */
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #333;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                padding: 5px;
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
                color: #b0b0b0;            /* Light gray text for menu titles */
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
                color: #ffffff;            /* White text on hover */
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
                border-radius: 4px;        /* Slightly rounded corners for the dropdown */
                padding: 5px;              /* Padding inside the dropdown */
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
                color: #ffffff;            /* White text on hover */
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
            QPushButton {
                background-color: #007acc; /* VS Code blue */
                color: #ffffff;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005f99; /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #004c7f; /* Even darker blue on press */
            }
        """)
        self.create_file_explorer()
        self.create_output_panel()
        self.create_code_area()
        self.create_menu_bar()
        self.create_status_bar()

    def create_file_explorer(self):
        # Create a dockable panel for the file explorer
        self.explorer_panel = QDockWidget("Explorer", self)
        self.explorer_panel.setObjectName("ExplorerPanel")

        # Set up the file system model
        self.file_system_model = QFileSystemModel()
        # Set root path to user's home directory
        self.file_system_model.setRootPath(QDir.homePath())

        # Create the tree view for the explorer, passing a callback for opening files
        self.explorer_tree = ExplorerTreeView(open_file_callback=self.open_file_in_tab)
        self.explorer_tree.setModel(self.file_system_model)
        # Set the root index to the home directory for display
        self.explorer_tree.setRootIndex(self.file_system_model.index(QDir.homePath()))
        self.explorer_panel.setWidget(self.explorer_tree)

        # Add the explorer panel to the left dock area of the main window
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorer_panel)

        # Hide unnecessary columns (like size, type, date modified) in the tree view
        for i in range(1, self.file_system_model.columnCount()):
            self.explorer_tree.setColumnHidden(i, True)

    def open_file_in_tab(self, file_path):
        """
        Opens the content of a given file path in a new tab in the code area.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            editor = QTextEdit()
            editor.setText(content)
            base_name = os.path.basename(file_path)
            self.tab_widget.addTab(editor, base_name)
            self.tab_widget.setCurrentWidget(editor)
            self.status_bar.showMessage(f"Opened: {base_name}", 3000) # Show message for 3 seconds
        except Exception as e:
            # Show an error message box if file cannot be opened
            QMessageBox.warning(self, "Error Opening File", f"Could not open file: {file_path}\nError: {e}")
            self.status_bar.showMessage(f"Error opening file: {os.path.basename(file_path)}", 3000)


    def create_output_panel(self):
        # Create a dockable panel for the terminal output
        self.output_panel = QDockWidget("Terminal", self) # Renamed to Terminal
        self.output_panel.setObjectName("OutputPanel")

        # Output text area (read-only)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        # Apply terminal-like styling
        self.output_text.setStyleSheet("background-color: #000000; color: #00ff00; font-family: 'Consolas', monospace; font-size: 12px;")

        # Input line edit for commands
        self.input_line = QLineEdit() # Changed from QTextEdit to QLineEdit
        self.input_line.setPlaceholderText("Enter command here...")
        # Connect the Enter key press to execute the command
        self.input_line.returnPressed.connect(self.execute_terminal_command)

        # Clear button for the output
        self.clear_output_button = QPushButton("Clear Terminal")
        self.clear_output_button.clicked.connect(self.output_text.clear) # Connect to clear the output text
        self.clear_output_button.setFixedHeight(30) # Make button a bit smaller

        # Layout for input line and clear button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.clear_output_button)
        input_layout.setStretch(0, 1) # Make input line expand to fill available space

        # Combined layout for output text and input/button layout
        self.combined_layout = QVBoxLayout()
        self.combined_layout.addWidget(self.output_text)
        self.combined_layout.addLayout(input_layout) # Add the input layout

        # Create a widget to hold the combined layout and set it as the dock widget's content
        self.output_widget = QWidget()
        self.output_widget.setLayout(self.combined_layout)
        self.output_panel.setWidget(self.output_widget)
        # Add the terminal panel to the bottom dock area
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.output_panel)

    def execute_terminal_command(self):
        """
        Executes the command entered in the input line and displays its output
        in the output text area.
        """
        command = self.input_line.text().strip() # Get command from QLineEdit and strip whitespace
        self.input_line.clear() # Clear the input line immediately after getting the command

        if not command:
            return # Do nothing if the command is empty

        # Display the command itself in gray in the output
        self.output_text.append(f"<span style='color: #888888;'>$ {command}</span>")

        try:
            # Run the command using subprocess.
            # shell=True allows execution of shell commands (like 'ls -l', 'grep', pipes).
            # capture_output=True captures stdout and stderr.
            # text=True decodes output as text (UTF-8 by default).
            # check=False means we handle non-zero exit codes manually, not by raising an exception.
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
                encoding='utf-8' # Explicitly set encoding for consistent output
            )

            # Append standard output if any
            if process.stdout:
                self.output_text.append(process.stdout)
            # Append standard error if any, styled in red
            if process.stderr:
                self.output_text.append(f"<span style='color: #ff6666;'>{process.stderr}</span>")

            # Indicate if the command exited with a non-zero (error) code, styled in orange
            if process.returncode != 0:
                self.output_text.append(f"<span style='color: #ffaa00;'>Command exited with code {process.returncode}</span>")
        except FileNotFoundError:
            # Handle case where the command executable itself is not found
            self.output_text.append(f"<span style='color: #ff6666;'>Error: Command '{command.split()[0]}' not found.</span>")
        except Exception as e:
            # Catch any other unexpected errors during subprocess execution
            self.output_text.append(f"<span style='color: #ff6666;'>An unexpected error occurred: {e}</span>")

        # Scroll the output text area to the very bottom to show the latest output
        self.output_text.verticalScrollBar().setValue(self.output_text.verticalScrollBar().maximum())


    def create_code_area(self):
        # Create a tab widget to hold multiple code editors
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True) # Allow tabs to be closed
        self.tab_widget.tabCloseRequested.connect(self.close_tab) # Connect signal for tab closing
        self.setCentralWidget(self.tab_widget) # Set the tab widget as the central widget

    def create_menu_bar(self):
        # Create the main menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar) # Set it as the main window's menu bar

        # Actions for showing/hiding explorer and terminal panels
        self.show_explorer_action = QAction("Show Explorer", self)
        self.show_explorer_action.setCheckable(True)
        self.show_explorer_action.setChecked(True) # Explorer is visible by default

        self.show_output_action = QAction("Show Terminal", self) # Renamed action for clarity
        self.show_output_action.setCheckable(True)
        self.show_output_action.setChecked(True) # Terminal is visible by default

        # File Menu
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction("Open Folder", self.open_folder)
        self.file_menu.addAction("New File", self.create_new_file)

        # Edit Menu
        self.edit_menu = self.menu_bar.addMenu("Edit")

        # Selection Menu
        self.selection_menu = self.menu_bar.addMenu("Selection")

        # View Menu (contains show/hide actions for panels)
        self.view_menu = self.menu_bar.addMenu("View")
        self.view_menu.addAction(self.show_explorer_action)
        self.view_menu.addAction(self.show_output_action)

        # Go Menu
        self.go_menu = self.menu_bar.addMenu("Go")

        # Run Menu
        self.run_menu = self.menu_bar.addMenu("Run")

        # Terminal Menu
        self.terminal_menu = self.menu_bar.addMenu("Terminal")
        # Action to show the terminal panel (it's already created, just show/hide)
        self.terminal_menu.addAction("New Terminal", lambda: self.output_panel.show())

        # Connect actions to toggle visibility of dock widgets
        self.show_explorer_action.toggled.connect(self.explorer_panel.setVisible)
        self.show_output_action.toggled.connect(self.output_panel.setVisible)

    def close_tab(self,index):
        """Closes the tab at the given index in the tab widget."""
        self.tab_widget.removeTab(index)

    def open_folder(self):
        """
        Opens a folder selected by the user in the file explorer.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", QDir.homePath())
        if folder_path:
            # Set the new root path for the file system model and tree view
            self.file_system_model.setRootPath(folder_path)
            self.explorer_tree.setRootIndex(self.file_system_model.index(folder_path))
            self.explorer_tree.expandAll() # Expand all directories in the new folder
            self.explorer_panel.setWindowTitle(os.path.basename(folder_path)) # Update panel title
            self.status_bar.showMessage(f"Opened folder: {os.path.basename(folder_path)}", 3000)

    def create_status_bar(self):
        """
        Creates and configures the status bar at the bottom of the main window.
        """
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Create various status buttons (currently placeholders)
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

        # List of all status bar widgets
        all_widgets = [self.go_to_line_col, self.select_indentaion, self.select_encoding, self.select_language_mode, self.notification]
        for widget in all_widgets:
            widget.setFixedHeight(25) # Set a fixed height for consistency
            self.status_bar.addPermanentWidget(widget) # Add widgets permanently to the right side

    def create_new_file(self):
        """
        Prompts the user for a new file name and creates an empty file
        in the currently selected folder in the explorer.
        """
        selected_folder_index = self.explorer_tree.currentIndex()
        # Determine the target folder path
        if not selected_folder_index.isValid() or not self.file_system_model.isDir(selected_folder_index):
            # If no valid folder is selected, use the current root path of the file system model
            folder_path = self.file_system_model.rootPath()
        else:
            # Otherwise, use the path of the selected folder
            folder_path = self.file_system_model.filePath(selected_folder_index)

        # Get file name from user via input dialog
        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and file_name:
            new_file_path = os.path.join(folder_path, file_name)
            try:
                # Create an empty file
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    pass
                self.status_bar.showMessage(f"Created new file: {file_name}", 3000)
                # Refresh the explorer tree to show the new file (by re-setting root path)
                self.file_system_model.setRootPath(self.file_system_model.rootPath())
                # Optionally open the new file in a tab
                self.open_file_in_tab(new_file_path)
            except Exception as e:
                # Show a critical error message box if file creation fails
                QMessageBox.critical(self, "Error Creating File", f"Could not create file: {new_file_path}\nError: {e}")
                self.status_bar.showMessage(f"Error creating file: {file_name}", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    code_edditor = Code_Edditor()
    code_edditor.show()
    sys.exit(app.exec())
