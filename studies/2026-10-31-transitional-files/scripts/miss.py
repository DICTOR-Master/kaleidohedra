import os,sys,subprocess
objs=set(open(sys.argv[1]).read().split())
SKIP={'node_modules','dist','dist-onesite','test-results','playwright-report','.venv','venv','__pycache__','.git','.vercel','.cache','.next'}
d=os.path.expanduser('~/'+sys.argv[2]); paths=[]
for dp,dn,fn in os.walk(d):
    dn[:]=[x for x in dn if x not in SKIP]
    paths+= [os.path.join(dp,f) for f in fn if os.path.isfile(os.path.join(dp,f)) and not os.path.islink(os.path.join(dp,f))]
out=subprocess.run(['git','hash-object','--stdin-paths'],input='\n'.join(paths),capture_output=True,text=True).stdout.split()
lim=int(sys.argv[3]) if len(sys.argv)>3 else 40
miss=sorted([(os.path.getsize(p),os.path.relpath(p,d)) for p,h in zip(paths,out) if h not in objs],reverse=True)
for s,p in miss[:lim]: print(f'{s//1024}K\t{p}')
