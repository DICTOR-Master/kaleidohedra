import numpy as np, sys
A=np.load('/home/dicto/eye-data/gw05-s600.npy',mmap_mode='r'); B=np.load('/home/dicto/eye-data/gw05-s600-blk.npy',mmap_mode='r')
a=float(A[40:760:4,760:1460:8,590:1676:8].mean()); b=float(B[::4,::8,::8].mean()); print('shape',A.shape,'block mean full/blk',a,b)
sys.exit(0 if A.shape==(1004,2264,1676) and abs(a-b)<0.01*b else 1)
