from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(['service.py', 'config.py', 'wd.py'], compiler_directives = {'language_level' : "3"}))