from call_seq import trace


def test2():
    pass


def test1():
    test2()
    return 1 + 1


def test():
    test1()
    print 'call me'
    test1()


@trace('output.json')
def main():
    test()


if __name__ == '__main__':
    main()

