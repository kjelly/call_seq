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

    map = CallSeq()
    map.set_trace()
    # the code you want to trace.
    map.unset_trace()
    map.dump_to_file('output.json')
  ```

  or

  ```sh
    $ python -m call_seq.core output.json demo1.py
  ```

  Now you can read the `output.json` file.

  The file output is maybe like

  ``` json
  {
    "name": "<top>",
    "seq": [
        {
            "code": "test()",
            "file_name": "/home/ya790206/PycharmProjects/call_seq/demo.py",
            "lineno": 24,
            "return": "None",
            "return_lineno": 16,
            "seq": [
                {
                    "code": "test1()",
                    "file_name": "/home/ya790206/PycharmProjects/call_seq/demo.py",
                    "lineno": 14,
                    "return": "2",
                    "return_lineno": 10,
                    "seq": [
                        {
                            "code": "test2()",
                            "file_name": "/home/ya790206/PycharmProjects/call_seq/demo.py",
                            "lineno": 9,
                            "return": "None",
                            "return_lineno": 5,
                            "seq": []
                        }
                    ]
                },
                {
                    "code": "test1()",
                    "file_name": "/home/ya790206/PycharmProjects/call_seq/demo.py",
                    "lineno": 16,
                    "return": "2",
                    "return_lineno": 10,
                    "seq": [
                        {
                            "code": "test2()",
                            "file_name": "/home/ya790206/PycharmProjects/call_seq/demo.py",
                            "lineno": 9,
                            "return": "None",
                            "return_lineno": 5,
                            "seq": []
                        }
                    ]
                }
            ]
        },
        {
            "code": "map.unset_trace()",
            "file_name": "/home/ya790206/PycharmProjects/call_seq/demo.py",
            "lineno": 25,
            "seq": [
                {
                    "code": "set_trace(None)",
                    "file_name": "/home/ya790206/PycharmProjects/call_seq/call_seq/core.py",
                    "lineno": 82,
                    "seq": []
                }
            ]
        }
    ]
  ```

  You can open the file using browser.py

  browser.py help you to trace code more easy.

  ``` sh
    python -m call_seq.browser demo.json
  ```
  
  If you want to use browser.py, you need to install the below package.
  
  ```
    pyside
    pyqode.core
    pyqode.python
    
  ```


Known limit.
-----------------

  * You can't set_trace twice.
  * It can't work with pdb or anything like pdb.
  * set_trace and unset_trace need to be called in the same frame. So it doesn't work if you call set_trace
     in function A and call unset_trace in function B.


