#!/usr/bin/python
# coding: utf-8
#
# https://github.com/adobe-type-tools/mapping-resources-pdf
# に掲載されている ToUnicode マッピングをC言語から利用しやすい形に
# 整形する。
#
# 次のようにして、C言語ソースに組み込める。
# あとはbsearchを使って検索できる。
#
# struct x {
#     unsigned int cid;
#     const char *const ucs2;
# } const x[] = {
# #include "Adobe-Japan1-UCS2.txt"
# };
#
# x[].ucs2 の先頭は後続の有効バイト数
# (バイト中に'\0'を含むため'\0'を終端マーカーとして使えないため)
#

import fileinput
import re

def cmap(x, offset):
    xs = [int(x[i:i+2], 16) for i in range(0, len(x), 2)]
    if 0 < offset:
        to = xs[-1] + offset
        if 255 < to:
            xs[-1] = (to % 256)
            xs[-2] = xs[-2] + 1
        else:
            xs[-1] = to
        True
    return xs

def mapc(a, b, d):
    x = int(a, 16)
    d[x] = cmap(b, 0)

def mapr(a, b, c, d):
    x = int(a, 16)
    y = int(b, 16)
    for v in range(x, y + 1):
        d[v] = cmap(c, v - x)

bfchar = re.compile(r"(begin|end)bfchar")
bfrange = re.compile(r"(begin|end)bfrange")
mapchar = re.compile(r"<([0-9A-Fa-f]{4})>\s*<([0-9A-Fa-f]{4,})>")
maprange = re.compile(r"<([0-9A-Fa-f]{4})>\s*<([0-9A-Fa-f]{4})>\s*<([0-9A-Fa-f]{4,})>")

in_char = False
in_range = False
to_map = {}

for line in fileinput.input():
    m = bfchar.search(line)
    if m:
        be = m.group(1)
        if be == "begin":
            in_char = True
        elif be == "end":
            in_char = False
    m = bfrange.search(line)
    if m:
        be = m.group(1)
        if be == "begin":
            in_range = True
        elif be == "end":
            in_range = False
    if in_char:
        m = mapchar.search(line)
        if m:
            mapc(m.group(1), m.group(2), to_map)
    if in_range:
        m = maprange.search(line)
        if m:
            mapr(m.group(1), m.group(2), m.group(3), to_map)

for x in sorted(to_map.keys()):
    v = to_map.get(x)
    s = "".join([("\\x%02X" % i) for i in v])
    print "{0x%04X, \"\\x%02X%s\"}," % (x, len(v), s)
