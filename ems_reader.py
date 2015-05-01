# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 01:10:47 2015

@author: eric

EMS file format: File starts with two 32 bit integers that gives the number of
            	rows and columns of the image. It is followed by the image 
                 data. The data points are Real 4 Bytes (single precision 
                 floating point)
"""
def open_jems_wavefuntion(FNAME):
    with open(fname+'.ems') as f:
        rows = np.fromfile(f, dtype=np.int32, count=1).newbyteorder('>')
        columns = np.fromfile(f, dtype=np.int32, count=1).newbyteorder('>')
        real_part = np.fromfile(f, dtype=np.float32,count=rows*columns).newbyteorder('>').reshape((rows,columns))
        f.read(4)
        imag_part = np.fromfile(f, dtype=np.float32, count=rows*columns).newbyteorder('>').reshape((rows,columns))

    return real_part, imag_part

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    
    fname = 'MgOslice_z-2x2x2_0000'
    
    real_part, imag_part = open_jems_wavefuntion(fname)
    
    plt.figure()
    plt.imshow(real_part)
    plt.title('Real part')
    
    plt.figure()
    plt.imshow(imag_part)
    plt.title('Imaginary part')
    #wave_function = complex(real_part,imag_part)

