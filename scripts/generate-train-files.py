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
DEV_TRAIN_FILENAME = join(BASEDIR, "data/train/CategorizedQuerySample.txt")

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-n", "--name", dest="name", help="Name of this run")
parser.add_option("--dev", dest="dev", action="store_true", help="Train on train-partition and evaluate on dev-partiton", default=True)
parser.add_option("--test", dest="dev", action="store_false", help="Train on train and evaluate on dev")
parser.add_option("--l2", dest="l2", help="l2 sigma", type="string")
(options, args) = parser.parse_args()
assert len(args) == 0
assert options.name is not None

if options.dev:
    TRAIN_FILENAME = join(BASEDIR, "data/train/CategorizedQuerySample.train-partition.txt")
    EVAL_FILENAMES = [join(BASEDIR, "data/train/CategorizedQuerySample.dev-partition.txt")]
else:
    assert 0

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

def read_labeled_queries(filename):
    """
    Read a labeled queries file.
    Return a list of (query, list of labels)
    """
    examples = []
    for e in open(filename):
        v = string.split(string.strip(e), "\t")
        query = v[0]
        labels = [origlabel_to_newlabel[string.strip(l)] for l in v[1:]]
        examples.append((query, labels))
    return examples

def run(cmd):
    print >> sys.stderr, cmd
    print >> sys.stderr, stats()
    os.system(cmd)
    print >> sys.stderr, stats()




if options.dev: workdir = join(BASEDIR, "work/%s/dev/" % options.name)
else: workdir = join(BASEDIR, "work/%s/test/" % options.name)
print >> sys.stderr, "Working in directory: %s" % workdir
if not os.path.exists(workdir): os.makedirs(workdir)
assert os.path.isdir(workdir)

read_labels()


# Generate features
for l in all_labels:
    featurestrainfile = open(join(workdir, "features.train.l2=%s.%s.txt" % (options.l2, l)), "wt")
    for query, labels in read_labeled_queries(TRAIN_FILENAME):
        featurestrainfile.write("%d %s\n" % (l in labels, query))

    for i in range(len(EVAL_FILENAMES)):
        featuresevalfile = open(join(workdir, "features.eval%d.l2=%s.%s.txt" % (i, options.l2, l)), "wt")
        for query, labels in read_labeled_queries(EVAL_FILENAMES[i]):
            featuresevalfile.write("%d %s\n" % (l in labels, query))

    modelfile = join(workdir, "model.l2=%s.%s.txt" % (options.l2, l))

    cmd = "megam -lambda %s %s > %s" % (options.l2, featurestrainfile, modelfile)
    print cmd

#    print labels, query
