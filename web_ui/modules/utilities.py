import json
import os

def extract_string(text, delimiter):
    # Extract string between delimiters
    start_index = text.index(delimiter) + len(delimiter)
    end_index = text.index(delimiter, start_index)
    return text[start_index:end_index]


def extract_string(text, delimiter, force=False):
    if not delimiter in text:
        if force:
            return ''
        else:
            return text
    else:
        substring = text.split(delimiter)
        result = []
        for i in range(1, len(substring), 2):
            result.append(substring[i])
        return ''.join(result)
        

def create_not_exist(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def create_file_not_exist(path):
    if not os.path.exists(path):
        write_file('', path)

def read_file(filepath, delimiter='', force=False):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read()
        if delimiter != '':
            data = extract_string(data, delimiter, force)
        return data


def read_files(file_dir, delimiter='', force=False):
    contents = []

    # Read all files in a directory
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            # extract file path
            filepath = os.path.join(root, file)
            # extract filename with extension
            filename = os.path.basename(filepath)
            # extract filename without extension
            filename = os.path.splitext(filename)[0]
            file_data = read_file(filepath, delimiter, force)
            if force and file_data == '':
                continue
            
            content = [f'[{filename}]', file_data]
            contents.append('\n\n'.join(content))
        
    result = '\n\n\n\n'.join(contents)
    return result

def write_file(content, filepath, mode='w'):
    create_not_exist(filepath)
    with open(filepath, mode, encoding='utf-8') as file:
        file.write(content)

def create_json_not_exist(filepath, initial_value={}):
    if not os.path.exists(filepath):
        write_json_file(initial_value, filepath)

def write_json_file(content, filepath, mode='w'):
    with open(filepath, mode) as file:
        json.dump(content, file, indent=2)


def read_json_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def read_json_at(filepath, key):
    data = read_json_file(filepath)
    if data[key] == 'True' or data[key] == 'true':
        return True
    elif data[key] == 'False' or data[key] == 'false':
        return False
    else:
        return data[key]

def update_json(filepath, key, value):
    data = read_json_file(filepath)
    data[key] = value
    write_json_file(data, filepath)


def contains(list, item):
    result = list.count(item)
    return result > 0
