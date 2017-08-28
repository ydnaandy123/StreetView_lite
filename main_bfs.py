#!/usr/bin/python3
# ==============================================================
# demo for using bfs
# ==============================================================
import google_store

# Create PanoFetcher
zoom, radius = 4, 10
fileID = 'BBIG'
"""
# 1. use BFS
# parameter: fileId, gps, queryNum
"""
panoFetcher = google_store.PanoFetcher(zoom, radius)
panoFetcher.bfs_aug(fileID, (25.069134, 121.479111), 1)
