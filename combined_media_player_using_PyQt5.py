from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QGraphicsView, QGraphicsScene
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5.QtCore import Qt, QUrl, QDir, QFileInfo
import sys
import importlib
import os

class Mp3_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.w = None
        self.y = None
        self.setWindowTitle("Media Player")
        self.setGeometry(350, 100, 1200, 800)
        self.setWindowIcon(QIcon('icon.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.videowidget = QLabel()
        self.videowidget.setAlignment(Qt.AlignCenter)
        self.videowidget.setStyleSheet("border: 2px solid white;")
        self.videowidget.setPixmap(QPixmap("icon.png"))
        openBtn = QPushButton('Browse')
        openBtn.clicked.connect(self.open_file)
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_media)

        self.image_view = QGraphicsView(self)
        self.image_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.image_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = QGraphicsScene(self)
        self.image_item = self.scene.addPixmap(QPixmap())  
        self.image_view.setScene(self.scene)
         
        self.prevBtn = QPushButton('Previous')
        self.prevBtn.setEnabled(False)
        self.prevBtn.clicked.connect(self.play_previous_media)
        self.nextBtn = QPushButton('Next')
        self.nextBtn.setEnabled(False)
        self.nextBtn.clicked.connect(self.play_next_media)

        self.volumeBtn = QPushButton()
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeBtn.setToolTip("Volume")
        self.volumeBtn.clicked.connect(self.toggle_volume_control)
        self.volumeBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.set_volume)
        self.volumeSlider.setFixedWidth(80)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label.setStyleSheet("color:white; text-align:center; font-size:20px;")
        btnlay = QHBoxLayout()
        btnlay.addWidget(QPushButton('Video', clicked=self.handle1))
        btnlay.addWidget(QPushButton('Audio', clicked=self.handle))
        btnlay.addWidget(QPushButton('Image', clicked=self.handle))
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.prevBtn)
        hboxLayout.addWidget(self.nextBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.volumeBtn)
        hboxLayout.addWidget(self.volumeSlider)

        vboxLayout = QVBoxLayout()
        # vboxLayout.addLayout(btnlay)
        vboxLayout.addWidget(self.video_widget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        self.setLayout(vboxLayout)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.current_index = 0
        self.media_files = []

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Select File')
        f = file_path[0]
        r = ''
        l = []
        f = f.split('/')
        f = f[:len(f) - 1]
        folder_path = ''
        for i in f:
            if i != f[-1]:
                folder_path += i + "/"
            else:
                folder_path += i

        if folder_path:
            ind=0
            self.media_files = self.get_supported_media_files(folder_path)
            for i in range(len(self.media_files)):
                if self.media_files[i] == file_path[0]:
                    ind = i

            if self.media_files:
                self.current_index = ind
                print(self.current_index)
                self.playBtn.setEnabled(True)
                self.nextBtn.setEnabled(True)

                self.prevBtn.setEnabled(True)
                self.play_next_media()

    def play_media(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def play_next_media(self):
        if self.media_files:
            if self.current_index < len(self.media_files):
                file_url = QUrl.fromLocalFile(self.media_files[self.current_index])
                file_info = QFileInfo(self.media_files[self.current_index])
                file_ext = file_info.suffix().lower()

                if file_ext in ['mp4', 'avi', 'wmv', 'mov', 'mkv', 'flv']:
                    self.mediaPlayer.setVideoOutput(self.video_widget)
                    self.layout().replaceWidget(self.videowidget, self.video_widget)
                    self.layout().replaceWidget(self.image_view, self.video_widget)
                    self.videowidget.hide()
                    self.image_view.hide()
                    self.playBtn.show()
                    self.slider.show()
                    self.volumeBtn.show()
                    self.volumeSlider.show()
                    self.video_widget.show()
                    self.mediaPlayer.setMedia(QMediaContent(file_url))
                    self.mediaPlayer.play()
                elif file_ext in ['mp3', 'wav']:
                    self.mediaPlayer.setVideoOutput(None)
                    self.layout().replaceWidget(self.video_widget, self.videowidget)
                    self.layout().replaceWidget(self.image_view, self.videowidget)
                    self.video_widget.hide()
                    self.image_view.hide()
                    self.playBtn.show()
                    self.slider.show()
                    self.volumeBtn.show()
                    self.volumeSlider.show()
                    self.videowidget.show()
                    self.mediaPlayer.setMedia(QMediaContent(file_url))
                    self.mediaPlayer.play()
                else:
                    image_path = self.media_files[self.current_index]
                    self.layout().replaceWidget(self.video_widget,self.image_view)
                    self.layout().replaceWidget(self.videowidget,self.image_view)
                    self.playBtn.hide()
                    self.slider.hide()
                    self.volumeBtn.hide()
                    self.volumeSlider.hide()
                    self.video_widget.hide()
                    self.videowidget.hide()
                    self.mediaPlayer.pause()
                    self.image_view.show()
                    self.load_image(image_path)                    

                self.current_index += 1
                if self.current_index >= len(self.media_files):
                    self.current_index = 0

                self.update_current_media_label()
            else:
                self.current_index = 0
                self.mediaPlayer.stop()

    def play_previous_media(self):
        if self.media_files:
            self.current_index -= 2
            if self.current_index < 0:
                self.current_index = len(self.media_files) - 1
            self.play_next_media()
            self.update_current_media_label()

    def update_current_media_label(self):
        if self.current_index < len(self.media_files):
            file_info = QFileInfo(self.media_files[self.current_index - 1])
            media_name = file_info.fileName()
            self.label.setText("Now Playing: " + media_name)

    def get_supported_media_files(self, folder_path):
        supported_formats = {'mp4', 'mp3', 'wav', 'avi', 'wmv', 'mov', 'mkv', 'flv','jpeg', 'png', 'jpg'}
        media_files = []
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                file_extension = os.path.splitext(filename)[1][1:].lower()
                if file_extension in supported_formats:
                    media_files.append(filepath)
        return media_files

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.image_view.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_item.setPixmap(pixmap)

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)

    def toggle_volume_control(self):
        self.volumeSlider.setVisible(not self.volumeSlider.isVisible())

    def handle1(self, checked):
        h = importlib.import_module('main1')
        if self.w is None:
            self.w = h.Vdo_Window()
            self.close()
        self.w.show()

    def handle(self, checked):
        h = importlib.import_module('image')
        if self.y is None:
            self.y = h.Window()
            self.close()
        self.y.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(app)
    window = Mp3_Window()
    sys.exit(app.exec_())
