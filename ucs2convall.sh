#!/bin/sh

BASE='https://github.com/adobe-type-tools/mapping-resources-pdf/raw/master/mappingresources4pdf_2unicode'

conv() {
    curl -sL "${BASE}/$1" | ./ucs2conv.py > "$1.txt"
}

conv Adobe-CNS1-UCS2
conv Adobe-GB1-UCS2
conv Adobe-Japan1-UCS2
conv Adobe-Korea1-UCS2
