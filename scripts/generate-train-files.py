#!/usr/bin/env python

CATEGORIES_FILENAME = "../data/train/Categories.txt"
TRAIN_FILENAME = "../data/train/CategorizedQuerySample.txt"

# Read labels
import string
labels = []
for l in open(CATEGORIES_FILENAME):
    l = string.strip(l)
    l = string.replace(l, "\\", ":")
    l = string.replace(l, " ", "_")
    labels.append(l)
