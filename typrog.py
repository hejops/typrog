#!/usr/bin/env python3
"""Simple typing test, inspired by http://wpm-test.com/programming-typing-test,
but with sample texts derived from local files, in any language.
"""

import configparser
import os
import sys
import time
from random import choice
from subprocess import getstatusoutput
from textwrap import wrap

from readchar import readchar


def main(
    *words: str,
    max_words: int = 25,
):
    start = 0
    lines = wrap(" ".join(words[:max_words]), 80)
    lines_done = []
    curr_line_typed = ""

    for curr_line in lines:
        while curr_line_typed != curr_line:
            os.system("clear")
            print(lang)
            if lines_done:
                print("\n".join("  " + l for l in lines_done))
            print("> " + curr_line)
            print("  " + curr_line_typed)

            char = readchar()

            if char == "\t":
                sys.exit()

            if char == curr_line[len(curr_line_typed)]:
                curr_line_typed += char
                if len(curr_line_typed) == 1 and not lines_done:
                    start = time.time()

        lines_done.append(curr_line)
        curr_line_typed = ""

    os.system("clear")
    print(lang)
    print("\n".join("  " + l for l in lines_done))

    end = time.time()
    wpm = max_words // ((end - start) / 60)
    print(wpm, "wpm")


config = configparser.ConfigParser()
config.read("config")

LANGS = dict(config["languages"])
lang = choice(list(LANGS))
cmd = LANGS[lang]

status, output = getstatusoutput(
    "set -o pipefail ; "
    + cmd
    # select 3 files, deduplicate their lines, get random 25 lines
    + " | shuf -n3 | xargs sort -u | grep -v '://' | shuf -n25"
)

if status != 0:
    print("Command failed:", cmd)
    sys.exit()

words = [word for line in output.split("\n") for word in line.split()]
main(*words)
