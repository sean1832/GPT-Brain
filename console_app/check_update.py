import os
import time
import utilities

file_path = r'.user\input.txt'
temp_file = r'.user\input_last-run.temp'
sig_file = r'.user\input_sig.temp'

def compare_time(t1, t2):
    return t1 == t2

def write_sig(bool):
    utilities.write_file(bool, sig_file)

def check():
    if os.path.exists(file_path):
        # get modification time of the file
        mod_time = os.path.getmtime(file_path)

        # convert the modification time to readable format
        read_mod_time = time.ctime(mod_time)

        if os.path.exists(temp_file):
            temp_info = utilities.open_file(temp_file)
            if compare_time(read_mod_time, temp_info):
                write_sig('not updated')
                print('File has not been updated.')
            else:
                print('File has been updated.')
                utilities.write_file(read_mod_time, temp_file)
                write_sig('updated')
        else:
            print('Temp file not exist, writing temp file...')
            # write to temp file
            utilities.write_file(read_mod_time, temp_file)
            write_sig('not updated')
    else:
        raise FileNotFoundError(f'File: {file_path} does not exist.')

def main():
    check()
    
if __name__ == '__main__':
    main()