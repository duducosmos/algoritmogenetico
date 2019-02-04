#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-

from numpy import array


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def binarray2int(x):
    cnt = array([2 ** i for i in range(x.shape[1])])
    return array([(cnt * x[i,:]).sum()
                  for i in range(x.shape[0])]).reshape(1, x.shape[0])
