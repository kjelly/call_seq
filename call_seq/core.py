import sys
import os
import copy
import json


def try_copy(data):
    # some inner structure use dict.
    if isinstance(data, dict):
        ret = {}
        for i in data:
            new_copy = try_copy(data[i])
            if new_copy:
                ret[i] = new_copy
        return ret
    else:
        try:
            # copy data
            return copy.deepcopy(data)
        except Exception as e:
            # if the data can't be copied
            pass
    # just return data.
    return data


def read_source_code_from_file(file_name, lineno):
    if not os.path.exists(file_name):
        return ''
    with open(file_name, 'r') as ftr:
        source_code = ftr.readlines()
        return source_code[lineno - 1].strip()


class CallSeq(object):
    def __init__(self, pattern_list=None):
        self.top_call_sequence = {'seq': [], 'name': '<top>'}
        self.cuurent_call_sequence = self.top_call_sequence
        self.pattern_list = pattern_list
        self.stack = [self.top_call_sequence]

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
            self.stack[-1]['return'] = str(arg)
            self.stack[-1]['return_lineno'] = return_lineno
            self.stack.pop()

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
                      indent=4, separators=(',', ': ')))


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
