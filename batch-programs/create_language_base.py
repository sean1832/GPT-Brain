import os
import subprocess
import sys
# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules import utilities as util


pages = util.scan_directory(f'pages')
pages_full = []
for page in pages:
    page = util.get_file_name(page, extension=True)
    pages_full.append(f'pages/{page}')
main_file = util.get_file_name(f'Seanium_brain.py', extension=True)

pages_full.append(main_file)

pages_flatten = ' '.join(pages_full)

locals_path = f'.locals'
languages = util.read_json(f'{locals_path}/languages.json')
# create LC_MESSAGES under .local directory if not exist
for language in languages.values():
    # if language path not exist, create it
    if not os.path.exists(f'{locals_path}/{language}/LC_MESSAGES'):
        os.makedirs(f'{locals_path}/{language}/LC_MESSAGES')

# create .pot file
subprocess.call(f'xgettext {pages_flatten} -o {locals_path}/base.pot', shell=True)
