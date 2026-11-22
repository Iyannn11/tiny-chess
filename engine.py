# Tiny Chess R3: 0x88 alpha-beta engine. Fixed node budget, null move,
# LMR, check extensions, TT, killers, history, quiescence, repetition 0.
import json,os,random,sys,urllib.request,urllib.error
NN=50000
INF=100000
MATE=90000
V=(0,100,320,330,500,900,0)
PP=(0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0)
PN=(-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50)
PB=(-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20)
PR=(0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0)
PQ=(-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20)
PK=(-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20)
PE=(-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50)
PS=((),PP,PN,PB,PR,PQ,PK)
ON=(33,18,-14,-31,-33,-18,14,31)
OK=(1,-1,16,-16,15,17,-15,-17)
OB=(15,17,-15,-17)
OR=(1,-1,16,-16)
SQ=[f+r*16 for r in range(8) for f in range(8)]
PC={'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6,'p':9,'n':10,'b':11,'r':12,'q':13,'k':14}
_r=random.Random(987654321)
Z=[[_r.getrandbits(64) for _ in range(128)] for _ in range(15)]
ZS=_r.getrandbits(64)
ZC=[_r.getrandbits(64) for _ in range(16)]
ZE=[_r.getrandbits(64) for _ in range(8)]
B=[0]*128
side=0
cast=0
ep=-1
half=0
key=0
KS=[4,116]
NM=[0,0]
ST=[]
HS={}
TT={}
KL=[[0,0] for _ in range(64)]
HT=[0]*(2*128*128)
nodes=0
class Abort(Exception):pass
def atk(sq,by):
    if by==0:
        for d in (-15,-17):
            s=sq+d
            if not(s&0x88) and B[s]==1:return True
    else:
        for d in (15,17):
            s=sq+d
            if not(s&0x88) and B[s]==9:return True
    for d in ON:
        s=sq+d
        if not(s&0x88) and B[s]==(2|by):return True
    for d in OK:
        s=sq+d
        if not(s&0x88) and B[s]==(6|by):return True
    for d in OR:
        s=sq+d
        while not(s&0x88):
            p=B[s]
            if p:
                if p==(4|by) or p==(5|by):return True
                break
            s+=d
    for d in OB:
        s=sq+d
        while not(s&0x88):
            p=B[s]
            if p:
                if p==(3|by) or p==(5|by):return True
                break
            s+=d
    return False
def make(m):
    global side,cast,ep,half,key
    f=m&127;t=(m>>7)&127;pr=m>>14;p=B[f];typ=p&7;cap=B[t];csq=t
    if typ==1 and t==ep and cap==0:
        csq=t-16 if side==0 else t+16;cap=B[csq]
    ST.append((m,cap,csq,cast,ep,half,key))
    key^=Z[p][f]
    if cap:
        key^=Z[cap][csq]
        if (cap&7) not in (1,6):NM[(cap&8)>>3]-=V[cap&7]
    if ep>=0:key^=ZE[ep&7]
    key^=ZC[cast]
    B[f]=0
    if cap:B[csq]=0
    np=(pr|side) if pr else p
    if pr:NM[side>>3]+=V[pr]
    B[t]=np
    key^=Z[np][t]
    if typ==6:
        KS[side>>3]=t
        if t-f==2:
            rs,rt=f+3,f+1;r=B[rs];B[rs]=0;B[rt]=r;key^=Z[r][rs]^Z[r][rt]
        elif f-t==2:
            rs,rt=f-4,f-1;r=B[rs];B[rs]=0;B[rt]=r;key^=Z[r][rs]^Z[r][rt]
        cast&=~(3 if side==0 else 12)
    if f==0 or t==0:cast&=~2
    if f==7 or t==7:cast&=~1
    if f==112 or t==112:cast&=~8
    if f==119 or t==119:cast&=~4
    ep=-1
    if typ==1 and abs(t-f)==32:
        ep=(f+t)//2;key^=ZE[ep&7]
    half=0 if typ==1 or cap else half+1
    key^=ZC[cast]
    side^=8
    key^=ZS
def unmake():
    global side,cast,ep,half,key
    m,cap,csq,ocast,oep,ohalf,okey=ST.pop()
    f=m&127;t=(m>>7)&127;pr=m>>14
    side^=8
    p=B[t]
    if pr:
        NM[side>>3]-=V[pr];p=1|side
    if cap and (cap&7) not in (1,6):NM[(cap&8)>>3]+=V[cap&7]
    B[f]=p;B[t]=0
    if cap:B[csq]=cap
    if (p&7)==6:
        KS[side>>3]=f
        if abs(t-f)==2:
            if t-f==2:rs,rt=f+3,f+1
            else:rs,rt=f-4,f-1
            B[rs]=B[rt];B[rt]=0
    cast,ep,half,key=ocast,oep,ohalf,okey
def gen(caps=False):
    ms=[]
    for sq in SQ:
        p=B[sq]
        if not p or (p&8)!=side:continue
        typ=p&7
        if typ==1:
            d=16 if side==0 else -16;prank=7 if side==0 else 0;srank=1 if side==0 else 6
            t1=sq+d
            if not B[t1]:
                if (t1>>4)==prank:
                    for pr in (5,4,3,2):ms.append(sq|(t1<<7)|(pr<<14))
                elif not caps:
                    ms.append(sq|(t1<<7))
                    if (sq>>4)==srank and not B[sq+2*d]:ms.append(sq|((sq+2*d)<<7))
            for t2 in (sq+d-1,sq+d+1):
                if t2&0x88:continue
                c=B[t2]
                if c and (c&8)!=side:
                    if (t2>>4)==prank:
                        for pr in (5,4,3,2):ms.append(sq|(t2<<7)|(pr<<14))
                    else:ms.append(sq|(t2<<7))
                elif t2==ep:ms.append(sq|(t2<<7))
        elif typ==2:
            for d in ON:
                t2=sq+d
                if t2&0x88:continue
                c=B[t2]
                if c:
                    if (c&8)!=side:ms.append(sq|(t2<<7))
                elif not caps:ms.append(sq|(t2<<7))
        elif typ==6:
            for d in OK:
                t2=sq+d
                if t2&0x88:continue
                c=B[t2]
                if c:
                    if (c&8)!=side:ms.append(sq|(t2<<7))
                elif not caps:ms.append(sq|(t2<<7))
            if not caps:
                if side==0:
                    if cast&1 and not B[5] and not B[6] and B[7]==4 and not atk(4,8) and not atk(5,8) and not atk(6,8):ms.append(4|(6<<7))
                    if cast&2 and not B[1] and not B[2] and not B[3] and B[0]==4 and not atk(4,8) and not atk(3,8) and not atk(2,8):ms.append(4|(2<<7))
                else:
                    if cast&4 and not B[117] and not B[118] and B[119]==12 and not atk(116,0) and not atk(117,0) and not atk(118,0):ms.append(116|(118<<7))
                    if cast&8 and not B[113] and not B[114] and not B[115] and B[112]==12 and not atk(116,0) and not atk(115,0) and not atk(114,0):ms.append(116|(114<<7))
        else:
            offs=OB if typ==3 else (OR if typ==4 else OB+OR)
            for d in offs:
                t2=sq+d
                while not(t2&0x88):
                    c=B[t2]
                    if c:
                        if (c&8)!=side:ms.append(sq|(t2<<7))
                        break
                    if not caps:ms.append(sq|(t2<<7))
                    t2+=d
    return ms
def ev():
    s=0;wq=bq=wb=bb=0
    for sq in SQ:
        p=B[sq]
        if not p:continue
        t=p&7
        if p&8:
            s-=V[t]+PS[t][(sq&7)+(sq>>4)*8]
            if t==5:bq=1
            elif t==3:bb+=1
        else:
            s+=V[t]+PS[t][(sq&7)+(7-(sq>>4))*8]
            if t==5:wq=1
            elif t==3:wb+=1
    if wb>=2:s+=30
    if bb>=2:s-=30
    if not wq and not bq:
        wk=KS[0];bk=KS[1]
        wi=(wk&7)+(7-(wk>>4))*8;bi=(bk&7)+(bk>>4)*8
        s+=PE[wi]-PK[wi]
        s-=PE[bi]-PK[bi]
    return s if side==0 else -s
def srt(moves,ttm,ply):
    def sc(m):
        if m==ttm:return 1<<25
        t=(m>>7)&127;c=B[t]
        if c:return 10000+V[c&7]*16-V[(B[m&127])&7]
        pr=m>>14
        if pr:return 9500+V[pr]
        if m==KL[ply][0]:return 9000
        if m==KL[ply][1]:return 8000
        return HT[(side>>3)*16384+(m&127)*128+t]
    moves.sort(key=sc,reverse=True)
def rep():
    if key in HS:return True
    for u in ST:
        if u[6]==key:return True
    return False
def qs(alpha,beta,ply):
    global nodes
    nodes+=1
    if nodes>=NN:raise Abort
    if half>=100 or rep():return 0
    chk=atk(KS[side>>3],side^8)
    if not chk:
        stand=ev()
        if stand>=beta:return beta
        if stand>alpha:alpha=stand
    moves=gen() if chk else gen(True)
    srt(moves,0,ply)
    legal=0
    for m in moves:
        make(m)
        if atk(KS[(side^8)>>3],side):
            unmake();continue
        legal+=1
        s=-qs(-beta,-alpha,ply+1)
        unmake()
        if s>=beta:return beta
        if s>alpha:alpha=s
    if chk and not legal:return -MATE+ply
    return alpha
def search(alpha,beta,depth,ply):
    global nodes,side,ep,half,key
    nodes+=1
    if nodes>=NN:raise Abort
    if half>=100 or rep():return 0
    e=TT.get(key)
    ttm=e[3] if e else 0
    if e and e[0]>=depth:
        s,fl=e[1],e[2]
        if fl==0:return s
        if fl==1 and s>=beta:return s
        if fl==2 and s<=alpha:return s
    if depth<=0:return qs(alpha,beta,ply)
    chk=atk(KS[side>>3],side^8)
    if chk:depth+=1
    if depth>=3 and not chk and NM[side>>3]>0 and beta<MATE-100 and beta>-MATE+100:
        okey,oep,ohalf=key,ep,half
        key^=ZS
        if ep>=0:key^=ZE[ep&7]
        ep=-1;side^=8;half+=1
        s=-search(-beta,-beta+1,depth-3,ply+1)
        side^=8;ep,half,key=oep,ohalf,okey
        if s>=beta:return beta
    moves=gen()
    srt(moves,ttm,ply)
    best=-INF;bestm=0;legal=0;oa=alpha
    for i,m in enumerate(moves):
        t=(m>>7)&127;cap=B[t]!=0 or t==ep
        make(m)
        if atk(KS[(side^8)>>3],side):
            unmake();continue
        legal+=1
        if i and depth>=3 and not cap and not(m>>14) and not chk:
            s=-search(-alpha-1,-alpha,depth-2,ply+1)
            if s>alpha:s=-search(-beta,-alpha,depth-1,ply+1)
        else:
            s=-search(-beta,-alpha,depth-1,ply+1)
        unmake()
        if s>best:best=s;bestm=m
        if s>alpha:alpha=s
        if alpha>=beta:
            if not cap:
                KL[ply][1]=KL[ply][0];KL[ply][0]=m
                HT[(side>>3)*16384+(m&127)*128+t]+=depth*depth
            break
    if not legal:return -MATE+ply if chk else 0
    if best>=beta:fl=1
    elif best<=oa:fl=2
    else:fl=0
    if len(TT)>200000:TT.clear()
    TT[key]=(depth,best,fl,bestm)
    return best
def roots(depth):
    moves=gen()
    e=TT.get(key)
    srt(moves,e[3] if e else 0,0)
    best=-INF;bestm=0;alpha=-INF
    for i,m in enumerate(moves):
        make(m)
        if atk(KS[(side^8)>>3],side):
            unmake();continue
        if i==0:s=-search(-INF,-alpha,depth-1,1)
        else:
            s=-search(-alpha-1,-alpha,depth-1,1)
            if s>alpha:s=-search(-INF,-alpha,depth-1,1)
        unmake()
        if s>best:best=s;bestm=m
        if s>alpha:alpha=s
    return bestm,best
def think(legal):
    global nodes
    nodes=0;bestm=0
    for depth in range(1,40):
        try:
            m,s=roots(depth)
            if m:bestm=m
        except Abort:break
    return bestm
def pf(fen):
    global B,side,cast,ep,half,key,KS,NM
    B=[0]*128;KS=[4,116];NM=[0,0]
    parts=fen.split();rows=parts[0].split('/')
    for r,row in enumerate(rows):
        f=0
        for ch in row:
            if ch.isdigit():f+=int(ch)
            else:
                sq=f+(7-r)*16;B[sq]=PC[ch]
                if ch=='K':KS[0]=sq
                elif ch=='k':KS[1]=sq
                f+=1
    side=0 if parts[1]=='w' else 8
    cast=0
    if parts[2]!='-':
        for ch in parts[2]:cast|={'K':1,'Q':2,'k':4,'q':8}[ch]
    ep=-1
    if parts[3]!='-':ep='abcdefgh'.index(parts[3][0])+(int(parts[3][1])-1)*16
    half=int(parts[4]) if len(parts)>4 else 0
    key=0
    for sq in SQ:
        p=B[sq]
        if p:
            key^=Z[p][sq]
            if (p&7) not in (1,6):NM[(p&8)>>3]+=V[p&7]
    if side:key^=ZS
    key^=ZC[cast]
    if ep>=0:key^=ZE[ep&7]
def utom(u):
    f='abcdefgh'.index(u[0])+(int(u[1])-1)*16
    t='abcdefgh'.index(u[2])+(int(u[3])-1)*16
    pr=0
    if len(u)==5:pr={'n':2,'b':3,'r':4,'q':5}[u[4]]
    return f|(t<<7)|(pr<<14)
def mtou(m):
    f=m&127;t=(m>>7)&127;pr=m>>14
    s='abcdefgh'[f&7]+str((f>>4)+1)+'abcdefgh'[t&7]+str((t>>4)+1)
    if pr:s+='nbrq'[pr-2]
    return s
def ghist(start_fen,moves):
    global HS
    pf(start_fen)
    HS={key:1}
    for u in moves:
        make(utom(u))
        HS[key]=HS.get(key,0)+1
    ST.clear()
    return HS
def fb(legal):
    best=None;bests=-INF
    for u in legal:
        make(utom(u))
        s=-ev()
        unmake()
        if s>bests:bests=s;best=u
    return best or legal[0]
def post(path,body):
    req=urllib.request.Request(ENV+path,data=json.dumps(body).encode(),headers={'content-type':'application/json'})
    try:
        with urllib.request.urlopen(req) as r:return json.load(r)
    except urllib.error.HTTPError as e:sys.exit(f'{path}: HTTP {e.code}')
ENV=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
if __name__=='__main__':
    while True:
        g=post('/game',{})
        if g['status']=='done':break
        ghist(g['start_fen'],g['moves'])
        pf(g['fen'])
        while g['status']=='your_move':
            ghist(g['start_fen'],g['moves'])
            pf(g['fen'])
            m=think(g['legal_moves'])
            u=mtou(m) if m else None
            if not u or u not in g['legal_moves']:u=fb(g['legal_moves'])
            g=post('/move',{'game':g['game'],'move':u})
        print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
