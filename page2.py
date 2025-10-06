# page2.py
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib as mpl

class Page2(QWidget):
    return_to_main = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # 主垂直布局
        self.layout = QVBoxLayout(self)

        # 1. 图像区域
        self.canvas = FigureCanvas(Figure(figsize=(5,5)))
        self.ax = self.canvas.figure.subplots()
        self.layout.addWidget(self.canvas)

        # 2. x 方向公式标签
        self.label_x_formula = QLabel(self)
        self.layout.addWidget(self.label_x_formula)

        # 3. w_x + 滑块
        h_wx = QHBoxLayout()
        h_wx.addWidget(QLabel("ωₓ:", self))
        self.slider_wx = QSlider(Qt.Orientation.Horizontal)
        self.slider_wx.setMinimum(1)
        self.slider_wx.setMaximum(50)
        self.slider_wx.setSingleStep(1)
        h_wx.addWidget(self.slider_wx)
        self.layout.addLayout(h_wx)

        # 4. φ_x + 滑块
        h_phix = QHBoxLayout()
        h_phix.addWidget(QLabel("φₓ:", self))
        self.slider_phix = QSlider(Qt.Orientation.Horizontal)
        self.slider_phix.setMinimum(0)
        self.slider_phix.setMaximum(628)  # 映射 0 ~ 2π (比如乘 100)
        self.slider_phix.setSingleStep(1)
        h_phix.addWidget(self.slider_phix)
        self.layout.addLayout(h_phix)

        # 5. y 方向公式标签
        self.label_y_formula = QLabel(self)
        self.layout.addWidget(self.label_y_formula)

        # 6. w_y + 滑块
        h_wy = QHBoxLayout()
        h_wy.addWidget(QLabel("ωᵧ:", self))
        self.slider_wy = QSlider(Qt.Orientation.Horizontal)
        self.slider_wy.setMinimum(1)
        self.slider_wy.setMaximum(50)
        self.slider_wy.setSingleStep(1)
        h_wy.addWidget(self.slider_wy)
        self.layout.addLayout(h_wy)

        # 7. φ_y + 滑块
        h_phiy = QHBoxLayout()
        h_phiy.addWidget(QLabel("φᵧ:", self))
        self.slider_phiy = QSlider(Qt.Orientation.Horizontal)
        self.slider_phiy.setMinimum(0)
        self.slider_phiy.setMaximum(628)
        self.slider_phiy.setSingleStep(1)
        h_phiy.addWidget(self.slider_phiy)
        self.layout.addLayout(h_phiy)

        # 8. 返回按钮
        self.btn_back = QPushButton("返回主页面", self)
        self.btn_back.clicked.connect(self.on_back_clicked)
        self.layout.addWidget(self.btn_back)

        # 连接滑块信号
        self.slider_wx.valueChanged.connect(self.on_slider_changed)
        self.slider_phix.valueChanged.connect(self.on_slider_changed)
        self.slider_wy.valueChanged.connect(self.on_slider_changed)
        self.slider_phiy.valueChanged.connect(self.on_slider_changed)

        # 初始化滑块默认值
        self.slider_wx.setValue(1)
        self.slider_phix.setValue(0)
        self.slider_wy.setValue(1)
        self.slider_phiy.setValue(0)

        # 初次更新公式和绘图
        self.update_all()

        self.setLayout(self.layout)

    def on_back_clicked(self):
        self.return_to_main.emit()

    def on_slider_changed(self, _):
        self.update_all()

    def update_all(self):
        wx = self.slider_wx.value()
        phix = self.slider_phix.value() / 100.0
        wy = self.slider_wy.value()
        phiy = self.slider_phiy.value() / 100.0

        # 更新公式标签（使用 MathText 风格字符串）
        # 注意 QLabel 默认可能不渲染 LaTeX，要把公式画在 matplotlib 上会更可靠
        self.label_x_formula.setText(f"x = sin({wx:.2f}t + {phix:.2f})")
        self.label_y_formula.setText(f"y = sin({wy:.2f}t + {phiy:.2f})")

        self.plot_lissajous(wx, wy, phix, phiy)

    def plot_lissajous(self, wx, wy, phix, phiy, t=None):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['axes.unicode_minus'] = False

        if t is None:
            t = np.linspace(0, 2 * np.pi, 1000)

        x = np.sin(wx * t + phix)
        y = np.sin(wy * t + phiy)

        self.ax.clear()
        self.ax.plot(x, y, '-')

        # 坐标轴样式
        self.ax.grid(False)
        ax = self.ax
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['left'].set_linewidth(1.2)

        # 刻度处理，去除零刻度重复
        xticks = ax.get_xticks()
        yticks = ax.get_yticks()
        xticks = [v for v in xticks if abs(v) > 1e-8]
        yticks = [v for v in yticks if abs(v) > 1e-8]
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        # 原点 “0”
        ax.text(-0.05, -0.05, '0', ha='right', va='top', fontsize=10)

        # 坐标轴标签
        ax.set_xlabel('x')
        ax.xaxis.set_label_coords(1.0, 0.54)
        ax.set_ylabel('y')
        ax.yaxis.set_label_coords(0.52, 1.0)

        self.canvas.draw()
