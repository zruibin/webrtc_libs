#! /usr/bin/env python
# -*- coding: utf-8 -*- 
#
# main.py
#
# Created by Ruibin.Chow on 2022/12/04.
# Copyright (c) 2022年 Ruibin.Chow All rights reserved.
# 

"""

"""

import os, re, json, sys, platform, fnmatch
import datetime, shutil
import tarfile, gzip
from pathlib import Path

libsDirName = "libs"
partsDirName = "parts"
homeDir = ""
libsDir = ""
partsDir = ""

partsNmae = "manifest"
libName = "libwebrtc.a.zip"

# github限制单个大文件上传的大小为100M
fileSize = 1024*1000*40 # 每个文件最多40MB

def getAllFileInDirectory(DIR, beyoundDir=''):
    """返回指定目录下所有文件的集合，beyoundDir的目录不包含"""
    array = []
    # print(DIR+beyoundDir)
    for root, dirs, files in os.walk(DIR):
        if len(beyoundDir) != 0 and os.path.exists(DIR+beyoundDir):
            if beyoundDir not in dirs:
                continue
        for name in files:
            if name != ".DS_Store":
                path = os.path.join(root,name)
                array.append(path)
    return array

def getDirtectory(DIR, beyoundDir=''):
    array = []
    for root, dirs, files in os.walk(DIR):
        if len(beyoundDir) != 0 and os.path.exists(DIR+beyoundDir):
            if beyoundDir not in dirs:
                continue
        array = dirs
        return array


def runSplit(filePath, outputdir):
    print("runSplit: " + filePath)
    from filesplit.split import Split
    split = Split(filePath, outputdir)
    split.bysize(size = fileSize) 
    pass

def runMerge(fileDir, outputdir):
    path = os.path.join(fileDir, partsNmae)
    if not os.path.exists(path):
        return
    print("runMerge: " + fileDir)
    print("outputdir: " + outputdir)
    print("libName: " + libName)
    from filesplit.merge import Merge
    merge = Merge(inputdir = fileDir, outputdir=outputdir, outputfilename = libName)
    merge.merge()
    pass

def moveLibs(dirs):
    for directory in dirs:
        filePath = os.path.join(libsDir, directory, libName)
        if not os.path.exists(filePath):
            continue
        p = Path(filePath)
        newFilePath = p.stem + "." + directory + p.suffix
        despath = os.path.join(homeDir, newFilePath)
        print(filePath)
        print(despath)
        shutil.move(filePath, despath)
    pass


def main():
    global homeDir, libsDir, partsDir
    homeDir = sys.path[0]
    libsDir = os.path.join(homeDir, libsDirName)
    partsDir = os.path.join(homeDir, partsDirName)

    # libs = getDirtectory(libsDir)
    # splitLibs = getAllFileInDirectory(libsDir)
    # print(splitLibs)
    # for splitLib in splitLibs:
    #     p = Path(splitLib)
    #     runSplit(splitLib, os.path.join(partsDir, p.parts[-2]))
    
    dirs = getDirtectory(partsDir)
    print(dirs)
    mergeDirs = []
    for directory in dirs:
        path = os.path.join(libsDir, directory)
        if not os.path.exists(path):
            os.makedirs(path)
        mergeDirs.append(os.path.join(partsDir, directory))
    # print(mergeDirs)

    for directory in mergeDirs:
        p = Path(directory)
        runMerge(directory, os.path.join(libsDir, p.parts[-1]))
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "move":
            moveLibs(dirs)
    pass

if __name__ == '__main__':
    main()
    pass
