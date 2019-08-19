#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

grep version $DIR/setup.py | cut -d= -f2 | cut -d\' -f2
