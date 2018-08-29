# -*- coding: UTF-8 -*-
import os
from decouple import config

if config('PYTHON_ENV') == 'production':
  from .production import *
elif config('PYTHON_ENV') == 'staging':
  from .development import *
else:
  from .development import *
