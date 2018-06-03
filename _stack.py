# -*- coding: utf-8 -*-
'''
 * @Author: ZQ.Pei 
 * @Date: 2018-06-03 16:59:39 
 * @Last Modified by:   ZQ.Pei 
 * @Last Modified time: 2018-06-03 16:59:39 
'''

class Stack(object):
    def __init__(self):
        self._item = []

    def push(self, value):
        self._item.append(value)

    def pop(self):
        return self._item.pop()

    def size(self):
        return len(self._item)

    def is_empty(self):
        return True if self.size() == 0 else False

    def empty(self):
        self._item = []

    
