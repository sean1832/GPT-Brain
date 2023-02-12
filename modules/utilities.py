import json
import os


# def extract_string(text, delimiter):
#     # Extract string between delimiters
#     start_index = text.index(delimiter) + len(delimiter)
#     end_index = text.index(delimiter, start_index)
#     return text[start_index:end_index]


def extract_string(text, delimiter, force=False, join=True, split_mode=False):
    if not delimiter in text:
        if force:
            return ''
        else:
            return text
    else:
        if split_mode:
            return text.split(delimiter)
        else:
            substring = text.split(delimiter)
            result = []
            for i in range(1, len(substring), 2):
                result.append(substring[i])
            if join:
                return ''.join(result)
            else:
                return result


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
        return parse_data(data, delimiter, force)


def parse_data(data, delimiter='', force=False):
    if delimiter != '':
        data = extract_string(data, delimiter, force)
    return data


def read_files(file_dir, delimiter='', force=False, single_string=True):
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
    if single_string:
        result = '\n\n\n\n'.join(contents)
    else:
        result = contents
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
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def read_json_at(filepath, key, default_value=''):
    data = read_json_file(filepath)
    try:
        # if key is string, check if it is boolean or numeric
        if isinstance(data[key], str):
            if data[key] in ['true', 'false']:
                return data[key] == 'true'
            elif data[key].isnumeric():
                return int(data[key])
            elif data[key].replace('.', '', 1).isnumeric():
                return float(data[key])
            else:
                return data[key]
        else:
            return data[key]
    except KeyError:
        # if key not found, create key with default value
        data[key] = default_value
        write_json_file(data, filepath)
        return data[key]


def update_json(filepath, key, value):
    data = read_json_file(filepath)
    data[key] = value
    write_json_file(data, filepath)


def contains(list, item):
    result = list.count(item)
    return result > 0