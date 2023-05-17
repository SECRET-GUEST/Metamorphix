import os
import rawpy
import imageio
from PyQt5.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QPushButton, QWidget, QRadioButton, QProgressBar, QLabel


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.vlayout = QVBoxLayout()

        self.select_directory_button = QPushButton('Choisir un dossier source', self)
        self.select_directory_button.clicked.connect(self.select_source_directory)

        self.select_output_directory_button = QPushButton('Choisir un dossier de sortie', self)
        self.select_output_directory_button.clicked.connect(self.select_output_directory)

        self.start_conversion_button = QPushButton('Commencer la conversion', self)
        self.start_conversion_button.clicked.connect(self.convert_images)
        self.start_conversion_button.setEnabled(False)

        self.jpg_button = QRadioButton("JPG")
        self.png_button = QRadioButton("PNG")
        self.tiff_button = QRadioButton("TIFF")

        self.jpg_button.setChecked(True)  # Par défaut, le format de sortie est JPG

        self.progress = QProgressBar(self)
        self.progress_label = QLabel('')

        self.vlayout.addWidget(self.select_directory_button)
        self.vlayout.addWidget(self.select_output_directory_button)
        self.vlayout.addWidget(self.start_conversion_button)
        self.vlayout.addWidget(self.jpg_button)
        self.vlayout.addWidget(self.png_button)
        self.vlayout.addWidget(self.tiff_button)
        self.vlayout.addWidget(self.progress_label)
        self.vlayout.addWidget(self.progress)

        self.setLayout(self.vlayout)

    def select_source_directory(self):
        self.source_directory = QFileDialog.getExistingDirectory(self, "Choisir un dossier source")
        if self.source_directory and hasattr(self, 'output_directory'):
            self.start_conversion_button.setEnabled(True)

    def select_output_directory(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, "Choisir un dossier de sortie")
        if self.output_directory and hasattr(self, 'source_directory'):
            self.start_conversion_button.setEnabled(True)

    def convert_images(self):
        if self.jpg_button.isChecked():
            output_format = 'jpg'
        elif self.png_button.isChecked():
            output_format = 'png'
        elif self.tiff_button.isChecked():
            output_format = 'tiff'
        else:
            print("Aucun format de sortie sélectionné.")
            return

        arw_files = [f for f in os.listdir(self.source_directory) if f.endswith((".ARW", ".arw"))]
        total_files = len(arw_files)

        self.progress.setMaximum(total_files)
        self.progress.setValue(0)

        for i, filename in enumerate(arw_files):
            raw_image_path = os.path.join(self.source_directory, filename)
            with rawpy.imread(raw_image_path) as raw:
                rgb = raw.postprocess()
            output_image_path = os.path.join(self.output_directory, f'{os.path.splitext(filename)[0]}.{output_format}')
            imageio.imsave(output_image_path, rgb)
            print(f"Image sauvegardée : {output_image_path}")

            self.progress.setValue(i + 1)
            self.progress_label.setText(f'Conversion en cours : {i + 1}/{total_files}')

        self.progress_label.setText('Conversion terminée !')


if __name__ == '__main__':
    app = QApplication([])
    converter = ConverterApp()
    converter.show()
    app.exec_()
