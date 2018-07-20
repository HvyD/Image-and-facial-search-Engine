#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:02:50 2018

@author: hvyd
"""

import numpy as np
import argparse
import cPickle
import cv2
 
class Searcher:
	def __init__(self, index):
		# store our index of images
		self.index = index
 
	def search(self, queryFeatures):
		# initialize our dictionary of results
		results = {}
 
		# loop over the index
		for (k, features) in self.index.items():
			d = self.chi2_distance(features, queryFeatures)
			results[k] = d
 
		results = sorted([(v, k) for (k, v) in results.items()])
 
		# return our results
		return results
 
	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
 
		# return the chi-squared distance
		return d

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images we just indexed")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where we stored our index")
args = vars(ap.parse_args())
 
# load the index and initialize our searcher
index = cPickle.loads(open(args["index"]).read())
searcher = Searcher(index)

for (query, queryFeatures) in index.items():
	# perform the search using the current query
	results = searcher.search(queryFeatures)
 
	# load the query image and display it
	path = args["dataset"] + "/%s" % (query)
	queryImage = cv2.imread(path)
	cv2.imshow("Query", queryImage)
	print "query: %s" % (query)
 
	
	montageA = np.zeros((166 * 5, 400, 3), dtype = "uint8")
	montageB = np.zeros((166 * 5, 400, 3), dtype = "uint8")
 
	# loop over the top ten results
	for j in xrange(0, 10):
		# grab the result (we are using row-major order) and
		# load the result image
		(score, imageName) = results[j]
		path = args["dataset"] + "/%s" % (imageName)
		result = cv2.imread(path)
		print "\t%d. %s : %.3f" % (j + 1, imageName, score)
 
		# check to see if the first montage should be used
		if j < 5:
			montageA[j * 166:(j + 1) * 166, :] = result
 
		# otherwise, the second montage should be used
		else:
			montageB[(j - 5) * 166:((j - 5) + 1) * 166, :] = result
 
	# show the results
	cv2.imshow("Results 1-5", montageA)
	cv2.imshow("Results 6-10", montageB)
	cv2.waitKey(0)
    
