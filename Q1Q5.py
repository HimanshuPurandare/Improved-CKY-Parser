#!/usr/bin/env python
import sys, fileinput
import tree
str_to_write = ""
def create_grammar(root):
    print root.label, "->",
    for i in root.children:
        print i.__str__(),
    print
    for ii in root.children:
        if ii.children:
            create_grammar(ii)
def main():
    for line in fileinput.input():
        t = tree.Tree.from_str(line)
        create_grammar(t.root)
main()
