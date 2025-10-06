from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider )
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib as mpl

class Page1(QWidget):
    return_to_main = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.subplots()
        self.main_layout.addWidget(self.canvas)

        self.label_x1_formula = QLabel("", self)
        self.main_layout.addWidget(self.label_x1_formula)

        ha1 = QHBoxLayout()
        ha1.addWidget(QLabel("a1:", self))
        self.slider_a1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_a1.setMinimum(0)
        self.slider_a1.setMaximum(500)
        self.slider_a1.setSingleStep(1)
        ha1.addWidget(self.slider_a1)
        self.main_layout.addLayout(ha1)

        hphi1 = QHBoxLayout()
        hphi1.addWidget(QLabel("φ1:", self))
        self.slider_phi1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_phi1.setMinimum(0)
        self.slider_phi1.setMaximum(500)
        self.slider_phi1.setSingleStep(1)
        hphi1.addWidget(self.slider_phi1)
        self.main_layout.addLayout(hphi1)

        self.label_x2_formula = QLabel("", self)
        self.main_layout.addWidget(self.label_x2_formula)

        ha2 = QHBoxLayout()
        ha2.addWidget(QLabel("a2:", self))
        self.slider_a2 = QSlider(Qt.Orientation.Horizontal)
        self.slider_a2.setMinimum(0)
        self.slider_a2.setMaximum(500)
        self.slider_a2.setSingleStep(1)
        ha2.addWidget(self.slider_a2)
        self.main_layout.addLayout(ha2)

        hphi2 = QHBoxLayout()
        hphi2.addWidget(QLabel("φ2:", self))
        self.slider_phi2 = QSlider(Qt.Orientation.Horizontal)
        self.slider_phi2.setMinimum(0)
        self.slider_phi2.setMaximum(500)
        self.slider_phi2.setSingleStep(1)
        hphi2.addWidget(self.slider_phi2)
        self.main_layout.addLayout(hphi2)

        self.btn_back = QPushButton("返回主页面", self)
        self.btn_back.clicked.connect(self.on_back_clicked)
        self.main_layout.addWidget(self.btn_back)

        self.slider_a1.valueChanged.connect(self.on_slider_changed)
        self.slider_phi1.valueChanged.connect(self.on_slider_changed)
        self.slider_a2.valueChanged.connect(self.on_slider_changed)
        self.slider_phi2.valueChanged.connect(self.on_slider_changed)

        self.slider_a1.setValue(100)
        self.slider_phi1.setValue(0)
        self.slider_a2.setValue(100)
        self.slider_phi2.setValue(0)

        self.update_all()

        self.setLayout(self.main_layout)

    def on_back_clicked(self):
        self.return_to_main.emit()

    def on_slider_changed(self, _):
        self.update_all()

    def update_all(self):
        a1 = self.slider_a1.value() / 100.0
        phi1 = self.slider_phi1.value() / 100.0
        a2 = self.slider_a2.value() / 100.0
        phi2 = self.slider_phi2.value() / 100.0

        self.label_x1_formula.setText(f"x₁(t) = {a1:.2f} · cos(ωt + {phi1:.2f})")
        self.label_x2_formula.setText(f"x₂(t) = {a2:.2f} · cos(ωt + {phi2:.2f})")

        self.plot_superpose(a1, phi1, a2, phi2)

    def plot_superpose(self, a1, phi1, a2, phi2, omega=1.0, t=None):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['axes.unicode_minus'] = False

        if t is None:
            t = np.linspace(0, 2 * np.pi, 500)

        x1 = a1 * np.cos(omega * t + phi1)
        x2 = a2 * np.cos(omega * t + phi2)
        x = x1 + x2

        self.ax.clear()
        self.ax.plot(t, x1, '--', label='x1')
        self.ax.plot(t, x2, '--', label='x2')
        self.ax.plot(t, x, '-', label='x = x1 + x2')

        self.ax.grid(False)

        ax = self.ax
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['left'].set_linewidth(1.2)

        xticks = ax.get_xticks()
        yticks = ax.get_yticks()
        xticks = [val for val in xticks if abs(val) > 1e-8]
        yticks = [val for val in yticks if abs(val) > 1e-8]
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        ax.text(-0.05, -0.05, '0', ha='right', va='top', fontsize=10)

        ax.set_xlabel('t')
        ax.xaxis.set_label_coords(1.0, 0.56)
        ax.set_ylabel('x')
        ax.yaxis.set_label_coords(0.15, 1.0)

        ax.legend(loc='upper right')
        self.canvas.draw()
