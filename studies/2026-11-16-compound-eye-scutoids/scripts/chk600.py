import numpy as np
A=np.load('/home/dicto/eye-data/gw05-s600-blk.npy',mmap_mode='r'); print('shape',A.shape)
B=np.load('/home/dicto/eye-data/gw05-s2400.npy',mmap_mode='r')
a=float(A[::4,::8,::8].mean()); b=float(B[40:760:4,760//4:1460//4:2,590//4:1676//4:2].mean())
print('mean600',a,'mean2400',b); import sys; sys.exit(0 if A.shape==(720,700,1086) and a>0 and abs(a-b)<0.1*b else 1)
