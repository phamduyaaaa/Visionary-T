from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor

import sys

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Hiển thị chỉ nửa màn hình dọc bên trái
        screen_width = 1920  # Chiều rộng màn hình
        screen_height = 1080  # Chiều cao màn hình
        self.setGeometry(0, 0, screen_width // 2, screen_height)  # Nửa màn hình bên trái

        # Biến để điều chỉnh kích thước vùng rỗng mặc định trước
        self.hole_width = 600  # Chiều rộng vùng rỗng
        self.hole_height = 200  # Chiều cao vùng rỗng
        self.hole_x = (self.width() - self.hole_width) // 2
        self.hole_y = (self.height() - self.hole_height) // 2

        # Biến hỗ trợ kéo chỉnh kích thước vùng rỗng
        self._is_resizing = False
        self._resize_start_pos = QPoint(0, 0)
        self._resize_edge = None  # Ghi nhận cạnh đang kéo (trái, phải, trên, dưới, hoặc góc)

        # Kích thước để phát hiện viền
        self.resize_margin = 20
        
        # Biến hỗ trợ việc di chuyển cửa sổ
        self._is_dragging = False
        self._start_pos = QPoint(0, 0)

    # vẽ cửa sổ
    def paintEvent(self, event):
        painter = QPainter(self)
        # Tô toàn bộ phần hiển thị với màu có độ đục có thể điều chỉnh
        border_color = QColor(255, 255, 255, self.border_opacity)  # Màu và độ mờ tùy ý
        painter.fillRect(self.rect(), border_color)  # Màu với độ mờ

        # Vùng rỗng (hình chữ nhật)
        hole = QRect(self.hole_x, self.hole_y, self.hole_width, self.hole_height)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(hole, QColor(0, 0, 0, 0))
    
    # xử lí khi nhấn chuột
    def mousePressEvent(self, event):
        # kéo toàn cửa sổ nếu nhấn trong vùng khung trắng 
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

        # Kiểm tra nếu nhấn chuột gần viền để bắt đầu kéo
        resize_edge = self.detectResizeEdge(event.pos())
        if resize_edge:
            self._is_resizing = True
            self._resize_edge = resize_edge
            self._resize_start_pos = event.pos()  # Lưu vị trí chuột bắt đầu
            event.accept()

    #xử lí khi xử dụng chuột kéo thả
    def mouseMoveEvent(self, event):
        if self._is_resizing:
            delta = event.pos() - self._resize_start_pos
            # Các giá trị kích thước hiện tại
            new_x = self.hole_x
            new_y = self.hole_y
            new_width = self.hole_width
            new_height = self.hole_height
            # Định nghĩa giới hạn
            MARGIN = 10  # Khoảng cách tối thiểu từ viền
            MIN_WIDTH, MIN_HEIGHT = 50, 50  # Kích thước tối thiểu

            # Kích thước tối đa, trừ đi MARGIN
            MAX_WIDTH = self.width() - 2 * MARGIN
            MAX_HEIGHT = self.height() - 2 * MARGIN

            # Xử lý kéo thả từng cạnh/góc
            if "left" in self._resize_edge:
                new_x += delta.x()
                new_width -= delta.x()
            if "right" in self._resize_edge:
                new_width += delta.x()
            if "top" in self._resize_edge:
                new_y += delta.y()
                new_height -= delta.y()
            if "bottom" in self._resize_edge:
                new_height += delta.y()
            # Ràng buộc kích thước vùng rỗng
            new_width = max(MIN_WIDTH, min(new_width, MAX_WIDTH))
            new_height = max(MIN_HEIGHT, min(new_height, MAX_HEIGHT))
            # Đảm bảo tọa độ không ra ngoài biên
            new_x =  max(MARGIN, min(new_x, self.width() - new_width - MARGIN))
            new_y = max(MARGIN, min(new_y, self.height() - new_height - MARGIN))
            # Cập nhật tọa độ và kích thước
            self.hole_x = new_x
            self.hole_y = new_y
            self.hole_width = new_width
            self.hole_height = new_height
            self._resize_start_pos = event.pos()
            self.update()
        elif hasattr(self, '_is_dragging') and self._is_dragging:
            # Di chuyển toàn bộ cửa sổ
            self.move(event.globalPos() - self._start_pos)
            event.accept()

    # xử lí khi nhả chuột
    def mouseReleaseEvent(self, event):
        if self._is_resizing:
            self._is_resizing = False
            self._resize_edge = None
            event.accept()
        elif hasattr(self, '_is_dragging') and self._is_dragging:
            self._is_dragging = False
            event.accept()

    # xác định cạnh và góc cạnh trỏ chuột (Kiểm tra nếu chuột gần viền của vùng rỗng)
    def detectResizeEdge(self, pos):
        edge = []
        if abs(pos.x() - self.hole_x) < self.resize_margin:
            edge.append("left")
        if abs(pos.x() - (self.hole_x + self.hole_width)) < self.resize_margin:
            edge.append("right")
        if abs(pos.y() - self.hole_y) < self.resize_margin:
            edge.append("top")
        if abs(pos.y() - (self.hole_y + self.hole_height)) < self.resize_margin:
            edge.append("bottom")
        return edge if edge else None
    
    # Đóng ứng dụng khi nhấn phím 'Q'
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()

    # thay đổi độ đục của viền
    def setBorderOpacity(self, opacity):
        self.border_opacity = max(0, min(255, opacity))  # Đảm bảo giá trị alpha trong phạm vi từ 0 đến 255
        self.update()  # Cập nhật cửa sổ để hiển thị thay đổi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()  # Hiển thị cửa sổ
    window.setBorderOpacity(255)  # Đặt độ đục của viền 
    sys.exit(app.exec_())
