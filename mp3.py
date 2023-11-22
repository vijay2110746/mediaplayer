from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5.QtCore import Qt, QUrl, QDir,QFileInfo
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MP3 Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('icon.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        
        videowidget = QLabel()
        videowidget.setAlignment(Qt.AlignCenter)
        videowidget.setStyleSheet("border: 2px solid white;")  
        videowidget.setPixmap(QPixmap("C:\\Users\\vijay\\OneDrive - SSN Trust\\Desktop\\sem 5\\meister gen\\icon.png"))
        openBtn = QPushButton('Browse')
        openBtn.clicked.connect(self.open_file)
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
    
        self.prevBtn = QPushButton('Previous')
        self.prevBtn.setEnabled(False)
        self.prevBtn.clicked.connect(self.play_previous_video)
        self.nextBtn = QPushButton('Next')
        self.nextBtn.setEnabled(False)
        self.nextBtn.clicked.connect(self.play_next_video)

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
        self.label.setStyleSheet("color:white;")

        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.nextBtn)
        hboxLayout.addWidget(self.prevBtn)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.volumeBtn)
        hboxLayout.addWidget(self.volumeSlider)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        self.setLayout(vboxLayout)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.current_index = 0
        self.media_files = []

    def open_file(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.media_files = self.get_supported_media_files(folder_path)
            if self.media_files:
                self.current_index = 0
                self.playBtn.setEnabled(True)
                self.nextBtn.setEnabled(True)
                self.prevBtn.setEnabled(True)
                self.play_next_video()

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def play_next_video(self):
        if self.media_files:
            if self.current_index < len(self.media_files):
                file_url = QUrl.fromLocalFile(self.media_files[self.current_index])
                self.mediaPlayer.setMedia(QMediaContent(file_url))
                self.mediaPlayer.play()
                self.current_index += 1
                if self.current_index >= len(self.media_files):
                    self.current_index = 0
                self.update_current_audio_label()  
            else:
                self.current_index = 0
                self.mediaPlayer.stop()
    def play_previous_video(self):
        if self.media_files:
            self.current_index -= 2  
            if self.current_index < 0:
                self.current_index = len(self.media_files) - 1
            self.play_next_video()
            self.update_current_audio_label()

    def update_current_audio_label(self):
        if self.current_index < len(self.media_files):
            file_info = QFileInfo(self.media_files[self.current_index-1])
            audio_name = file_info.fileName()
            self.label.setText("Now Playing: " + audio_name)

    def get_supported_media_files(self, folder_path):
        supported_formats = {'mp3', 'wav'}
        files = QDir(folder_path).entryInfoList()
        media_files = [file.absoluteFilePath() for file in files if file.suffix().lower() in supported_formats]
        return media_files

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


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
