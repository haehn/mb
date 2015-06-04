import cv2
import glymur
import os

class Tile(object):

  def __init__(self, filename, tx=-1, ty=-1, tz=-1):
    '''
    '''
    self._filename = filename
    self._tx = tx
    self._ty = ty
    self._tz = tz

    self._width = -1
    self._height = -1

    self._imagedata = None

  @property
  def id(self):
    return self._filename

  @property
  def width(self):
    return self._width

  @width.setter
  def width(self, value):
    self._width = value

  @property
  def height(self):
    return self._height

  @height.setter  
  def height(self, value):
    self._height = value
  
  def load(self, directory, file_prefix='', ratio_x=1, ratio_y=1):
    '''
    '''
    # print 'LOADING',os.path.join(directory, file_prefix + self._filename) 

    extension = os.path.splitext(self._filename)[1].lower()

    if extension == '.jp2':
      self._imagedata = glymur.Jp2k(os.path.join(directory, file_prefix + self._filename))
    else:
      self._imagedata = cv2.imread(os.path.join(directory, file_prefix + self._filename), 0) # this is grayscale loading with any OpenCV version
    

  def downsample(self, level):
    '''
    '''
    extension = os.path.splitext(self._filename)[1].lower()

    if extension == '.jp2':
      return self._imagedata.read(rlevel=level)
    else:
      factor = 2**level
      if factor == 1.:
        return self._imagedata

      factor = 1./factor
      return cv2.resize(self._imagedata, (0,0), fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)


  @staticmethod
  def from_string(string):
    '''
    Creates a new image from a string.
    '''

    string = string.strip() # remove some weird line break
    values = string.split() # split the string

    # right now we have something like this
    # ['021_000001_003_2015-01-14T1653216213670.bmp', '2189614.003', '1853228.961', '0']
    
    tile = Tile(values[0], float(values[1]), float(values[2]), float(values[3]))
    # print values
    return tile
