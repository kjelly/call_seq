import sys
import os
import copy
import json


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


class CallSeq(object):
    def __init__(self, pattern_list=None):
        self.top_call_sequence = {'seq': [], 'name': '<top>'}
        self.cuurent_call_sequence = self.top_call_sequence
        self.pattern_list = pattern_list
        self.stack = [self.top_call_sequence]
        self.record_local_vars = False

    def trace(self, frame, event, arg):
        if not frame.f_back:
            return self.trace
        if self.pattern_list:
            code = frame.f_back.f_code
            file_name = code.co_filename
            for pattern in self.pattern_list:
                if pattern in file_name:
                    break
            else:
                return self.trace
        if event in ['call']:
            self.record_local_vars = True
            code = frame.f_back.f_code
            file_name = code.co_filename
            callee = read_source_code_from_file(file_name,
                                                frame.f_back.f_lineno)
            new_call_sequence = {'code': callee, 'seq': [],
                                 'lineno': frame.f_back.f_lineno,
                                 'file_name': file_name}

            self.stack[-1]['seq'].append(new_call_sequence)
            self.stack.append(new_call_sequence)

        elif event in ['return']:
            if self.stack[-1] is self.top_call_sequence:
                return self.trace
            return_lineno = frame.f_lineno
            # self.stack[-1]['return'] = make_string(arg)
            self.stack[-1]['return'] = get_obj_type(arg)
            self.stack[-1]['return_lineno'] = return_lineno
            self.stack.pop()
        elif self.record_local_vars:
            self.record_local_vars = False
            # self.stack[-1]['arguments'] = try_copy(frame.f_locals)
            self.stack[-1]['arguments'] = get_obj_type(frame.f_locals)

        return self.trace

    def to_dict(self):
        return try_copy(self.top_call_sequence)

    def set_trace(self):
        set_trace(self.trace)

    def unset_trace(self):
        set_trace(None)

    def dump_to_file(self, path):
        with open(path, 'w') as ftr:
            ftr.write(json.dumps(self.to_dict(), sort_keys=True,
                      indent=4, separators=(',', ': '), cls=Encoder))


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


if __name__ == '__main__':
    output_name = sys.argv[1]
    file_name = sys.argv[2]
    seq = CallSeq()
    seq.set_trace()
    execfile(file_name)
    seq.unset_trace()
    seq.dump_to_file(output_name)
