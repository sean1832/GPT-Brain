import os
import subprocess
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules import utilities as util

pages = util.scan_directory(f'pages', exclude=['__init__.py', '__pycache__'])
tools = util.scan_directory(f'streamlit_toolkit', exclude=['__init__.py', '__pycache__'])

files_to_process = []

main_file = util.get_file_name(f'Seanium_brain.py', extension=True)
files_to_process.append(main_file)

for page in pages:
    page = util.get_file_name(page, extension=True)
    files_to_process.append(f'pages/{page}')
for tool in tools:
    tool = util.get_file_name(tool, extension=True)
    files_to_process.append(f'streamlit_toolkit/{tool}')

files_flatten = ' '.join(files_to_process)

locals_path = f'.locals'
languages = util.read_json(os.path.abspath(f'{locals_path}/languages.json'))
# create LC_MESSAGES under .local directory if not exist
for language in languages.values():
    # if language path not exist, create it
    if not os.path.exists(f'{locals_path}/{language}/LC_MESSAGES'):
        os.makedirs(f'{locals_path}/{language}/LC_MESSAGES')

# create .pot file
subprocess.call(f'xgettext {files_flatten} -o {locals_path}/base.pot', shell=True)
