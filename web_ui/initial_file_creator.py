import os
from modules import utilities as util

user_dir = r'.user'


def create():
    # create brain data
    util.create_json_not_exist(f'{user_dir}/brain-data.json', [])
    print(f'brain data created: {user_dir}/brain-data.json')
    # create brain memo
    util.create_json_not_exist(f'{user_dir}/brain-memo.json',
                               {'note_dir': '', 'delimiter': '', 'append_mode': False, 'force_mode': False})
    print(f'brain memo file created: {user_dir}/brain-memo.json')

create()
