import os,sys,subprocess,json,collections,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from regen import *
from _lib import root_letters, gold_roots
os.chdir("/workspace/geez-review/a2base_1022/ds")
k0=counts(); print("BEFORE",summary(k0))
D="(22 Oct 2026)"
HELD=re.compile(r'(genesis (1|5)|exodus 20|psalmus 1(09|10)|matth?aeus 1|matthew 1|lucas 1|luke 1):\d',re.I)
KX={'id','source','book','page','source_ref','evidence','also_in','status','status_reason','split'}
key=lambda x:json.dumps({a:b for a,b in x.items() if a not in KX},sort_keys=True,ensure_ascii=False)
T="u028429 u032522 u040312 u040313 u021796 u037623 u037624 u021827 u022584 u023914 u028428 u032724 u037655 u043381 u021719".split()
KEEP={"u012044","u042121","u012960","u021805","u029869"}; assert not KEEP&set(T)
PM="data/unified/geez_morphology_rows.jsonl"; PR="data/unified/geez_morphology_rows_reviewed.jsonl"
Ml=load(PM); Rl=load(PR); M={r["id"]:r for r in Ml}; R={r["id"]:r for r in Rl}
OLD={r["id"]:r for r in map(json.loads,subprocess.check_output(["git","show","03e0164:"+PR],text=True).splitlines())}
FLD=("root","word_class","number","gender","split")
gr=gold_roots(Ml); res={}
for i in T:
    a=M[i]; o=OLD[i]; assert a["source"]!="gold" and a["status"]=="CHECK" and o["status"]==""
    cand=dict(a,**{k:o[k] for k in FLD})
    w=[]; ok,ln=root_letters(cand["form"],cand["root"])
    if not ok: w.append("root letters: "+ln)
    if gr[cand["form"]] and cand["root"] not in gr[cand["form"]]: w.append("gold root "+"/".join(sorted(gr[cand["form"]])))
    sp={x["split"] for x in Ml if x["root"]==cand["root"] and x["status"]!="EXCLUDED" and x["id"]!=i}
    if len(sp)>1 or (sp and cand["split"] not in sp): w.append(f"root split {sorted(sp)} vs {cand['split']}")
    d=[x["id"] for x in Ml if x["status"]=="" and x["id"]!=i and key(x)==key(cand)]
    if d: w.append("repeats "+",".join(d))
    if HELD.search(a["evidence"] or ""): w.append("held-out chapter")
    res[i]=(cand["form"],cand["root"],cand["split"],w,ln)
    if w: continue
    for F in (M,R):
        x=F[i]
        for k in FLD: x[k]=o[k]
        x["status"]="";x["status_reason"]=""
        x["evidence"]+=f"; passes the letter check with matching series (ሠ/ሰ, ጸ/ፀ, ሀ/ሐ/ኀ, አ/ዐ; {ln}); review fields restored, loads {D}" if i!="u021719" else f"; the gold row u001147 is EXCLUDED, so it is no conflict; review fields restored, loads {D}"
for i,v in res.items(): print(i,*v)
wr(PM,Ml); wr(PR,Rl)
files={}
for i in T:
    r=M[i]; ref=r["source_ref"] or ""
    if r["status"] or not ref.startswith("data/books/"): continue
    f,_,n=ref.rpartition(":"); L=files.setdefault(f,[json.loads(l) for l in open(f,encoding="utf-8")])
    b=L[int(n)-1]; assert b["form"]==r["form"]; b["root"]=r["root"]
    if "split" in b: b["split"]=r["split"]
for f,L in files.items(): wr(f,L)
subprocess.run([sys.executable,"scripts/build_clitic_forms.py"],check=True)
k=counts(); docs(k)
n=sum(1 for v in res.values() if not v[3])
open("docs/CHANGES.md","a").write(f"- Letter check: ሠ/ሰ, ጸ/ፀ, ሀ/ሐ/ኀ and አ/ዐ count as one series (Language). Roots keep Merho's spelling. EXCLUDED gold rows are no gold conflict. {n} rows held back by c12 now load in both files (e.g. ሰኑይ, ሥልጣን, ፆም, ነፍስ u021719).\n")
sums(); print("AFTER",summary(k),k["gp"])
