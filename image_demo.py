
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)


ax = plt.subplot(111)
ax.plot(
    [1, 2, 3], [1, 2, 3],
    'go-',
    label='line 1',
    linewidth=2
 )
# arr_img = plt.imread("stinkbug.svg")
xy = (0.5, 0.7)
offsetbox = TextArea("Test 1", minimumdescent=False)


arr_img = plt.imread("title_bg2.png")
im = OffsetImage(arr_img, zoom=0.1)
ab = AnnotationBbox(offsetbox, xy,
                    xybox=(-20, 40),
                    xycoords='data',
                    boxcoords="offset points",
                    arrowprops=dict(arrowstyle="->"))
ax.add_artist(ab)
"""

ab = AnnotationBbox(im, (1, 0), xycoords='axes fraction')
ax.add_artist(ab)
"""
plt.show()