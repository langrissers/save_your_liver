# coding:utf-8
# this is a 32-bit bmp reader
class bmp:

    def _b2i(self, b_name): # byte_to_int
        l = len(b_name)
        tt_int = 0
        for i in range(l):
            tt_int += b_name[i] * 256 ** i
            
        return tt_int


    def __init__(self, filename):
        fin = open(filename, 'rb')   # use fin.seek(location) if necessary
        # bmp file header
        self.bf_type = fin.read(2)
        if self.bf_type != b'BM':
            print('not a bmp file')
        self.bf_size = self._b2i(fin.read(4))
        self.reserved1 = fin.read(2) # reserved bit
        self.reserved2 = fin.read(2) # reserved bit
        self.bf_offbits = self._b2i(fin.read(4)) # shift from file header to picture data
        # 14 bytes read

        # bitmap information
        self.bi_size = self._b2i(fin.read(4)) # information size, 40 bytes
        self.bi_width = self._b2i(fin.read(4))  
        self.bi_height = self._b2i(fin.read(4)) 
        self.bi_planes = self._b2i(fin.read(2)) # usually === 1
        self.bi_bit_count = self._b2i(fin.read(2)) # 1, 2, 4, 8, 16, 24, 32
        self.bi_compression = self._b2i(fin.read(4)) # usually 0, no compression
        self.bi_size_images = self._b2i(fin.read(4)) # data size
        self.bi_x_ppm = self._b2i(fin.read(4)) # Pixels per meter
        self.bi_y_ppm = self._b2i(fin.read(4)) #
        self.bi_clr_used = self._b2i(fin.read(4)) # data size
        self.bi_clr_important = self._b2i(fin.read(4)) # data size

        # color palette, here we have no palette when treating 32 bit bmp

        # bitmap data
        # if bi_height > 0: bit_data is placed like below,
        '''
        20 21 22 23 24 25 26 27 28 29
        10 11 12 13 14 15 16 17 18 19
         0  1  2  3  4  5  6  7  8  9
        '''
        # and reverse_data is placed like below,
        '''
         0  1  2  3  4  5  6  7  8  9
        10 11 12 13 14 15 16 17 18 19
        20 21 22 23 24 25 26 27 28 29
        '''
        # 32 bit  B-G-R-Alpha,  alpha === 255
        # RowSize = 4 * ceil(bi_bit_count * bi_width / 32)
        # 4 bytes = 32 bits,  32 % 32 === 0, then, row_size = 4 * bi_width
        self.bit_data = [[[0, 0, 0, 255] for i in range(self.bi_width)] for j in range(self.bi_height)]
        self.reverse_data = [[[0, 0, 0, 255] for i in range(self.bi_width)] for j in range(self.bi_height)]
        for i in range(self.bi_height):
            for j in range(self.bi_width):
                tt = fin.read(4) # tt is a byte type, but tt[0], etc are integers
                self.bit_data[i][j] = [ tt[0], tt[1], tt[2], tt[3] ]
                self.reverse_data[self.bi_height-1-i][j] = [ tt[0], tt[1], tt[2], tt[3] ]

        fin.close()
        

    def cut_pic(self, x1, y1, x2, y2):
        m = x2 - x1 # width
        n = y2 - y1 # height
        result =[ [ [ 0, 0, 0, 255] for i in range(n)] for j in range(m)]
        for i in range(n):  # height
            for j in range(m):  # width
                result[i][j] = self.reverse_data[y1+i][x1+j]
        
        return [m, n, result]


    def write_to_file(self, filename, wmin, hmin, wmax, hmax):
        x1 = 768 - hmax
        y1 = wmin
        x2 = 768 - hmin
        y2 = wmax
        new_size = 54 + 4 * (x2 - x1) * (y2 - y1)
        new_width = y2 - y1
        new_height = x2 - x1
        fout = open(filename, 'wb')
        fout.write(b'BM') # 2 bytes
        fout.write(new_size.to_bytes(4,'little'))
        fout.write(self.reserved1) # 2 bytes
        fout.write(self.reserved2) # 2 bytes
        fout.write(self.bf_offbits.to_bytes(4,'little'))
        # write bmp information
        fout.write(self.bi_size.to_bytes(4, 'little'))
        fout.write(new_width.to_bytes(4, 'little'))
        fout.write(new_height.to_bytes(4, 'little'))
        fout.write(self.bi_planes.to_bytes(2, 'little'))
        fout.write(self.bi_bit_count.to_bytes(2, 'little'))
        fout.write(self.bi_compression.to_bytes(4, 'little'))
        fout.write(self.bi_size_images.to_bytes(4, 'little'))
        fout.write(self.bi_x_ppm.to_bytes(4, 'little'))
        fout.write(self.bi_y_ppm.to_bytes(4, 'little'))
        fout.write(self.bi_clr_used.to_bytes(4, 'little'))
        fout.write(self.bi_clr_important.to_bytes(4, 'little'))
        # no color palette
        # write bmp data
        for i in range(x1, x2):
            for j in range(y1, y2):
                fout.write(self.bit_data[i][j][0].to_bytes(1, 'little'))
                fout.write(self.bit_data[i][j][1].to_bytes(1, 'little'))
                fout.write(self.bit_data[i][j][2].to_bytes(1, 'little'))
                fout.write(self.bit_data[i][j][3].to_bytes(1, 'little'))
                
        
        fout.close()
        return 0
