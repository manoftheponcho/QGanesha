__author__ = 'DUDE'

import numpy


class TextureFile:

    def __init__(self, file_name):
        self._data = numpy.fromfile(file_name, dtype='B')
        #separate the data into left and right nibbles
        self._lefts = self._data >> 4
        self._rights = self._data & 15
        #then interleave them into the full array
        self.full = numpy.dstack((self._lefts, self._rights)).flatten()
        self.full.resize((1024, 256))
        self.full = self.full.T

if __name__ == "__main__":
    import random
    import os
    import sys
    from PyQt4 import QtCore, QtGui
    #find all texture files in the MAP directory and pick one at random
    os.chdir('C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\')
    all_files = os.listdir()
    texture_files = [tex for tex in all_files if os.stat(tex).st_size == 131072]
    random_tex_file = random.choice(texture_files)
    random_tex_file = 'MAP001.8'
    texture_file = TextureFile(random_tex_file)
    #create an image and fill its color table with shades of grey
    grey_scaled = QtGui.QImage(QtCore.QSize(256, 1024), QtGui.QImage.Format_Indexed8)
    grey_scaled.setColorTable([QtGui.qRgb(i * 16, i * 16, i * 16) for i in range(16)])
    for pos, color in numpy.ndenumerate(texture_file.full):
        grey_scaled.setPixel(QtCore.QPoint(pos[0], pos[1]), color)

    class TestWidget(QtGui.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.drawImage(self.rect(), grey_scaled)
        def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Escape:
                self.close()
            else:
                super().keyPressEvent(event)
        def sizeHint(self):
            return QtCore.QSize(256,1024)
    app = QtGui.QApplication(sys.argv)
    window = TestWidget()
    window.show()
    app.exec_()