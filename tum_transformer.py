#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 17:33:03 2025

@author: risalinux
"""

import sys

path=sys.argv[1]
import numpy as np

matrix=np.eye(3)

for x in range(9):
    matrix[int((x-x%3)/3),x%3]=sys.argv[2+x]
from scipy.spatial.transform import Rotation as R
transform=R.from_matrix(matrix)
quaternion=transform.as_quat()
newfile=[]
with open(path) as f:
    for row in f:
        row=row.split(' ')
        row[1:4]=transform.as_matrix()@np.float64(row[1:4])
        row[4:]=(transform*R.from_quat(row[4:])).as_quat()
        for x in range(len(row)):
            row[x]=str(row[x])
        newfile.append(' '.join(row)+'\n')
with open(path,'w') as f:
    f.writelines(newfile)
    
    