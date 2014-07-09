__author__ = 'DUDE'

import numpy


class MeshFile:

    #made this a class because it doesn't split nicely
    class Color:
        def __init__(self, data=0):
            self._data = data

        def __str__(self):
            return 'R {} G {} B {} A {}'.format(self.r, self.g, self.b, self.a)
        def __repr__(self):
            return 'Color({})'.format(self._data)
        @property
        def r(self):
            return self._data & 31
        @property
        def g(self):
            return (self._data >> 5) & 31
        @property
        def b(self):
            return (self._data >> 10) & 31
        @property
        def a(self):
            return (self._data >> 15)

    #mesh file header is big and ugly
    toc = numpy.dtype({'names': ['primary', 'palettes', 'lights', 'terrain',
                                 'tex_anis', 'pal_anis', 'tex_palettes', 'ani_commands', 'ani_meshes',
                                 'vis_angles'],
                       'formats': ['<u4', '<u4', '<u4', '<u4', '<u4', '<u4', '<u4', '<u4', '<8u4', '<u4'],
                       'offsets': [0x40,   0x44,  0x64,  0x68,  0x6c,  0x70,  0x7c,  0x8c,   0x90,  0xb0],
                       'itemsize': 196})

    #texcoords are also a little weird
    triuv = numpy.dtype({'names': ['A.u', 'A.v', 'palette', 'B.u', 'B.v', 'page', 'C.u', 'C.v'],
                         'formats': ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
                         'offsets': [0x0, 0x1, 0x2, 0x4, 0x5, 0x6, 0x8, 0x9],
                         'itemsize': 10})
    quaduv = numpy.dtype({'names': ['A.u', 'A.v', 'palette', 'B.u', 'B.v', 'page', 'C.u', 'C.v', 'D.u', 'D.v'],
                          'formats': ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
                          'offsets': [0x0, 0x1, 0x2, 0x4, 0x5, 0x6, 0x8, 0x9, 0xa, 0xb]})

    #primary mesh header contains 4 16-bit primitive counts
    header = numpy.dtype([('textris', '<H'), ('texquads', '<H'), ('untris', '<H'), ('unquads', '<H')])

    #a few helpers not big enough for classes
    point = numpy.dtype([('x', '<i2'), ('y', '<i2'), ('z', '<i2')])
    tri = numpy.dtype([('A', point), ('B', point), ('C', point)])
    quad = numpy.dtype([('A', point), ('B', point), ('C', point), ('D', point)])
    turnblue = numpy.dtype([('z', 'b'), ('x', 'b')])
    palette = numpy.dtype('16u2')

    def __init__(self, file_name):
        with open(file_name, 'rb') as f:
            self._data = f.read()
        self.table_of_contents = numpy.frombuffer(self._data, dtype=MeshFile.toc, count=1)

    @property
    def counts(self):
        """Number of each type of primitive in the file."""
        if self.table_of_contents['primary'][0] == 0:
            return numpy.asarray([0], dtype=MeshFile.header)
        else:
            return numpy.frombuffer(self._data,
                                    dtype=MeshFile.header,
                                    offset=self.table_of_contents['primary'][0],
                                    count=1)

    @property
    def textris(self):
        """numpy.array of all textured triangles in the file."""
        if self.table_of_contents['primary'][0] == 0:
            return None
        else:
            location = (self.table_of_contents['primary'][0] +
                        self.counts.size * self.header.itemsize)
            try:
                return numpy.frombuffer(self._data,
                                        dtype=MeshFile.tri,
                                        offset=location,
                                        count=self.counts['textris'])
            except AttributeError:
                print('Mesh data not initialized.')

    @property
    def texquads(self):
        """numpy.array of all textured quads in the file."""
        if self.table_of_contents['primary'][0] == 0:
            return None
        else:
            location = (self.table_of_contents['primary'][0] +
                        self.counts.size * MeshFile.header.itemsize +
                        self.counts['textris'].size * MeshFile.tri.itemsize)
            try:
                return numpy.frombuffer(self._data,
                                        dtype=MeshFile.quad,
                                        offset=location,
                                        count=self.counts['texquads'])
            except AttributeError:
                print('Mesh data not initialized.')

    @property
    def untris(self):
        """numpy.array of all untextured triangles in the file."""
        if self.table_of_contents['primary'][0] == 0:
            return None
        else:
            location = (self.table_of_contents['primary'][0] +
                        self.counts.size * MeshFile.header.itemsize +
                        self.counts['textris'].size * MeshFile.tri.itemsize +
                        self.counts['texquads'].size * MeshFile.quad.itemsize)
            try:
                return numpy.frombuffer(self._data,
                                        dtype=MeshFile.tri,
                                        offset=location,
                                        count=self.counts['untris'])
            except AttributeError:
                print('Mesh data not initialized.')

    @property
    def unquads(self):
        """numpy.array of all untextured quads in the file."""
        if self.table_of_contents['primary'][0] == 0:
            return None
        else:
            location = (self.table_of_contents['primary'][0] +
                        self.counts.size * MeshFile.header.itemsize +
                        self.counts['textris'].size * MeshFile.tri.itemsize +
                        self.counts['texquads'].size * MeshFile.quad.itemsize +
                        self.counts['untris'].size * MeshFile.tri.itemsize)
            try:
                return numpy.frombuffer(self._data,
                                        dtype=MeshFile.quad,
                                        offset=location,
                                        count=self.counts['unquads'])
            except AttributeError:
                print('Mesh data not initialized.')

    @property
    def textrinorms(self):
        """numpy.array of the normals of all textured triangles in the file."""
        if self.table_of_contents['primary'][0] == 0:
            return None
        else:
            location = (self.table_of_contents['primary'][0] +
                        self.counts.size * MeshFile.header.itemsize +
                        self.counts['textris'].size * MeshFile.tri.itemsize +
                        self.counts['texquads'].size * MeshFile.quad.itemsize +
                        self.counts['untris'].size * MeshFile.tri.itemsize +
                        self.counts['unquads'].size * MeshFile.tri.itemsize)
            try:
                return numpy.frombuffer(self._data,
                                        dtype=MeshFile.tri,
                                        offset=location,
                                        count=self.counts['textris'])
            except AttributeError:
                print('Mesh data not initialized.')

    @property
    def texquadnorms(self):
        """numpy.array of the normals of all textured quads in the file."""
        if self.table_of_contents['primary'][0] == 0:
            return None
        else:
            location = (self.table_of_contents['primary'][0] +
                        self.counts.size * MeshFile.header.itemsize +
                        self.counts['textris'].size * MeshFile.tri.itemsize +
                        self.counts['texquads'].size * MeshFile.quad.itemsize +
                        self.counts['untris'].size * MeshFile.tri.itemsize +
                        self.counts['unquads'].size * MeshFile.tri.itemsize +
                        self.counts['textris'].size * MeshFile.tri.itemsize)
            try:
                return numpy.frombuffer(self._data,
                                        dtype=MeshFile.quad,
                                        offset=location,
                                        count=self.counts['texquads'])
            except AttributeError:
                print('Mesh data not initialized.')

    @property
    def color_palettes(self):
        """List of Color objects representing the color data in the file."""
        if self.table_of_contents['palettes'] == 0:
            return None
        else:
            location = self.table_of_contents['palettes'][0]
            try:
                _data = numpy.frombuffer(self._data,
                                         dtype=MeshFile.palette,
                                         offset=location,
                                         count=16)
                return [MeshFile.Color(_data[0][x]) for x in range(16)]
            except AttributeError:
                print('Mesh data not initialized.')

if __name__ == "__main__":
    import random
    import os
    #find all mesh files in the MAP directory and pick one at random
    os.chdir('C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\')
    all_files = os.listdir()
    mesh_files = [mesh for mesh in all_files if os.stat(mesh).st_size != 131072
                  and os.path.splitext(mesh)[1].lower() != '.gns']
    done = False
    while not done:
        random_mesh_file = random.choice(mesh_files)
        mesh_file = MeshFile(random_mesh_file)
        if mesh_file.table_of_contents['palettes'] != 0:
            print(mesh_file.color_palettes)
            done = True