# python-tasks

# Tail
Write a program that prints N last lines of a file in reverse order (just like a tail -r FreeBSD command). Both file name and a number of lines to print shall be passed as command-line arguments.

Think of a memory-efficient yet fast way to implement this task.

# Proxy
Write a universal transparent proxy that is able to provide read/write access to attributes of any object instance being proxied.

For example, the following code snippet shall print Hello World!:
```python
  class A(object):

      phrase = 'Test'

      def test(self):
          print self.phrase

  proxy = Proxy(A())
  proxy.phrase = 'Hello World!'
  proxy.test()
```
In addition, a proxy shall count how many times a proxied object methods were called (separately for each method).

Note

A method can be accessed but not called, hence, you need to proxy method objects as well to fulfill this task. At the same moment, any read/write operation on method proxy shall be delegated to an original method as well.


# Producer-Consumers
Write an application which spawns several children threads or processes (based on a command line argument). A parent shall read from a file and put all lines into a queue. Children shall take those lines and append them into another file if and only if those lines start with a capital letter. An order of lines in a resulting file is not important, however, all lines shall be put intact. All threads (processes) shall exit gracefully after an input file ends and all necessary lines are put to output an file.

Compare a performance difference between the two solutions for alice.txt.

# TODO: Change Queue implementation for queue that support close method
# TODO: Add process implementation
