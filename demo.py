from call_seq import CallSeq


def test2():
    pass


def test1():
    test2()
    return 1 + 1


def test():
    test1()
    print 'call me'
    test1()


if __name__ == '__main__':
    map = CallSeq()
    map.set_trace()
    test()
    map.unset_trace()
    map.dump_to_file('output.json')
