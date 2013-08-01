'''
Usage: python cythonize.py path_to_setup.py py_file_path ...

python cythonize.py setup.py `cat cython_list
'''

from sys import argv
from os.path import split
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

	# use graphics flags for certain files
	def flags():
		return ('base_flags'
			if pyx_path not in ['kivy/core/window/window_pygame.pyx']
			else 'merge(base_flags, gl_flags, graphics_flags)')

	# add pyx files to sources list in setup.py
	setup_py.insert(
		setup_py.index('sources = {\n') + 1,
		"    '{}': " + flags() + ",\n".format('/'.join(pyx_path.split('/')[1:])))



with open(setup_py_path, 'w') as setup_py_file:
	setup_py_file.writelines(setup_py)