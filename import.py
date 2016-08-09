#!/usr/bin/env python
from parser import LogParser
from sys import stdin

def main():
    parser = LogParser(stdin)
    parser.readCommits()

if __name__ == "__main__":
    main()
