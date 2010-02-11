#!/usr/bin/env python

CATEGORIES_FILENAME = "../data/train/Categories.txt"
TRAIN_FILENAME = "../data/train/CategorizedQuerySample.txt"

# Read labels
import string
labels = []
origlabel_to_newlabel = {}
for l in open(CATEGORIES_FILENAME):
    l = string.strip(l)
    origl = l
    l = string.replace(l, "\\", ":")
    l = string.replace(l, " ", "_")
    labels.append(l)
    origlabel_to_newlabel[origl] = l

for e in open(TRAIN_FILENAME):
    v = string.split(string.strip(e), "\t")
    query = v[0]
    labels = [origlabel_to_newlabel[string.strip(l)] for l in v[1:]]
    print labels, query
