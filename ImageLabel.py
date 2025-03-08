from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

SCALE_UNIT = 3000
MAX_SCALE = 10.0
MIN_SCALE = 0.1

class ImageLabel(QLabel):
    """
    可缩放的图片标签类
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = None
        self.scale_factor = 1.0
        self.imgWidth=10
        self.imgHeight=10

    def setPixmap(self, pixmap,height,width):
        self.pixmap = pixmap
        self.imgWidth=width
        self.imgHeight=height
        self.updateScale()
        
    def updateScale(self):
        if not self.pixmap:
            return
        # print(f"update: {self.scale_factor}")
        super().setPixmap(self.pixmap.scaled(int(self.imgWidth * self.scale_factor),
                                        int(self.imgHeight * self.scale_factor),
                                        Qt.KeepAspectRatio))

    def setScale(self,scale):
        self.scale_factor= scale
        self.updateScale()

class HandlerScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_pos = None
        self.minScale = 0.1
        self.maxScale = 2.0
        self.scale_factor = 1.0
        self.onScaleChanged=None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 记录鼠标按下时的位置
            self.last_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.last_pos and event.buttons() & Qt.LeftButton:
            # 计算鼠标的偏移量
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()

            # 获取垂直和水平滚动条
            v_scroll_bar = self.verticalScrollBar()
            h_scroll_bar = self.horizontalScrollBar()

            # 根据偏移量调整滚动条位置
            if v_scroll_bar:
                v_scroll_bar.setValue(v_scroll_bar.value() - dy)
            if h_scroll_bar:
                h_scroll_bar.setValue(h_scroll_bar.value() - dx)

            # 更新鼠标位置
            self.last_pos = event.pos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # 鼠标释放时，重置记录的位置
        self.last_pos = None
        super().mouseReleaseEvent(event)   
        

    
    def setScale(self,scale):
        self.scale_factor= max(self.minScale,min(scale,self.maxScale))
        if self.onScaleChanged:
            self.onScaleChanged(self.scale_factor)
        # print("scale: ",self.scale_factor)

    def wheelEvent(self, event):
        # 获取滚轮的滚动方向
        angle = event.angleDelta().y()
        angle/=SCALE_UNIT
        self.setScale(self.scale_factor+angle)
        # print("scale: ",self.scale_factor)

    
class ZoomImageLabel:
    """
    带区域限制的图片标签
    """
    def __init__(self):
        self.image = None   # 原始图片对象
        self.init_layout()
        self.display_image()
        pass
    
    
    def init_layout(self):
        self.scroll_area = HandlerScrollArea()
        self.scroll_area.minScale = MIN_SCALE
        self.scroll_area.maxScale = MAX_SCALE
        self.imageLabel = ImageLabel()
        
        # 设置滚动区域(图片)
        self.scroll_area.setWidget(self.imageLabel)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.onScaleChanged = self.onScaleChanged
        
        # 滚动区域外(两个标签)
        self.title = QLabel("图片")
        self.title.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.text = QLabel("缩放: xx.xx%")
        self.text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # 设置布局
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.scroll_area)

        # 设置整体布局(widget 为代理单元)
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)

    def setTitle(self,title:str):
        self.title.setText(title)
        
        
    def onScaleChanged(self,scale):
        text = '%.2f%%' % (scale * 100)
        self.text.setText(f"缩放: {text}")
        self.imageLabel.setScale(scale)
        # print(f"handle_scale: {scale}")
        
    
    def display_image(self):
        """
        显示图片
        """
        if self.image is None:
            return
        # 将 OpenCV 图像转换为 QImage
        if len(self.image.shape) == 3:  # 彩色图像
            height, width, channel = self.image.shape
            bytes_per_line = 3 * width
            q_img = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        else:  # 灰度图像
            height, width = self.image.shape
            bytes_per_line = width
            q_img = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

        # 将 QImage 转换为 QPixmap
        pixmap = QPixmap.fromImage(q_img)

        # 显示图像
        self.imageLabel.setScale(1.0)
        self.imageLabel.setPixmap(pixmap,height, width)
        
                
    def setImage(self,image):
        """
        设置图片
        """
        self.image=image
        self.display_image()
