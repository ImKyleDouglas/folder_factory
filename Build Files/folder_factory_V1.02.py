import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QGroupBox, QProgressBar
from PyQt5.QtCore import QRegExp, Qt, QPoint
from PyQt5.QtGui import QIcon, QRegExpValidator
import qdarkstyle
from resources_rc import *

class FolderFactory(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hides the default titlebar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Window title, icon, and size
        self.setWindowTitle('Folder Factory')
        self.setWindowIcon(QIcon(':/Folder_Open.ico'))
        self.resize(400, 280)
        self.center_window()

        # Set default settings
        self.folder_path = ''
        self.prefix_input = ''
        self.suffix_input = ''
        self.num_input = ''

        # Setup and show user interface
        self.setup_titlebar()
        self.setup_ui()
        self.show()

    def setup_titlebar(self):
        # Create a central widget and set the layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title bar widget
        self.title_bar = QWidget(self)
        self.title_bar.setObjectName("TitleBar")
        self.title_bar.setFixedHeight(32)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QIcon(':/Folder_Open.ico').pixmap(24, 24))
        title_layout.addWidget(self.icon_label)

        self.title_label = QLabel("Folder Factory")
        self.title_label.setStyleSheet("color: white;")
        title_layout.addWidget(self.title_label)

        title_layout.addStretch()

        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(24, 24)
        self.minimize_button.setStyleSheet(
            "QPushButton { color: white; background-color: transparent; }"
            "QPushButton:hover { background-color: red; }"
        )
        title_layout.addWidget(self.minimize_button)

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet(
            "QPushButton { color: white; background-color: transparent; }"
            "QPushButton:hover { background-color: red; }"
        )
        title_layout.addWidget(self.close_button)

        title_layout.setAlignment(Qt.AlignRight)

        self.minimize_button.clicked.connect(self.showMinimized)
        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.title_bar, 0, Qt.AlignTop)

        # Initialize variables for dragging
        self.draggable = False
        self.offset = QPoint()

    # Mouse events allow the title bar to be dragged around
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() <= self.title_bar.height():
            self.draggable = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            if event.buttons() & Qt.LeftButton:
                self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False
        
    def setup_ui(self):
        # Create group box
        self.group_box = QGroupBox('Folder Creator', self)
        self.group_box.setGeometry(10, 45, self.width() - 20, self.height() - 50)

        vbox_folder_creator = QVBoxLayout()

        hbox_folder_select = QHBoxLayout()
        # Create folder select button
        self.folder_select_button = QPushButton('Select Folder Location')
        self.folder_select_button.clicked.connect(self.select_folder)
        hbox_folder_select.addWidget(self.folder_select_button)

        vbox_folder_creator.addLayout(hbox_folder_select)

        hbox_folder_label = QHBoxLayout()
        # Create folder label
        self.folder_label = QLabel(self.folder_path)
        hbox_folder_label.addWidget(self.folder_label)

        vbox_folder_creator.addLayout(hbox_folder_label)

        hbox_prefix_layout = QHBoxLayout()
        # Folder prefix input
        prefix_label = QLabel('Folder Prefix:')
        hbox_prefix_layout.addWidget(prefix_label)
        self.prefix_input = QLineEdit()
        # Create QRegExp that matches any character that is not alphanumeric or \ / : * ? " < > |
        regex = QRegExp("[^\\\\/:*?\"<>|]+")
        validator = QRegExpValidator(regex)
        self.prefix_input.setValidator(validator)
        self.prefix_input.textChanged.connect(self.update_output_label)
        hbox_prefix_layout.addWidget(self.prefix_input)

        vbox_folder_creator.addLayout(hbox_prefix_layout)
        
        hbox_num_layout = QHBoxLayout()
        # Number of folders input
        num_label = QLabel('Number of Folders:')
        hbox_num_layout.addWidget(num_label)
        self.num_input = QLineEdit()
        regex = QRegExp('[0-9]*')  # regular expression to allow only numbers
        validator = QRegExpValidator(regex)
        self.num_input.setValidator(validator)
        self.num_input.textChanged.connect(self.update_output_label)
        hbox_num_layout.addWidget(self.num_input)
        
        vbox_folder_creator.addLayout(hbox_num_layout)

        hbox_suffix_layout = QHBoxLayout()
        # Folder suffix input
        suffix_label = QLabel('Folder Suffix:')
        hbox_suffix_layout.addWidget(suffix_label)
        self.suffix_input = QLineEdit()
        # Create QRegExp that matches any character that is not alphanumeric or \ / : * ? " < > |
        regex = QRegExp("[^\\\\/:*?\"<>|]+")
        validator = QRegExpValidator(regex)
        self.suffix_input.setValidator(validator)
        self.suffix_input.textChanged.connect(self.update_output_label)
        hbox_suffix_layout.addWidget(self.suffix_input)

        vbox_folder_creator.addLayout(hbox_suffix_layout)

        hbox_output_label = QHBoxLayout()
        # Create output label
        self.output_label = QLabel('Output Example: ')
        hbox_output_label.addWidget(self.output_label)

        vbox_folder_creator.addLayout(hbox_output_label)
        
        hbox_create_button = QHBoxLayout()
        # Create folders button
        self.create_button = QPushButton('Create Folders')
        self.create_button.clicked.connect(self.create_folders)
        self.create_button.setEnabled(False)
        hbox_create_button.addWidget(self.create_button)

        vbox_folder_creator.addLayout(hbox_create_button)

        hbox_progress_bar = QHBoxLayout()
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        hbox_progress_bar.addWidget(self.progress_bar)

        vbox_folder_creator.addLayout(hbox_progress_bar)

        self.group_box.setLayout(vbox_folder_creator)

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def select_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, 'Select Music Folder'))
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.setText(self.folder_path)
            self.progress_bar.setValue(0)
            self.valid_input()

    def update_output_label(self):
        prefix = self.prefix_input.text()
        num_folders = self.num_input.text()
        suffix = self.suffix_input.text()
        #Change label name
        folder_name = f'Output Example: {prefix}{num_folders}{suffix}'
        self.output_label.setText(folder_name)
        #Check if create button can be enabled
        self.valid_input()

    def valid_input(self):
        if self.folder_path and self.num_input.text():
            self.create_button.setEnabled(True)
        else:
            self.create_button.setEnabled(False)

    def create_folders(self):
        prefix = self.prefix_input.text()
        num_folders = int(self.num_input.text().strip())
        suffix = self.suffix_input.text()

        for i in range(1, num_folders + 1):
            folder_number = str(i).zfill(len(str(num_folders)))  # convert i to a string and pad with leading zeros
            folder_name = f'{prefix}{folder_number}{suffix}'
            folder_path = os.path.join(self.folder_path, folder_name)
            os.makedirs(folder_path)
            # Update progress bar
            self.progress_bar.setValue(int((i + 1) / num_folders * 100))

        self.prefix_input.setText('')
        self.num_input.setText('')
        self.suffix_input.setText('')
        self.output_label.setText('')
        self.folder_path = ''
        self.folder_label.setText(self.folder_path)
        self.create_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    folder_factory = FolderFactory()
    app.exec_()
