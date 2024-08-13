from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QMouseEvent, QIcon, QFont

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(400, 300)

        # Setup UI elements
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title bar height
        self.title_bar_height = 40
        
        # Button colors
        self.close_button_color = QColor(255, 0, 0)
        self.minimize_button_color = QColor(0, 255, 0)
        self.maximize_button_color = QColor(0, 0, 255)
        self.title_color = QColor(70, 130, 180)

        # Window drag variables
        self.old_pos = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_window_frame(painter)
        self.draw_title_bar(painter)
        
    def draw_window_frame(self, painter):
        # Draw rounded window background
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(QColor(255, 255, 255))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 15, 15)

    def draw_title_bar(self, painter):
        # Draw the title bar
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.title_color)
        painter.setPen(Qt.NoPen)
        title_rect = QRect(0, 0, self.width(), self.title_bar_height)
        painter.drawRoundedRect(title_rect, 15, 15)
        
        # Draw title text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont('Arial', 12))
        painter.drawText(20, 0, self.width(), self.title_bar_height, Qt.AlignLeft | Qt.AlignVCenter, "Custom Window Title")

        # Draw the close button
        close_button_rect = QRect(self.width() - 45, 5, 35, 30)
        painter.setBrush(self.close_button_color)
        painter.drawEllipse(close_button_rect)

        # Draw the minimize button
        minimize_button_rect = QRect(self.width() - 85, 5, 35, 30)
        painter.setBrush(self.minimize_button_color)
        painter.drawEllipse(minimize_button_rect)

        # Draw the maximize button
        maximize_button_rect = QRect(self.width() - 125, 5, 35, 30)
        painter.setBrush(self.maximize_button_color)
        painter.drawEllipse(maximize_button_rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Handle button click actions
        if event.button() == Qt.LeftButton:
            if self.is_point_in_rect(event.pos(), QRect(self.width() - 45, 5, 35, 30)):
                self.close()
            elif self.is_point_in_rect(event.pos(), QRect(self.width() - 85, 5, 35, 30)):
                self.showMinimized()
            elif self.is_point_in_rect(event.pos(), QRect(self.width() - 125, 5, 35, 30)):
                if self.isMaximized():
                    self.showNormal()
                else:
                    self.showMaximized()

    def is_point_in_rect(self, point, rect):
        return rect.contains(point)

if __name__ == "__main__":
    app = QApplication([])
    window = CustomWindow()
    window.show()
    app.exec()
