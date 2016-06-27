#!/usr/bin/env python

def fib(n):
    if n == 0:
        return n
    elif n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
        # fibIx = fib(n - 1) + fib(n - 2)
        # print 'fibIx: %s ' % fibIx
        # return fibIx

if __name__ == '__main__':
      x = fib(5)
      print x
