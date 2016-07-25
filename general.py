import os


OUT_DIR = r'crawled'
OUT_FILE = os.path.join(OUT_DIR, 'crawled.txt')


def create_project_dir():
    if not os.path.exists(OUT_DIR):
        print('Creating directory: ' + OUT_DIR)
        os.makedirs(OUT_DIR)


def create_data_file():
    if not os.path.isfile(OUT_FILE):
        write_file(OUT_FILE, '')


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def append_to_file(path, data):
    with open(path, 'a') as f:
        f.write(data + '\n')


def delete_file_contents(path):
    open(path, 'w').close()


def file_to_set(file_name):
    results = set()
    with open(file_name) as f:
        for line in f:
            results.add(line.replace('\n', ''))


def set_to_file(set, file_name):
    with open(file_name, 'w') as f:
        for item in sorted(set):
            f.write(item + '\n')
