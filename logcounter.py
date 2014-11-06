#coding:utf-8
#!/usr/bin/env python

"""非堵塞的日志统计"""
import datetime
import array
import getopt
import os
import sys
import time
import fcntl
import select
from logcolor import *


SEP = "\n"
SECS_1M = 60


def usage():
    """Usage help"""
    print "USAGE: tail -f access_log1 access_log2 access_logN | rps"


def parse_args():
    """Args parser"""
    try:
        opts = getopt.getopt(sys.argv[1:], "h", ["help"])[0]
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(-1)
    for opt in opts:
        if opt[0] in ("-h", "--help"):
            usage()
            sys.exit()


def prepare_stdin():
    """Makes stdin non-blocking"""
    try:
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
    except IOError:
        print "SORRY, could not make stdin non-blocking"
        sys.exit(-2)


def main():
    """Parsing args & processing stdin"""
    parse_args()
    prepare_stdin()
    buf = ""
    total_reqs = 0
    stat_1m = array.array('I')

    print "Use Ctrl + C to terminate the program"

    while True:
        time_left, cnt = 1.0, 0
        while time_left >= 0:
            time_start = time.time()
            try:
                rlist = select.select([sys.stdin], [], [], time_left)[0]
            except KeyboardInterrupt:
                print "BYE, %d total reqs" % total_reqs
                sys.exit(0)
            if not rlist:
                break
            time_left -= (time.time() - time_start)
            buf += sys.stdin.read()
            try:
                ridx = buf.rindex(SEP)
            except ValueError:
                continue
            idx = 0
            while True:
                idx = buf.find(SEP, idx, ridx)
                if idx == -1:
                    break
                cnt += 1
                idx += 1
            cnt += 1
            buf = buf[ridx + 1:]

        total_reqs += cnt
        if len(stat_1m) == SECS_1M:
            stat_1m.pop(0)
        stat_1m.append(cnt)
        str = ("%d/%d (rps/min avg)" % (cnt, round(float(sum(stat_1m)) /
                                            len(stat_1m))))
        print use_style(str, fore='black', back='white')


if __name__ == "__main__":
    main()
