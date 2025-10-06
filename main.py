import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget

from page1 import Page1
from page2 import Page2
from mainPage import mainPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("物理")
        self.setGeometry(450, 250, 800, 600)

        # 主布局
        self.layout = QVBoxLayout(self)

        # 创建堆栈控件
        self.stack = QStackedWidget(self)
        self.layout.addWidget(self.stack)

        # 创建页面
        self.main_page = mainPage(self)
        self.page1 = Page1(self)
        self.page2 = Page2(self)

        # 把各个页面加入 stack
        self.stack.addWidget(self.main_page)  # index 0
        self.stack.addWidget(self.page1)  # index 1
        self.stack.addWidget(self.page2)  # index 2

        # 默认显示主页面
        self.stack.setCurrentIndex(0)

        # 连接主页面按钮信号到切换方法
        self.main_page.btn1.clicked.connect(self.show_page1)
        self.main_page.btn2.clicked.connect(self.show_page2)

        self.page1.return_to_main.connect(self.show_main_page)
        self.page2.return_to_main.connect(self.show_main_page)

    def show_main_page(self):
        self.stack.setCurrentWidget(self.main_page)
    def show_page1(self):

        self.stack.setCurrentWidget(self.page1)
    def show_page2(self):
        self.stack.setCurrentWidget(self.page2)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
