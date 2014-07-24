__author__ = 'DUDE'

import sys
import numpy
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *

class GLWidget(QtOpenGL.QGLWidget):
    PROGRAM_VERTEX_ATTRIBUTE, PROGRAM_TEXCOORD_ATTRIBUTE = range(2)
    def __init__(self, textris, texquads, untris, unquads, texuvs, parent=None):
        super().__init__(parent)
        self.textris = textris
        self.texquads = texquads
        self.texvertices = textris.tolist()
        self.untexvertices = untris.tolist() + unquads.tolist()
        print(self.untexvertices)
        self.tex_coords = texuvs
        self.tex_program = None
        self.untex_program = None
        file_name = 'C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\MAP001.8'
        raw_data = numpy.fromfile(file_name, dtype='B')
        full_data = numpy.dstack((raw_data >> 4, raw_data & 15)).flatten()
        full_data.resize((1024, 256))
        self.tex_data = full_data.T
        self.tex_images = [QtGui.QImage(QtCore.QSize(256, 256), QtGui.QImage.Format_Indexed8)] * 4
        for image in self.tex_images:
            image.setColorTable([QtGui.qRgb(i * 16, i * 16, i * 16) for i in range(16)])
        for pos, color in numpy.ndenumerate(self.tex_data):
            self.tex_images[pos[1]//256].setPixel(QtCore.QPoint(pos[0], pos[1] % 256), color)
        self.tex_pixmaps = [QtGui.QPixmap(image) for image in self.tex_images]

    def initializeGL(self):
        self.texture_loc = self.bindTexture(self.tex_pixmaps[0])

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

#        self.tex_program = QtOpenGL.QGLShaderProgram(self)
#        self.tex_program.addShaderFromSourceFile(QtOpenGL.QGLShader.Vertex, 'shader.vert')
#        self.tex_program.addShaderFromSourceFile(QtOpenGL.QGLShader.Fragment, 'shader.frag')
#        self.tex_program.link()
#        self.tex_program.bind()
#        self.tex_program.enableAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE)
#        self.tex_program.enableAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE)
#        self.tex_program.setAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE, self.textris)
#        self.tex_program.setAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE, self.tex_coords)
#        self.tex_program.release()

        self.untex_program = QtOpenGL.QGLShaderProgram(self)
        self.untex_program.addShaderFromSourceFile(QtOpenGL.QGLShader.Vertex, 'untexshader.vert')
        self.untex_program.addShaderFromSourceFile(QtOpenGL.QGLShader.Fragment, 'untexshader.frag')
        self.untex_program.link()
        self.untex_program.bind()
        self.untex_program.enableAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE)
        self.untex_program.setAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE, self.untexvertices)
        self.untex_program.release()

        glScale(1/256, 1/256, 1/256)
        glClearColor(0.0, 0.0, 1.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#        self.tex_program.bind()
#        glBindTexture(GL_TEXTURE_2D, self.texture_loc)
#        glDrawArrays(GL_TRIANGLES, 0, 3 * len(self.textris))
#        self.tex_program.release()
        self.untex_program.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3 * len(self.untexvertices))
        self.untex_program.release()

    def resizeGL(self, w, h):
        self.size = w, h
        glViewport(0, 0, w, h)
        self.updateGL()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.parent().close()
        if event.key() == QtCore.Qt.Key_Up:
            glRotate(5, 1, 0, 0)
        elif event.key() == QtCore.Qt.Key_Down:
            glRotate(-5, 1, 0, 0)
        if event.key() == QtCore.Qt.Key_Left:
            glRotate(5, 0, 1, 0)
        elif event.key() == QtCore.Qt.Key_Right:
            glRotate(-5, 0, 1, 0)
        self.updateGL()

    def sizeHint(self):
        return QtCore.QSize(512, 512)

class MapWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        from MeshFile import MeshFile
        super().__init__(parent)
        self.fh = 'C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\MAP001.9'
#        self.fh = QtGui.QFileDialog.getOpenFileName(parent=self,
#                                                    caption='QGanesha',
#                                                    filter='FFT Map Files (*.9)')
        self.mesh = MeshFile(self.fh)
        self.textris = numpy.concatenate((self.mesh.textris['A'],
                                          self.mesh.textris['B'],
                                          self.mesh.textris['C']))
        self.textriuvs = (self.mesh.textriuvs[['A.u', 'A.v', 'page']].tolist() +
                          self.mesh.textriuvs[['B.u', 'B.v', 'page']].tolist() +
                          self.mesh.textriuvs[['C.u', 'C.v', 'page']].tolist())
        self.textricolors = self.mesh.textriuvs['palette']
        self.texquads = numpy.concatenate((self.mesh.texquads['A'],
                                           self.mesh.texquads['B'],
                                           self.mesh.texquads['C'],
                                           self.mesh.texquads['B'],
                                           self.mesh.texquads['C'],
                                           self.mesh.texquads['D']))
        self.texquaduvs1 = (self.mesh.texquaduvs[['A.u', 'A.v']].tolist() +
                            self.mesh.texquaduvs[['B.u', 'B.v']].tolist() +
                            self.mesh.texquaduvs[['C.u', 'C.v']].tolist())
        self.texquadcolors = self.mesh.texquaduvs['palette']
        self.untris = numpy.concatenate((self.mesh.untris['A'],
                                         self.mesh.untris['B'],
                                         self.mesh.untris['C']))
        self.unquads = numpy.concatenate((self.mesh.unquads['A'],
                                          self.mesh.unquads['B'],
                                          self.mesh.unquads['C'],
                                          self.mesh.unquads['B'],
                                          self.mesh.unquads['C'],
                                          self.mesh.unquads['D']))
        self.unquads1 = self.mesh.unquads[['A', 'B', 'C']].astype(MeshFile.tri)
        self.unquads2 = self.mesh.unquads[['B', 'C', 'D']].astype(MeshFile.tri)
        self.gl_widget = GLWidget(self.textris, self.texquads, self.untris, self.unquads, self.textriuvs)
        self.setCentralWidget(self.gl_widget)

    def keyPressEvent(self, *args, **kwargs):
        return self.gl_widget.keyPressEvent(*args, **kwargs)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MapWindow()
    window.show()
    app.exec_()