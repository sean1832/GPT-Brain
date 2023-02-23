import json
import os
import glob


def extract_string(text, delimiter, force=False, join=True, split_mode=False):
    # Check if delimiter is not in text
    if delimiter not in text:
        # If force is True, return empty string; otherwise, return the original text
        return '' if force else text
    # If split_mode is True, split text by delimiter and return the resulting list
    elif split_mode:
        return text.split(delimiter)
    else:
        substring = text.split(delimiter)
        result = []
        # Split text by delimiter and select every second item starting from the second one
        for i in range(1, len(substring), 2):
            result.append(substring[i])
        # If join is True, join the resulting list into a string and return it; otherwise, return the list
        return ''.join(result) if join else result


def remove_oldest_file(directory, max_files):
    files = scan_directory(directory)
    if len(files) >= max_files:
        oldest_file = min(files, key=os.path.getctime)
        os.remove(oldest_file)


def scan_directory(directory, include_subdir=False, exclude=None):
    if include_subdir:
        files = glob.glob(f'{directory}/*', recursive=True)
    else:
        files = glob.glob(f'{directory}/*.*')
    if exclude is not None:
        filtered_files = []
        for file in files:
            excluded = False
            for exclude_dir in exclude:
                if exclude_dir in file:
                    excluded = True
                    break
            if not excluded:
                filtered_files.append(file)
    return files


# get file name without extension
def get_file_name(filepath, extension=False):
    if extension:
        return os.path.basename(filepath)
    else:
        return os.path.splitext(os.path.basename(filepath))[0]


def create_path_not_exist(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


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


def read_files(file_dir, delimiter='', force=False, single_string=True, exclude_dir: list = None, supported_formats: list = None):
    contents = []
    if exclude_dir is None:
        exclude_dir = []
    if supported_formats is None:
        supported_formats = ['.txt', '.md']
    # Read all files in a directory
    for root, dirs, files in os.walk(file_dir):
        # Check if root is in excluded directories
        if any(dir in root for dir in exclude_dir):
            continue
        for file in files:
            # extract file path
            filepath = os.path.join(root, file)
            # extract filename with extension
            filename = os.path.basename(filepath)
            # extract filename without extension
            filename = os.path.splitext(filename)[0]

            # Check if filepath contains any excluded directories
            if any(dir in filepath for dir in exclude_dir):
                continue
            # Check if file extension is in supported formats
            if not any(file.endswith(format) for format in supported_formats):
                continue

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
    create_path_not_exist(filepath)
    with open(filepath, mode, encoding='utf-8') as file:
        file.write(content)


def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


def create_json_not_exist(filepath, initial_value={}):
    if not os.path.exists(filepath):
        write_json(initial_value, filepath)


def write_json(content, filepath, mode='w', encoding='UTF-8'):
    with open(filepath, mode, encoding=encoding) as file:
        json.dump(content, file, indent=2)


def read_json(filepath, encoding='UTF-8', default_value={}):
    try:
        with open(filepath, 'r', encoding=encoding) as file:
            return json.load(file)
    except FileNotFoundError:
        create_json_not_exist(filepath, default_value)
        return {}


def read_json_at(filepath, key, default_value=''):
    data = read_json(filepath)
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
        write_json(data, filepath)
        return data[key]


def update_json(filepath, key, value):
    data = read_json(filepath)
    data[key] = value
    write_json(data, filepath)


def contains(ls: list, item):
    result = ls.count(item)
    return result > 0


def get_index(ls: list, item, default=0) -> int:
    try:
        return ls.index(item)
    except ValueError:
        return default


def extract_frontmatter(content, delimiter='---'):
    # extract metadata
    try:
        yaml = extract_string(content, delimiter, True, join=False, split_mode=True)[1]
    except IndexError:
        yaml = ''
    fields = yaml.split('\n')
    return fields
