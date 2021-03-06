import numpy as np
import os
import sys


from fov import FoV
from util import Util

class Section(object):

  def __init__(self, directory, fovs, calculate_bounding_box):
    '''
    '''
    self._directory = directory

    self._fovs = fovs

    self._tx = -1
    self._ty = -1
    self._tz = -1
    self._width = -1
    self._height = -1

    if calculate_bounding_box:
      # calculate these values
      self.update_bounding_box()


    self._imagedata = None
    self._thumbnail = None

  def __str__(self):
    '''
    '''
    return 'Section ' + self.id + ' with ' + str(len(self._fovs)) + ' FoVs.'


  @property
  def id(self):
    return self._directory.strip(os.sep).split(os.sep)[-1]
    

  def update_bounding_box(self):
    '''
    '''
    width = 0
    height = 0

    minX = sys.maxint
    minY = sys.maxint

    for f in self._fovs:

      offset_x = f._tx
      offset_y = f._ty

      minX = min(minX, offset_x)
      minY = min(minY, offset_y)

    for f in self._fovs:

      offset_x = f._tx
      offset_y = f._ty

      width = max(width, f._width+offset_x-minX)
      height = max(height, f._height+offset_y-minY)    

    self._width = width #- minX
    self._height = height #- minY
    self._tx = minX
    self._ty = minY

  def index_fovs(self):
    '''
    '''
    fovs = []

    for f in Util.listdir(directory):
      fov_path = os.path.join(directory, f)

      # if not os.path.isdir(fov_path):
      #   # fovs always reside in directories
      #   continue

      fov = FoV.from_directory(fov_path, calculate_bounding_box)
      if fov:
        fovs.append(fov)

    self._fovs = fovs


  @staticmethod
  def from_directory(directory, calculate_bounding_box=False, index_subdirs=True):
    '''
    Loads a section from a directory without loading any images.

    If the directory does not seem to be a section or is not ready,
    return None.
    '''

    if index_subdirs:
  
      fovs = []

      for f in Util.listdir(directory):
        fov_path = os.path.join(directory, f)

        # if not os.path.isdir(fov_path):
        #   # fovs always reside in directories
        #   continue

        fov = FoV.from_directory(fov_path, calculate_bounding_box)
        if fov:
          fovs.append(fov)

    else:

      fovs = None

    section = Section(directory, fovs, calculate_bounding_box)
    return section
