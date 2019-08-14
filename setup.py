import os
from    1 import os
   2 from distutils.core import setup
   3 import py2exe
   4 
   5 Mydata_files = []
   6 for files in os.listdir('C:/path/to/image/directory/'):
   7     f1 = 'C:/path/to/image/directory/' + files
   8     if os.path.isfile(f1): # skip directories
   9         f2 = 'images', [f1]
  10         Mydata_files.append(f2)
  11 
  12 setup(
  13     console=['trypyglet.py.py'],
  14     data_files = Mydata_files,
  15     options={
  16                 "py2exe":{
  17                         "unbuffered": True,
  18                         "optimize": 2,
  19                         "excludes": ["email"]
  20                 }
  21         }
  22 )