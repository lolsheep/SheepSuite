#!/usr/bin/env python3
import sys
import random
from datetime import datetime, date

# def progress_bar(index, total, file):
#     print('\n')
#     total = total - 1
#     bar_length = 60
#     bar_filled = int(round(bar_length * index / float(total)))
#     percent = round(100.0 * index / float(total),2)
#     p_bar = "/" *  bar_filled + ( "-" * (bar_length - bar_filled))
#     sys.stdout.write("[%s]  %s%% [%s]\r" % (p_bar,percent,file))
#     sys.stdout.flush()
#     if int(percent) == 100:
#         print('\r')


def return_date():
    return str(date.today())
def return_datetime():
    return str(datetime.now())
