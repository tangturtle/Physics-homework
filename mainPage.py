from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton


class mainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.btn1 = QPushButton("同方向同频率的简谐振合成", self)
        self.btn2 = QPushButton("李萨如图形", self)

        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)

        self.setLayout(self.layout)
