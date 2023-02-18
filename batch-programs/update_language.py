import os
import subprocess
import sys

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules import utilities as util

locals_path = f'.locals'
languages = util.read_json(f'{locals_path}/languages.json')

try:
    # create LC_MESSAGES under .local directory if not exist
    for language in languages.values():
        subprocess.call(f'msgmerge -U {locals_path}/{language}/LC_MESSAGES/base.po {locals_path}/base.pot', shell=True)
except Exception as e:
    print(e)
    print('Error: Unable to merge .pot file with .po files')