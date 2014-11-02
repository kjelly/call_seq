import sys
import json
import os
import copy


def set_trace(trace_func=None, frame=None):
    """Start debugging from `frame`.

    If frame is not specified, debugging starts from caller's frame.
    """
    if frame is None:
        frame = sys._getframe().f_back
    while frame:
        frame.f_trace = trace_func
        frame = frame.f_back
    sys.settrace(trace_func)


def try_copy(data):
    # some inner structure use dict.
    if isinstance(data, dict):
        try:
            ret = {}
            for i in data:
                new_copy = try_copy(data[i])
                ret[i] = new_copy
            return ret
        except:
            pass
    try:
        # copy data
        return copy.deepcopy(data)
    except Exception as e:
        # if the data can't be copied
        pass
    # just return data.
    try:
        ret = {}
        for i in data:
            ret[i] = make_string(data[i])
        return ret
    except:
        pass
    return data


def read_source_code_from_file(file_name, lineno):
    if not os.path.exists(file_name):
        return ''
    with open(file_name, 'r') as ftr:
        source_code = ftr.readlines()
        return source_code[lineno - 1].strip()


def get_obj_type(obj, deep=True):
    ret = None
    try:
        if isinstance(obj, dict):
            ret = {}
            for key in iter(obj):
                if deep:
                    ret[key] = get_obj_type(obj[key], deep=False)
                else:
                    ret[key] = '<' + obj[key].__class__.__name__ + '>'
        elif isinstance(obj, list) or isinstance(obj, tuple):
            ret = []
            for ele in obj:
                if deep:
                    ret.append(get_obj_type(ele, deep=False))
                else:
                    ret.append('<' + ele.__class__.__name__ + '>')
        elif isinstance(obj, int):
                ret = '<' + obj.__class__.__name__ + '>: '
                ret += str(obj)
        elif isinstance(obj, str):
                ret = '<' + obj.__class__.__name__ + '>: '
                ret += repr(obj)
    except:
        ret = None
    if ret is None:
        try:
            ret = '<' + obj.__class__.__name__ + '>'
        except:
            ret = 'Error'
    return ret


class Encoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            pass
        try:
            return json.dumps(make_string(obj))
        except:
            pass
        return 'encode error'


def make_string(obj):
    try:
        return str(obj)
    except:
        pass
    try:
        return repr(obj)
    except:
        pass
    return 'error happened'


class FileManger(object):
    def __init__(self):
        self.cache = {}

    def read_file(self, file_name):
        if not file_name in self.cache:
            if not os.path.exists(file_name):
                self.cache[file_name]= ''
            else:
                with open(file_name, 'r') as ftr:
                    source_code = ftr.readlines()
                    self.cache[file_name]= source_code
        return self.cache[file_name]


    def get_line(self, file_name, lineno):
        lines = self.read_file(file_name)
        return lines[lineno - 1].strip()

    def get_content(self, file_name):
        lines = self.read_file(file_name)
        return ''.join(lines)

    def to_dict(self):
        return self.cache


