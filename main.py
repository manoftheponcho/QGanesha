__author__ = 'DUDE'

import sys
import numpy
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *

class GLWidget(QtOpenGL.QGLWidget):
    PROGRAM_VERTEX_ATTRIBUTE, PROGRAM_TEXCOORD_ATTRIBUTE = range(2)
    def __init__(self, texvertices, untexvertices, texuvs, parent=None, size=QtCore.QSize(500, 500)):
        super().__init__(parent, size=size)
        self.texvertices = texvertices
        self.untexvertices = untexvertices
        self.tex_coords = texuvs
        self.tex_program = None
        self.untex_program = None
        file_name = 'C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\MAP001.8'
        raw_data = numpy.fromfile(file_name, dtype='B')
        full_data = numpy.dstack((raw_data >> 4, raw_data & 15)).flatten()
        full_data.resize((1024, 256))
        self.tex_data = full_data.T
        self.tex_image = QtGui.QImage(QtCore.QSize(256, 1024), QtGui.QImage.Format_Indexed8)
        self.tex_image.setColorTable([QtGui.qRgb(i * 16, i * 16, i * 16) for i in range(16)])
        for pos, color in numpy.ndenumerate(self.tex_data):
            self.tex_image.setPixel(QtCore.QPoint(pos[0], pos[1]), color)
        self.tex_pixmap = QtGui.QPixmap(self.tex_image)

    def initializeGL(self):
        self.texture_loc = self.bindTexture(self.tex_pixmap)

        glEnable(GL_DEPTH_TEST)

        self.tex_program = QtOpenGL.QGLShaderProgram(self)
        self.tex_program.addShaderFromSourceFile(QtOpenGL.QGLShader.Vertex, 'shader.vert')
        self.tex_program.addShaderFromSourceFile(QtOpenGL.QGLShader.Fragment, 'shader.frag')
        self.tex_program.link()
        self.tex_program.bind()
        self.tex_program.enableAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE)
        self.tex_program.enableAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE)
        self.tex_program.setAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE, self.texvertices)
        self.tex_program.setAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE, self.tex_coords)
        self.tex_program.release()

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
        self.tex_program.bind()
        glBindTexture(GL_TEXTURE_2D, self.texture_loc)
        glDrawArrays(GL_TRIANGLES, 0, 3 * len(self.texvertices))
        self.tex_program.release()
        self.untex_program.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3 * len(self.untexvertices))
        self.untex_program.release()

    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)
        self.updateGL()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.parent().close()

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
        self.textriuvs = (self.mesh.textriuvs[['A.u', 'A.v']].tolist() +
                          self.mesh.textriuvs[['B.u', 'B.v']].tolist() +
                          self.mesh.textriuvs[['C.u', 'C.v']].tolist())
        self.textricolors = self.mesh.textriuvs['palette']
        self.texquads1 = self.mesh.texquads[['A', 'B', 'C']].astype(MeshFile.tri)
        self.texquaduvs1 = (self.mesh.texquaduvs[['A.u', 'A.v']].tolist() +
                            self.mesh.texquaduvs[['B.u', 'B.v']].tolist() +
                            self.mesh.texquaduvs[['C.u', 'C.v']].tolist())
        self.texquads2 = self.mesh.texquads[['B', 'C', 'D']].astype(MeshFile.tri)
        self.texquaduvs2 = list(zip(self.mesh.texquaduvs[['B.u', 'C.u', 'D.u']],
                                    self.mesh.texquaduvs[['B.v', 'C.v', 'D.v']]))
        self.texquadcolors = self.mesh.texquaduvs['palette']
        self.untris = numpy.concatenate((self.mesh.untris['A'],
                                         self.mesh.untris['B'],
                                         self.mesh.untris['C']))
        self.unquads1 = self.mesh.unquads[['A', 'B', 'C']].astype(MeshFile.tri)
        self.unquads2 = self.mesh.unquads[['B', 'C', 'D']].astype(MeshFile.tri)
        self.gl_widget = GLWidget(self.textris, self.untris, self.textriuvs)
        self.setCentralWidget(self.gl_widget)

    def keyPressEvent(self, *args, **kwargs):
        return self.gl_widget.keyPressEvent(*args, **kwargs)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MapWindow()
    window.show()
    app.exec_()
