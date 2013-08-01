'''
Usage: python cythonize.py path_to_setup.py py_file_path ...

python cythonize.py setup.py `cat cython_list
'''

from sys import argv
from os import rename

setup_py_path = argv[1]
py_path_list = argv[2:]
pyx_path_list = [path + 'x' for path in py_path_list]

# read in setup.py
with open(setup_py_path, 'r') as setup_py_file:
	setup_py = setup_py_file.readlines()

# rename py files to pyx
for py_path, pyx_path in zip(py_path_list, pyx_path_list):
	rename(py_path, pyx_path)

	# add pyx files to sources list in setup.py
	setup_py.insert(
		setup_py.index('sources = {\n') + 1,
		("    '{}': base_flags,\n").format(
			'/'.join(pyx_path.split('/')[1:])))

# make core/text/__init__.py import from pyx file
with open('kivy/core/text/__init__.py', 'r+') as py_file:
	lines = py_file.readlines()
	lines[
		lines.index("DEFAULT_FONT = 'DroidSans'\n"):
		lines.index("        doc='''(deprecated) Use text_size instead.''')\n") + 1
	] = 'from ctext import *\n'
	
	py_file.seek(0)
	py_file.writelines(lines)
	py_file.truncate()
	
with open(setup_py_path, 'w') as setup_py_file:
	setup_py_file.writelines(setup_py)