#!/usr/bin/python3
# ==============================================================
# demo for using bfs
# ==============================================================
import google_store

# Create PanoFetcher
zoom, radius = 1, 10
fileID = 'NTHUDEMO'
"""
# 1. use BFS
# parameter: fileId, gps, queryNum
"""
if True:
    panoFetcher = google_store.PanoFetcher(zoom, radius)
    panoFetcher.bfs_aug(fileID, (24.7963071, 120.992373), 5)
