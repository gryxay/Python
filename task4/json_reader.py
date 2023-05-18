import json
import os

def load_data(file_path, obj_class):
    assert(os.path.getsize(file_path) > 0), f'Empty file encountered: {file_path}'
    with open(file_path, 'r') as f:
        data = json.load(f)
        objects = [obj_class.from_json(obj_data) for obj_data in data]
        return objects

def write_json_to_file(file_path, object_list, mode='w'):
    with open(file_path, mode) as f:
        json_strings = [json.dumps(obj.to_json(), indent=4) for obj in object_list]
        f.write(f'[\n' + ',\n'.join(json_strings) + '\n]')

__all__ = ['load_data', 'write_json_to_file']