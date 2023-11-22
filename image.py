from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap, QImageReader, QFont
from PyQt5.QtCore import Qt, QDir, QFileInfo
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(350, 100, 1000, 700)
        self.setWindowIcon(QIcon('icon.png'))

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFixedSize(1000, 600)  

        openBtn = QPushButton('Browse')
        openBtn.clicked.connect(self.open_folder)
        self.prevBtn = QPushButton('Previous')
        self.prevBtn.setEnabled(False)
        self.prevBtn.clicked.connect(self.play_previous_image)
        self.nextBtn = QPushButton('Next')
        self.nextBtn.setEnabled(False)
        self.nextBtn.clicked.connect(self.display_next_image)

        self.label = QTextEdit() 
        self.label.setFixedHeight(50)  
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label.setStyleSheet("color:white ; background-color:black;")  
        self.label.setReadOnly(True)
        self.label.setAlignment(Qt.AlignCenter)  


        font = self.label.font()
        font.setPointSize(10)  
        self.label.setFont(font)

        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.nextBtn)
        hboxLayout.addWidget(self.prevBtn)
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.imageLabel)
        vboxLayout.addWidget(self.label)  
        vboxLayout.addLayout(hboxLayout)

        self.setLayout(vboxLayout)

        self.current_index = 0
        self.image_files = []

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.image_files = self.get_supported_image_files(folder_path)
            if self.image_files:
                self.current_index = 0
                self.nextBtn.setEnabled(True)
                self.prevBtn.setEnabled(True)
                self.display_next_image()
                self.update_current_image_label()

    def display_next_image(self):
        if self.image_files:
            if self.current_index < len(self.image_files):
                image_path = self.image_files[self.current_index]
                pixmap = self.load_image(image_path)
                self.imageLabel.setPixmap(pixmap)
                self.current_index += 1
                if self.current_index >= len(self.image_files):
                    self.current_index = 0
                self.update_current_image_label()

    def play_previous_image(self):
        if self.image_files:
            self.current_index -= 2  
            if self.current_index < 0:
                self.current_index = len(self.image_files) - 1
            self.display_next_image()
            self.update_current_image_label()

    def get_supported_image_files(self, folder_path):
        supported_formats = {'jpeg', 'png'}
        files = QDir(folder_path).entryInfoList()
        image_files = [file.absoluteFilePath() for file in files if file.suffix().lower() in supported_formats]
        return image_files
    
    def update_current_image_label(self):
        if self.current_index < len(self.image_files):
            file_info = QFileInfo(self.image_files[self.current_index-1])
            image_name = file_info.fileName()
            self.label.setText("Now Displaying: " + image_name)

    def load_image(self, image_path):
        reader = QImageReader(image_path)
        reader.setAutoTransform(True)
        image = reader.read()
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
