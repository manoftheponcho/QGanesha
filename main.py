__author__ = 'DUDE'

import sys
from MapFileTree import MapFileTree
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.arrays import vbo

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, texvertices, untexvertices, parent=None, size=QtCore.QSize(500, 500)):
        super().__init__(parent, size=size)
        self.texvertices = texvertices
        self.untexvertices = untexvertices
        self.program = None

    def initializeGL(self):
        VERTEX_SHADER = '''#version 130
        in vec3 vertex;
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * vec4(vertex.x, -vertex.y, vertex.z, 1.0);
        }'''
        vs = QtOpenGL.QGLShader(QtOpenGL.QGLShader.Vertex, self)
        vs.compileSourceCode(VERTEX_SHADER)

        FRAGMENT_SHADER = '''#version 130
        uniform bool isTex;
        void main() {
            if (isTex) {
                gl_FragColor = vec4(1, 1, 1, 1);
            }
            else {
                gl_FragColor = vec4(0, 0, 0, 1);
            }
        }'''
        fs = QtOpenGL.QGLShader(QtOpenGL.QGLShader.Fragment, self)
        fs.compileSourceCode(FRAGMENT_SHADER)

        self.program = QtOpenGL.QGLShaderProgram(self)
        self.program.addShader(vs)
        self.program.addShader(fs)
        self.program.link()

        self.texvbo = vbo.VBO(self.texvertices)
        self.untexvbo = vbo.VBO(self.untexvertices)
        self.isTex_location = self.program.uniformLocation('isTex')
        self.vertex_location = self.program.attributeLocation('vertex')
        glScale(1/256, 1/256, 1/256)
        glClearColor(0.0, 0.0, 1.0, 1.0)

    def paintGL(self):
        self.program.bind()
        glClear(GL_COLOR_BUFFER_BIT)
        with self.texvbo:
            glUniform1i(self.isTex_location, True)
            glEnableVertexAttribArray(self.vertex_location)
            glVertexAttribPointer(self.vertex_location,
                                  3, GL_SHORT, False, 0, self.texvbo)
            glDrawArrays(GL_TRIANGLES, 0, 3 * len(self.texvbo))

        with self.untexvbo:
            glUniform1i(self.isTex_location, False)
            glVertexAttribPointer(self.vertex_location,
                                  3, GL_SHORT, False, 0, self.untexvbo)
            glDrawArrays(GL_TRIANGLES, 0, 3 * len(self.untexvbo))

        glDisableVertexAttribArray(self.vertex_location)
        self.program.release()

    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)
        self.updateGL()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.parent().close()

class MapWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        import numpy
        from MeshFile import MeshFile
        super().__init__(parent)
        self.fh = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                    caption='myGanesha',
                                                    filter='FFT Map Files (*.9)')
        self.mesh = MeshFile(self.fh)
        self.textris = self.mesh.textris
        self.texquads1 = self.mesh.texquads[['A', 'B', 'C']].astype(MeshFile.tri)
        self.texquads2 = self.mesh.texquads[['B', 'C', 'D']].astype(MeshFile.tri)
        self.untris = self.mesh.untris
        self.unquads1 = self.mesh.unquads[['A', 'B', 'C']].astype(MeshFile.tri)
        self.unquads2 = self.mesh.unquads[['B', 'C', 'D']].astype(MeshFile.tri)
        self.gl_widget = GLWidget(numpy.concatenate((self.textris,
                                                     self.texquads1,
                                                     self.texquads2)),
                                  numpy.concatenate((self.untris,
                                                     self.unquads1,
                                                     self.unquads2)),
                                  self)
        self.setCentralWidget(self.gl_widget)

    def keyPressEvent(self, *args, **kwargs):
        return self.gl_widget.keyPressEvent(*args, **kwargs)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MapWindow()
    window.show()
    app.exec_()
