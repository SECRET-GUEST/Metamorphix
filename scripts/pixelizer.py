import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QSpinBox, QLabel, QMessageBox
from PIL import Image

class pixelize(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.input_button = QPushButton('Select Input Folder')
        self.input_button.clicked.connect(self.select_input_folder)
        self.layout.addWidget(self.input_button)

        self.pixel_size_spinbox = QSpinBox()
        self.pixel_size_spinbox.setRange(1, 512)
        self.pixel_size_spinbox.setValue(12)
        self.layout.addWidget(QLabel("Pixel Size"))
        self.layout.addWidget(self.pixel_size_spinbox)

        self.output_button = QPushButton('Select Output Folder')
        self.output_button.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.output_button)

        self.launch_button = QPushButton('Launch pixelizer')
        self.launch_button.clicked.connect(self.launch_pixelizer)
        self.layout.addWidget(self.launch_button)

        self.setLayout(self.layout)

        self.input_folder = None
        self.output_folder = None

    def select_input_folder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder')

    def select_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')

    def launch_pixelizer(self):
        if self.input_folder is None or self.output_folder is None:
            QMessageBox.warning(self, 'Warning', 'Both input and output folders must be selected')
            return
        if os.path.commonpath([self.input_folder, self.output_folder]) == self.input_folder:
            QMessageBox.warning(self, 'Warning', 'Output folder must not be inside the input folder')
            return
        pixel_size = self.pixel_size_spinbox.value()
        self.pixelize_images(self.input_folder, self.output_folder, pixel_size)

    @staticmethod
    def pixelize_images(input_folder, output_folder, pixel_size):
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    input_path = os.path.join(root, file)
                    output_path = os.path.join(output_folder, file)
                    pixelize.pixelize_image(input_path, output_path, pixel_size)

    @staticmethod
    def pixelize_image(input_path, output_path, pixel_size):
        image = Image.open(input_path)
        rgb = image.convert('RGB')
        canvas = Image.new('RGB', image.size)

        pixel_size = min(pixel_size, image.size[0], image.size[1])

        for i in range(0, image.size[0], pixel_size):
            for j in range(0, image.size[1], pixel_size):
                if i < image.size[0] and j < image.size[1]:
                    pixel = rgb.getpixel((i, j))
                    for k in range(i, min(i + pixel_size, canvas.size[0])):
                        for l in range(j, min(j + pixel_size, canvas.size[1])):
                            canvas.putpixel((k, l), pixel)

        canvas.save(output_path)
