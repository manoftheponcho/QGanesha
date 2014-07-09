__author__ = 'DUDE'

import sys
from MapFileTree import MapFileTree
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.arrays import vbo

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, vertices, parent=None, size=QtCore.QSize(500, 500)):
        super().__init__(parent, size=size)
        self.vertices = vertices
        self.program = None

    def initializeGL(self):
        VERTEX_SHADER = '''
        attribute vec3 vertex;
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * vec4(vertex, 1.0);
        }'''
        vs = QtOpenGL.QGLShader(QtOpenGL.QGLShader.Vertex, self)
        vs.compileSourceCode(VERTEX_SHADER)

        FRAGMENT_SHADER = '''
        void main() {
            gl_FragColor = vec4(1, 1, 1, 1);
        }'''
        fs = QtOpenGL.QGLShader(QtOpenGL.QGLShader.Fragment, self)
        fs.compileSourceCode(FRAGMENT_SHADER)

        self.program = QtOpenGL.QGLShaderProgram(self)
        self.program.addShader(vs)
        self.program.addShader(fs)
        self.program.link()

        self.vbo = vbo.VBO(self.vertices)
        self.vertex_location = self.program.attributeLocation('vertex')
        glEnable(GL_DEPTH_TEST)
        glScale(1/256, 1/256, 1/256)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        self.program.bind()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        with self.vbo:
            glEnableVertexAttribArray(self.vertex_location)
            glVertexAttribPointer(self.vertex_location,
                                  4, GL_SHORT, False, 0, self.vbo)
            glDrawArrays(GL_TRIANGLES, 0, 3 * len(self.vbo))

        glDisableVertexAttribArray(self.vertex_location)
        self.program.release()

    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)

class MapWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        from MeshFile import MeshFile
        super().__init__(parent)
        self.fh = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                    caption='myGanesha',
                                                    filter='FFT Map Files (*.8)')
        self.mesh = MeshFile(self.fh)
        self.tri1 = self.mesh.texquads[['A', 'B', 'C']]
        self.tri2 = self.mesh.texquads[['B', 'C', 'D']]
        self.gl_widget = GLWidget(self.tri1, self)
        self.setCentralWidget(self.gl_widget)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MapWindow()
    window.show()
    app.exec_()
