import os, markdown, sys
from pydub import AudioSegment
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMessageBox

from arw2Jpg import ConverterApp
from resizer import ImageResizer
from batchGround import remBackBatch
from giffer import FFMpegGifConverter
from pixelizer import pixelize


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main Page')
        

        self.batchbackground_button = QPushButton('Supprimer l\'arrière-plan')
        self.batchbackground_button.clicked.connect(self.open_batchbackground)

        self.resizer_button = QPushButton('Redimensionner')
        self.resizer_button.clicked.connect(self.open_resizer)

        self.arw2jpg_button = QPushButton('Convertir ARW en JPG')
        self.arw2jpg_button.clicked.connect(self.open_arw2jpg)

        self.pixelizer_button = QPushButton('Pixeliser')
        self.pixelizer_button.clicked.connect(self.open_pixelizer)

        self.ffmpeggifconverter_button = QPushButton('Convertir en GIF')
        self.ffmpeggifconverter_button.clicked.connect(self.open_ffmpeggifconverter)

        self.md2html_button = QPushButton('Convertir Markdown en HTML')
        self.md2html_button.clicked.connect(self.md2html)

        self.mp32wav_button = QPushButton('Convertir MP3 en WAV')
        self.mp32wav_button.clicked.connect(self.mp3_wav)

        layout = QVBoxLayout()
        layout.addWidget(self.batchbackground_button)
        layout.addWidget(self.resizer_button)
        layout.addWidget(self.arw2jpg_button)
        layout.addWidget(self.pixelizer_button)
        layout.addWidget(self.ffmpeggifconverter_button)
        layout.addWidget(self.md2html_button)
        layout.addWidget(self.mp32wav_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_batchbackground(self):
        self.batchbackground_window = remBackBatch()
        self.batchbackground_window.show()

    def open_resizer(self):
        self.resizer_window = ImageResizer()
        self.resizer_window.show()

    def open_arw2jpg(self):
        self.arw2jpg_window = ConverterApp()
        self.arw2jpg_window.show()

    def open_pixelizer(self):
        self.pixelizer_window = pixelize()
        self.pixelizer_window.show()

    def open_ffmpeggifconverter(self):
        self.ffmpeggifconverter_window = FFMpegGifConverter()
        self.ffmpeggifconverter_window.show()

    def md2html(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Markdown files (*.md);;All files (*.*)')

        if fname:
            with open(fname, 'r', encoding='utf-8') as file:
                content = file.read()

            html = markdown.markdown(content)

            new_file_name = "md_" + os.path.basename(fname).split(".")[0] + ".html"
            new_file_path = os.path.join(os.path.dirname(fname), new_file_name)

            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(html)

            QMessageBox.information(self, 'Conversion réussie', 'Le fichier a été converti et sauvegardé sous le nom : ' + new_file_name)

    def mp3_wav(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly 
        folder = QFileDialog.getExistingDirectory(self, "Sélectionnez un dossier", "", options=options) 

        if folder: 
            for filename in os.listdir(folder):
                if filename.endswith(".mp3"):
                    mp3_file = AudioSegment.from_file(os.path.join(folder, filename), "mp3")
                    wav_file = mp3_file.export(os.path.join(folder, f"{os.path.splitext(filename)[0]}.wav"), format="wav")

            QMessageBox.information(self, 'Conversion réussie', 'Les fichiers MP3 ont été convertis en WAV.')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Charge le style depuis le fichier
    with open('style.txt', 'r') as file:
        style = file.read()

    # Applique le style à l'application
    app.setStyleSheet(style)

    main_page = MainPage()
    main_page.show()

    sys.exit(app.exec_())
