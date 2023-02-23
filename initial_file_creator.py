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

    util.create_file_not_exist(f'{user_dir}/input.txt', '')
    print(f'input file created: {user_dir}/input.txt')

    if not os.path.exists(f'{user_dir}/API-KEYS.txt'):
        print('Create API profile...')
        api_key = input('Enter your OpenAI API key: ')
        util.create_file_not_exist(f'{user_dir}/API-KEYS.txt', api_key)
        print(f'API key file created: {user_dir}/API-KEYS.txt')


create()
