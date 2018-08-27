#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

def write_file(file):
    with open(file, 'a') as f:
        f.write(str(datetime.datetime.now()) + '\n')
    f.close()

file = '/Users/liu/test.txt'
write_file(file)
