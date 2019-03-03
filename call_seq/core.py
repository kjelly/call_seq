import sys
import json
from .utils import get_obj_type, \
    Encoder, try_copy, set_trace, FileManger


class CallSeq(object):
    def __init__(self, pattern_list=None, name="sequence.json",
                 max_depth=None):
        self.name = name
        self.top_call_sequence = {'seq': [], 'name': '<top>'}
        self.cuurent_call_sequence = self.top_call_sequence
        self.pattern_list = pattern_list
        self.stack = [self.top_call_sequence]
        self.record_local_vars = False
        self.file_manager = FileManger()
        self.max_depth = max_depth
        self.depth = 0

    def reach_max_depth(self):
        if self.max_depth is None:
            return False
        return self.depth > self.max_depth

    def increase_depth(self):
        self.depth += 1

    def decrease_depth(self):
        self.depth -= 1

    def trace(self, frame, event, arg):
        if not frame.f_back or self.reach_max_depth():
            return self.trace
        if self.pattern_list:
            caller_code = frame.f_back.f_code
            caller_file_name = caller_code.co_filename
            for pattern in self.pattern_list:
                if pattern in caller_file_name:
                    break
            else:
                return self.trace
        if event in ['call']:
            self.increase_depth()
            self.record_local_vars = True
            caller_code = frame.f_back.f_code
            caller_file_name = caller_code.co_filename
            caller = self.file_manager.get_line(caller_file_name,
                                                frame.f_back.f_lineno)
            callee_code = frame.f_code
            callee_file_name = callee_code.co_filename
            new_call_sequence = {
                'caller_code': caller, 'seq': [],
                'lineno': frame.f_back.f_lineno,
                'caller_file_name': caller_file_name,
                'callee_first_line': callee_code.co_firstlineno,
                'callee_file_name': callee_file_name,
            }

            self.stack[-1]['seq'].append(new_call_sequence)
            self.stack.append(new_call_sequence)

        elif event in ['return']:
            if self.stack[-1] is self.top_call_sequence:
                return self.trace
            self.decrease_depth()
            return_lineno = frame.f_lineno
            # self.stack[-1]['return'] = make_string(arg)
            self.stack[-1]['return'] = get_obj_type(arg)
            self.stack[-1]['return_lineno'] = return_lineno
            self.stack.pop()
            caller_code = frame.f_back.f_code
            self.stack[-1]['name'] = caller_code.co_name

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
            data = {
                'trace': self.to_dict(),
                'code': self.file_manager.to_dict()
            }
            ftr.write(json.dumps(data, sort_keys=True, skipkeys=True,
                                 indent=4, separators=(',', ': '),
                                 cls=Encoder))

    def __enter__(self):
        self.set_trace()

    def __exit__(self, type, value, traceback):
        self.unset_trace()
        self.dump_to_file(self.name)


if __name__ == '__main__':
    output_name = sys.argv[1]
    file_name = sys.argv[2]
    seq = CallSeq()
    seq.set_trace()
    execfile(file_name)
    seq.unset_trace()
    seq.dump_to_file(output_name)
