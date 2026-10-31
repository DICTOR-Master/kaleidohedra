import os,sys,subprocess
objs=set(open(sys.argv[1]).read().split())
SKIP={'node_modules','dist','dist-onesite','test-results','playwright-report','.venv','venv','__pycache__','.git','.vercel','.cache','.next','out-tmp'}
home=os.path.expanduser('~')
for d in sys.argv[2:]:
    root=os.path.join(home,d); paths=[]
    for dp,dn,fn in os.walk(root):
        dn[:]=[x for x in dn if x not in SKIP]
        for f in fn:
            p=os.path.join(dp,f)
            if os.path.isfile(p) and not os.path.islink(p): paths.append(p)
    if not paths: print(f'{d}\t0\t0\t0\t'); continue
    out=subprocess.run(['git','hash-object','--stdin-paths'],input='\n'.join(paths),capture_output=True,text=True).stdout.split()
    miss=[(p,os.path.getsize(p)) for p,h in zip(paths,out) if h not in objs]
    ms=sum(s for _,s in miss); miss.sort(key=lambda x:-x[1])
    ex=';'.join(os.path.relpath(p,root)+':'+str(s//1024)+'K' for p,s in miss[:6])
    print(f'{d}\t{len(paths)}\t{len(miss)}\t{ms//1024}\t{ex}',flush=True)
