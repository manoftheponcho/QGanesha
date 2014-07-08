__author__ = 'DUDE'

import os
import sys
import numpy
from PyQt4 import QtCore, QtGui


class GNSFile:

    def __init__(self, file_name):

        storage = numpy.dtype({'names': ['index1', 'arrange', 'environment', 'resource_type',
                                         'pad1', 'resource_lba', 'resource_size'],
                               'formats': ['<H', '<B', '<B', '<H', 'H', '<I', '<I'],
                               'itemsize': 20})

        self._data = numpy.fromfile(file_name, storage)

    @property
    def situations(self):
        try:
            #return index1, arrange, and temp1 limited to our resource data
            return numpy.concatenate((self.texture_data,
                                      self.type0_data,
                                      self.type1_data,
                                      self.type2_data))[['index1', 'arrange', 'environment']]
        except AttributeError:
            print('Data not initialized.')

    @property
    def texture_data(self):
        TEXTURE = 5889
        try:
            return self._data[self._data['resource_type'] == TEXTURE]
        except AttributeError:
            print('Texture data not initialized.')

    @property
    def type0_data(self):
        RTYPE0 = 11777
        try:
            return self._data[self._data['resource_type'] == RTYPE0]
        except AttributeError:
            print('Resource data not initialized.')

    @property
    def type1_data(self):
        RTYPE1 = 12033
        try:
            return self._data[self._data['resource_type'] == RTYPE1]
        except AttributeError:
            print('Resource data not initialized.')

    @property
    def type2_data(self):
        RTYPE2 = 12289
        try:
            return self._data[self._data['resource_type'] == RTYPE2]
        except AttributeError:
            print('Resource data not initialized.')


class MapWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fh = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                    caption='myGanesha',
                                                    filter='FFT Map Files (*.gns)')
        self.gns_file_tree = GNSFileTree(self.fh)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MapWindow()
    window.show()
    app.exec_()
