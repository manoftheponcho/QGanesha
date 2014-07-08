__author__ = 'DUDE'

import numpy


class GNSFile:

    def __init__(self, file_name):

        storage = numpy.dtype({'names': ['index1', 'arrange', 'environment', 'resource_type',
                                         'resource_lba', 'resource_size'],
                               'formats': ['<H', '<B', '<B', '<H', '<I', '<I'],
                               'offsets': [   0,    4,    5,    6,   10,   12],
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