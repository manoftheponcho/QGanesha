__author__ = 'DUDE'

import numpy


class GNSFile:
    TEXTURE = 5889
    LARGE_R = 11777
    MED_R = 12033
    SMALL_R = 12289

    def __init__(self, file_name):

        storage = numpy.dtype({'names': ['index1', 'arrange', 'environment', 'resource_type',
                                         'resource_lba', 'resource_size'],
                               'formats': ['<H', '<B', '<B', '<H', '<I', '<I'],
                               'offsets': [ 0x0,  0x2,  0x3,  0x4,  0x8,  0xc],
                               'itemsize': 20})

        self._data = numpy.fromfile(file_name, dtype=storage)

    @property
    def situations(self):
        try:
            #return index1, arrange, environment, and resource_type limited to our resource data
            return self._data[self._data['resource_type'] <= GNSFile.SMALL_R][['index1',
                                                                               'arrange',
                                                                               'environment',
                                                                               'resource_type']]
        except AttributeError:
            print('Data not initialized.')

    @property
    def texture_data(self):
        try:
            return self._data[self._data['resource_type'] == GNSFile.TEXTURE]
        except AttributeError:
            print('Texture data not initialized.')

    @property
    def type0_data(self):
        try:
            return self._data[self._data['resource_type'] == GNSFile.LARGE_R]
        except AttributeError:
            print('Resource data not initialized.')

    @property
    def type1_data(self):
        try:
            return self._data[self._data['resource_type'] == GNSFile.MED_R]
        except AttributeError:
            print('Resource data not initialized.')

    @property
    def type2_data(self):
        try:
            return self._data[self._data['resource_type'] == GNSFile.SMALL_R]
        except AttributeError:
            print('Resource data not initialized.')


if __name__ == "__main__":
    gns_file = GNSFile('C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\MAP001.GNS')
    print(gns_file.situations)