import numpy as np


def rot_data(x_data=None, y_data=None, phi=None, point=None):
    """ rot_data-performs transformation of arrays of coordinates of graphical object points
    when turning at a given angle around a given point

    SYNTAX:
              [x_data, y_data] = rot_data( x_data, y_data, phi, point )
    AT BASELINE:
    - x_data, y_data-double vectors that determine the coordinates of the points of the graphic object
    - phi-rotation angle
    - point = 2-vector double-contains the coordinates of the point-center of rotation

    RESULT:
    - x_data, y_data - double of the vector defining the coordinates of the points
      the graphical object after the rotation
    """

    complex_point = complex(point[0], point[1])
    complex_data = (x_data + 1j * y_data) - complex_point
    complex_data = np.array(complex_data) * np.exp(1j * phi) + complex_point
    x_data = np.real(complex_data)
    y_data = np.imag(complex_data)

    return x_data, y_data
