call_seq
===========

  call_seq is a tool that let you trace code easily. It record function call sequence.
   So you can learn how the process run.


How to install
----------------

```sh
pip install git+https://github.com/ya790206/call_seq
```


How to use
-------------

  ```python
    from call_seq import CallSeq

    trail = CallSeq()
    trail.set_trace()
    # the code you want to trace.
    trail.unset_trace()
    trail.dump_to_file('output.json')
  ```

  or

  ```python
    @trace('output.json')
    def main():
        test()

  ```



  ```python
    if __name__ == '__main__':
        with CallSeq(name='output.json'):
            test()
  ```

  or

  ```sh
    $ python -m call_seq.core output.json demo1.py
  ```

  Now you can read the `output.json` file.

  The file output is maybe like

  ``` json
{
    "name": "inner",
    "seq": [
        {
            "arguments": {},
            "callee_file_name": "demo3.py",
            "callee_first_line": 19,
            "caller_code": "ret = func(*args, **kwargs)",
            "caller_file_name": "/home/ya790206/call_seq/call_seq/__init__.py",
            "lineno": 9,
            "name": "main",
            "return": "<NoneType>",
            "return_lineno": 21,
            "seq": [
                {
                    "arguments": {},
                    "callee_file_name": "demo3.py",
                    "callee_first_line": 13,
                    "caller_code": "test()",
                    "caller_file_name": "demo3.py",
                    "lineno": 21,
                    "name": "test",
                    "return": "<NoneType>",
                    "return_lineno": 16,
                    "seq": [
                        {
                            "arguments": {},
                            "callee_file_name": "demo3.py",
                            "callee_first_line": 8,
                            "caller_code": "test1()",
                            "caller_file_name": "demo3.py",
                            "lineno": 14,
                            "name": "test1",
                            "return": "<int>: 2",
                            "return_lineno": 10,
                            "seq": [
                                {
                                    "arguments": {},
                                    "callee_file_name": "demo3.py",
                                    "callee_first_line": 4,
                                    "caller_code": "test2()",
                                    "caller_file_name": "demo3.py",
                                    "lineno": 9,
                                    "return": "<NoneType>",
                                    "return_lineno": 5,
                                    "seq": []
                                }
                            ]
                        },
                        {
                            "arguments": {},
                            "callee_file_name": "demo3.py",
                            "callee_first_line": 8,
                            "caller_code": "test1()",
                            "caller_file_name": "demo3.py",
                            "lineno": 16,
                            "name": "test1",
                            "return": "<int>: 2",
                            "return_lineno": 10,
                            "seq": [
                                {
                                    "arguments": {},
                                    "callee_file_name": "demo3.py",
                                    "callee_first_line": 4,
                                    "caller_code": "test2()",
                                    "caller_file_name": "demo3.py",
                                    "lineno": 9,
                                    "return": "<NoneType>",
                                    "return_lineno": 5,
                                    "seq": []
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "arguments": {
                "self": "<CallSeq>"
            },
            "callee_file_name": "/home/ya790206/call_seq/call_seq/core.py",
            "callee_first_line": 69,
            "caller_code": "trail.unset_trace()",
            "caller_file_name": "/home/ya790206/call_seq/call_seq/__init__.py",
            "lineno": 10,
            "seq": [
                {
                    "arguments": {
                        "frame": "<NoneType>",
                        "trace_func": "<NoneType>"
                    },
                    "callee_file_name": "/home/ya790206/call_seq/call_seq/utils.py",
                    "callee_first_line": 7,
                    "caller_code": "set_trace(None)",
                    "caller_file_name": "/home/ya790206/call_seq/call_seq/core.py",
                    "lineno": 70,
                    "seq": []
                }
            ]
        }
    ]
}
  ```

  You can open the file using [call_seq_browser](https://github.com/ya790206/call_seq_browser)

  call_seq_browser help you to trace code more easy.

  ``` sh
    python -m call_seq_browser output.json
  ```
  
  
  See [call_seq_browser](https://github.com/ya790206/call_seq_browser) for more.

Screen snapshot
-----------------

![Screen snapshot1](https://raw.githubusercontent.com/ya790206/call_seq/master/snapshot/explain.png "Screen snapshot1")


Known limit.
-----------------

  * You can't set_trace twice.
  * It can't work with pdb or anything like pdb.
  * set_trace and unset_trace need to be called in the same frame. So it doesn't work if you call set_trace
     in function A and call unset_trace in function B.



Special thanks
----------------------

Thanks to JetBrains for providing pycharm open source license to the project.
