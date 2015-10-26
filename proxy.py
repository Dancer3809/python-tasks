#!/usr/bin/env python
import inspect

class ProxyMethodWrapper:
    """
    Wrapper object for a method to be called.
    """
    def __init__( self, obj, func, name ):
        self.obj, self.func, self.name = obj, func, name
        self.count = 0

    def __call__( self, *args, **kwds ):
        self.count = self.count + 1
        print "Method count:{}".format(self.count)
        return self.func(*args, **kwds)

class Proxy(object):
    """
    Proxy class
    """
    def __init__(self, impl):
        self.__impl = impl
        # Wrap all impl methods
        for method in inspect.getmembers(impl, predicate=inspect.ismethod):
            self.__wrap(method[0], method[1])

    def __wrap(self, name, value):
            wrapper = ProxyMethodWrapper(self.__impl, value, name)
            setattr(self.__impl, name, wrapper)

    def __setattr__(self, name, value):
        if name == "_{}__impl".format(self.__class__.__name__):
            object.__setattr__(self, name, value)
        else:
            self.__wrap(name, value)

    def __setitem__( self, key, value ):
            self.__wrap(key, value)

    def __getattr__(self, name):
        return getattr(self.__impl, name)


if __name__ == '__main__':
    class A(object):
        phrase = 'Test'
        def test(self):
            print self.phrase

    def new_func():
        print "new func:{}"


    proxy = Proxy(A())
    proxy.test()

    proxy.test = new_func
    proxy.test()
    proxy.test()
    proxy['test'] = new_func
    proxy.test()
    proxy.test()

