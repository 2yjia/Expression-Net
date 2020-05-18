# coding:utf-8
# 读取csv文件中的顶点信息，绘制三维人脸，并显示在软件界面上

import os
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import main_ExpShapePoseNet

output_folder = './output' # The location where .ply files are saved
if not os.path.exists(output_folder):
        os.makedirs(output_folder)

class picture(QWidget):
    def __init__(self):
        super(picture, self).__init__()
        self.btn1 = 0
        self.btn2 = 0
        self.initUI()

    def initUI(self):
        self.resize(1520, 800)
        self.center()
        self.setWindowTitle("3D人脸重建")
        self.background()
        self.image_frame()
        self.button()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def background(self):
        self.p = QPalette()
        self.p.setBrush(self.backgroundRole(), QBrush(QColor(255, 239, 213)))
        self.setPalette(self.p)
        self.setAutoFillBackground(True)

    def image_frame(self):
        self.label_1 = QLabel(self)
        self.label_1.setText(" 上传的人脸图片")
        self.label_1.setFixedSize(720, 547)
        self.label_1.move(20, 80)
        self.label_1.setStyleSheet(
            "QLabel{background:white;}" "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:微软雅黑;}")

        self.label_2 = QLabel(self)
        self.label_2.setText("处理后的人脸图片")
        self.label_2.setFixedSize(720, 547)
        self.label_2.move(770, 80)
        self.label_2.setStyleSheet(
            "QLabel{background:white;}" "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;}")

    def button(self):
        self.btn = QPushButton(self)
        self.btn.setText("打开图片")
        self.btn.move(340, 700)
        self.btn.clicked.connect(self.openimage)

        self.btn_fix = QPushButton(self)
        self.btn_fix.setText("3D人脸建模")
        self.btn_fix.move(1080, 700)
        self.btn_fix.clicked.connect(self.fiximage)

    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "All Files(*)")
        if imgName:
            img = QtGui.QPixmap(imgName)
            if img.width() < img.height():
                self.label_1.setFixedSize(547 / 1.3, 720 / 1.3)
                self.label_1.move(200, 80)
            self.label_1.setPixmap(img)
            self.label_1.setScaledContents(True)
            self.input_img = imgName

    def fiximage(self):
        name = os.path.splitext(os.path.basename(self.input_img))
        outfile_path = output_folder + '/' + name[0] + '_Shape_Expr_Pose.ply'
        main_ExpShapePoseNet.main(self.input_img, outfile_path)

        outimage_path = output_folder + '/' + name[0] + '_Shape_Expr_Pose' + name[1]
        displayModel(outfile_path, outimage_path)
        im = QtGui.QPixmap(outimage_path)
        self.label_2.setPixmap(im)
        self.label_2.setScaledContents(True)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '3D人脸重建',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def readXYZfile(filename, Separator):
    data = [[], [], []]

    f = open(filename, 'r')
    line = f.readline()
    num = 0

    while line:  # 按行读入点云
        if num > 8:
            index = len(line.split(Separator))
            if index == 3:
                x,y,z = line.split(Separator)
                data[0].append(float(x))  # X坐标
                data[1].append(float(y))  # Y坐标
                data[2].append(float(z))  # Z坐标
            else:
                break
        line = f.readline()
        num = num + 1

    f.close()

    point=[data[0],data[1],data[2]]

    return point


def displayModel(outfile_path, outimage_path):
    point = readXYZfile(outfile_path, ' ')
    fig = plt.figure()

    ax = fig.gca(projection='3d')
    ax.plot_trisurf(point[0], point[1], point[2],color='chocolate')
    # ax.view_init(elev=45, azim=45)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.savefig(outimage_path, dpi=120)
    print ('> Save ' + outimage_path)

def show():
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    print ('> Finished !')
    sys.exit(app.exec_())

if __name__ == "__main__":
    show()
