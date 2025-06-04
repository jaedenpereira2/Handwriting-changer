import sys
import pytesseract
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget,
    QFileDialog, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from handright import Template, handwrite
from PIL import Image, ImageFont
import os

class HandwritingChangerAI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Handwriting Changer - Phase 2 (AI Style)")
        self.setGeometry(100, 100, 900, 700)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.image_label = QLabel("Upload a handwritten image")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        upload_btn = QPushButton("Upload Image")
        upload_btn.clicked.connect(self.upload_image)
        button_layout.addWidget(upload_btn)

        self.style_box = QComboBox()
        self.style_box.addItems(["Light", "Medium", "Messy"])
        button_layout.addWidget(self.style_box)

        render_btn = QPushButton("Render AI Handwriting")
        render_btn.clicked.connect(self.render_handwriting)
        button_layout.addWidget(render_btn)

        layout.addLayout(button_layout)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.img_path = path
            self.image_label.setPixmap(QPixmap(path).scaled(800, 400, Qt.KeepAspectRatio))
            text = pytesseract.image_to_string(path)
            self.text_edit.setText(text)

    def render_handwriting(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            text = "This is a sample text.\nTry uploading a clearer image!"

        style = self.style_box.currentText()

        font_path = "handwriting_font.ttf"
        if not os.path.exists(font_path):
            print("Font file missing:", font_path)
            return
        font = ImageFont.truetype(font_path, 32)

        # Create a white background image for the template
        background = Image.new("RGB", (800, 1200), "white")

        if style == "Light":
            template = Template(
                background=background,
                font=font,
                line_spacing=45,
                fill=0,
                left_margin=20,
                top_margin=20,
                right_margin=20,
                bottom_margin=20,
                word_spacing=1.5,
                line_spacing_sigma=1,
                font_size_sigma=1,
                word_spacing_sigma=0.2,
                end_chars="，。：；！?",
            )
        elif style == "Medium":
            template = Template(
                background=background,
                font=font,
                line_spacing=45,
                fill=0,
                left_margin=20,
                top_margin=20,
                right_margin=20,
                bottom_margin=20,
                word_spacing=1.5,
                line_spacing_sigma=2,
                font_size_sigma=2,
                word_spacing_sigma=0.5,
                end_chars="，。：；！?",
            )
        else:  # Messy
            template = Template(
                background=background,
                font=font,
                line_spacing=45,
                fill=0,
                left_margin=20,
                top_margin=20,
                right_margin=20,
                bottom_margin=20,
                word_spacing=1.8,
                line_spacing_sigma=3,
                font_size_sigma=3,
                word_spacing_sigma=1,
                end_chars="，。：；！?",
            )

        images = list(handwrite(text, template))
        if not images:
            print("No rendered images generated.")
            return

        total_height = sum([img.height for img in images]) + 20
        final_img = Image.new("RGB", (800, total_height), "white")
        y = 0
        for img in images:
            final_img.paste(img, (20, y))
            y += img.height

        out_path = "rendered_output_ai.png"
        final_img.save(out_path)
        self.image_label.setPixmap(QPixmap(out_path).scaled(800, 400, Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandwritingChangerAI()
    window.show()
    sys.exit(app.exec_())
