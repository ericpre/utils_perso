# -*- coding: utf-8 -*-
# Copyright 2012-2015 Eric Prestat
#
#
# This is a free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# <http://www.gnu.org/licenses/>.-

import matplotlib

cdict = {
'red'  :  ((0., 0., 0.), (0.2, 0, 0), (0.4, 0, 0), (0.6, 1, 1), (0.8, 1, 1), (1, 1, 1)),
'green':  ((0., 0., 0.), (0.2, 0, 0), (0.4, 170./255, 170./255), (0.6, 0, 0), (0.8, 1, 1), (1, 1, 1)),
'blue' :  ((0., 0., 0.), (0.2, 1, 1), (0.4, 0, 0), (0.6, 0, 0), (0.8, 0, 0), (1, 1, 1))
}
#generate the colormap with 1024 interpolated values
cmap_DM = matplotlib.colors.LinearSegmentedColormap('colormap_DM', cdict, 1024)

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack([gradient for i in range(256)])
    
    plt.figure()
    plt.imshow(gradient, cmap=cmap_DM)
    plt.colorbar()
