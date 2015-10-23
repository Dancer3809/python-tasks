class Proxy(object):
    def __init__(self, impl):
        self.__impl = impl

    def __setattr__(self, name, value):
        print self.__class__
        if name == "_%s__impl" % self.__class__.__name__:
            object.__setattr__(self, name, value)
        else:
            self.__impl.__setattr__(name, value)

    def __getattr__(self, name):
        return getattr(self.__impl, name)

class A(object):

    phrase = 'Test'

    def test(self):
        print self.phrase

if __name__ == "__main__":
    proxy = Proxy(A())
    proxy.phrase = 'Hello World!'
    proxy.test()
