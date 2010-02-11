#!/usr/bin/env python
"""
TODO: Add different example weighting.
"""

import sys, string
from os.path import join
import os.path, os
from os.path import join
BASEDIR = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

CATEGORIES_FILENAME = join(BASEDIR, "data/train/Categories.txt")
TRAIN_FILENAME = join(BASEDIR, "data/train/CategorizedQuerySample.txt")

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-n", "--name", dest="name", help="Name of this run")
(options, args) = parser.parse_args()
assert len(args) == 0
assert options.name is not None

all_labels, origlabel_to_newlabel = None, None
def read_labels():
    global all_labels, origlabel_to_newlabel

    # Read labels
    all_labels = []
    origlabel_to_newlabel = {}
    for l in open(CATEGORIES_FILENAME):
        l = string.strip(l)
        origl = l
        l = string.replace(l, "\\", ":")
        l = string.replace(l, " ", "_")
        all_labels.append(l)
        origlabel_to_newlabel[origl] = l



workdir = join(BASEDIR, "work/%s" % options.name)
print >> sys.stderr, "Working in directory: %s" % workdir
if not os.path.exists(workdir): os.mkdir(workdir)
assert os.path.isdir(workdir)

read_labels()

label_to_trainfile = {}
for l in all_labels:
    trainfile = open(join(workdir, "trainfeature.%s.txt" % l), "wt")
    label_to_trainfile[l] = trainfile

for e in open(TRAIN_FILENAME):
    v = string.split(string.strip(e), "\t")
    query = v[0]
    labels = [origlabel_to_newlabel[string.strip(l)] for l in v[1:]]

    for l in all_labels:
        if l in labels: outl = l
        else: outl = "NOT-%s" % l
        label_to_trainfile[l].write("%s %s\n" % (outl, query))
#    print labels, query
