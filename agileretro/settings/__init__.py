# -*- coding: UTF-8 -*-
import os

if os.environ['PYTHON_ENV'] == 'production':
  from .production import *
elif os.environ['PYTHON_ENV'] == 'staging':
  from .development import *
else:
  from .development import *
