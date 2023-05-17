import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget

class FFMpegGifConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.gifLay = QVBoxLayout()

        self.directory_label = QLabel("Dossier d'images:")
        self.gifLay.addWidget(self.directory_label)

        self.directory_line_edit = QLineEdit()
        self.gifLay.addWidget(self.directory_line_edit)

        self.browse_button = QPushButton('Parcourir...')
        self.gifLay.addWidget(self.browse_button)
        self.browse_button.clicked.connect(self.browse_directory)

        self.fps_label = QLabel("FPS:")
        self.gifLay.addWidget(self.fps_label)

        self.fps_line_edit = QLineEdit()
        self.gifLay.addWidget(self.fps_line_edit)

        self.scale_label = QLabel("Échelle (largeur):-1")
        self.gifLay.addWidget(self.scale_label)

        self.scale_line_edit = QLineEdit()
        self.gifLay.addWidget(self.scale_line_edit)

        self.output_label = QLabel("Nom du fichier de sortie (GIF):")
        self.gifLay.addWidget(self.output_label)

        self.output_line_edit = QLineEdit()
        self.gifLay.addWidget(self.output_line_edit)

        self.convert_button = QPushButton('Convertir')
        self.gifLay.addWidget(self.convert_button)
        self.convert_button.clicked.connect(self.convert_images)

        self.setLayout(self.gifLay)

        self.setWindowTitle("Convertisseur d'images en GIF - FFMpeg")

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Sélectionnez un dossier d'images")
        if directory:
            self.directory_line_edit.setText(directory)

    def convert_images(self):
        directory = self.directory_line_edit.text()
        fps = self.fps_line_edit.text()
        scale = self.scale_line_edit.text()
        output = self.output_line_edit.text()

        if not all([directory, fps, scale, output]):
            print("Veuillez remplir tous les champs.")
            return

        cmd = f'ffmpeg -i "{os.path.join(directory, "pic%04.png")}" -vf "fps={fps},scale={scale}:-1:flags=lanczos" -c:v gif "{output}"'
        subprocess.run(cmd, shell=True)
        print("Conversion terminée.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = FFMpegGifConverter()
    main_window.show()
    sys.exit(app.exec_())
