import os
import time
import modules.utilities as util
import modules as mod

file_path = r'.user\input.txt'
temp_file = r'.user\input_last-run.temp'


def compare_time(t1, t2):
    return t1 == t2


def is_input_updated():
    if os.path.exists(file_path):
        # get modification time of the file
        mod_time = os.path.getmtime(file_path)

        # convert the modification time to readable format
        read_mod_time = time.ctime(mod_time)

        if os.path.exists(temp_file):
            temp_info = util.read_file(temp_file)
            if compare_time(read_mod_time, temp_info):
                print('File has not been updated.')
                return False
            else:
                print('File has been updated.')
                util.write_file(read_mod_time, temp_file)
                return True
        else:
            print('Temp file not exist, writing temp file...')
            # write to temp file
            util.write_file(read_mod_time, temp_file)
            time.sleep(1)
            return True
    else:
        raise FileNotFoundError(f'File: {file_path} does not exist.')


def is_param_updated(param_val, param_infile_key):
    infile_val = util.read_json_at(mod.INFO.BRAIN_MEMO, param_infile_key)
    if infile_val != param_val:
        return True
