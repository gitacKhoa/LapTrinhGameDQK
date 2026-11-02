import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,".."))
from pxlib import *
from PIL import ImageOps
DIRS=["down","up","left","right"]; ANIMS=[("idle",2),("walk",4),("eat",3)]

# ======================= BIRDS 16x16 =======================
BIRD={
 "chicken":dict(body=("ST3","CR0","CR1","CR1"),head=("ST3","CR0","CR1","CR1"),wing="ST3",bill="SU2",leg="SU1",comb=True,oc="ST1"),
 "duck":dict(body=("WD1","WD2","WD3","WD3"),head=("GR1","GR2","GR3","GR3"),wing="WD1",bill="SU2",leg="SU1",comb=False,oc="WD0"),
}
def bird(kind,d,anim,f):
    c=BIRD[kind]; im=new(16,16)
    yb={"idle":[0,1][f%2] if anim=="idle" else 0,"walk":[1,0,1,0][f] if anim=="walk" else 0}.get(anim,1 if anim=="eat" else 0)
    hd=[1,3,2][f] if anim=="eat" else 0
    lp=[(0,0),(1,0),(0,0),(0,1)][f] if anim=="walk" else (0,0)   # lifted flags (left leg, right leg)
    sx=[0,1,0,-1][f] if anim=="walk" else 0
    if d=="left":
        for x,y in((13,6),(14,5),(14,6),(13,7),(14,7),(12,7)): put(im,x,y+yb,c["body"][1])
        put(im,14,5+yb,c["body"][2])
        blob(im,9,10+yb,5,4,c["body"]); line(im,8,9+yb,11,10+yb,c["wing"])
        hx,hy=(6 if hd<2 else 5),6+hd+yb
        rect(im,hx+1,hy+1,hx+3,9+yb,c["head"][1]) if hd>0 else None
        blob(im,hx,hy,2.6,2.5,c["head"],hi=False); put(im,hx-1,hy-1,"OL0")
        if c["comb"]:
            for x,y in((hx-1,hy-3),(hx,hy-3),(hx,hy-4)): put(im,x,y,"RD2")
            put(im,hx-2,hy+2,"RD2")
            put(im,hx-3,hy,c["bill"]); put(im,hx-4,hy,c["bill"])
        else:
            put(im,hx-3,hy+1,c["bill"]); put(im,hx-4,hy+1,c["bill"]); put(im,hx-3,hy,c["bill"]); put(im,hx+1,hy+2,"CR1")
        for lx,lift in((8-sx,lp[0]),(10+sx,lp[1])):
            put(im,lx,13-lift,c["leg"]) if not lift else None; put(im,lx,14-lift,c["leg"]); put(im,lx-1,14-lift,c["leg"])
            if not lift and True: put(im,lx,13,c["leg"])
    elif d=="down":
        blob(im,8,10+yb,4.4,4,c["body"]); put(im,4,10+yb,c["wing"]); put(im,4,11+yb,c["wing"]); put(im,12,10+yb,c["wing"]); put(im,12,11+yb,c["wing"])
        hy=5+hd+yb; blob(im,8,hy,2.8,2.5,c["head"],hi=False); put(im,7,hy,"OL0"); put(im,9,hy,"OL0")
        if c["comb"]:
            for x,y in((7,hy-3),(8,hy-3),(9,hy-3),(8,hy-4)): put(im,x,y,"RD2")
            put(im,8,hy+3,"RD2"); put(im,8,hy+2,c["bill"])
        else:
            rect(im,7,hy+2,9,hy+2,c["bill"]); put(im,8,hy+3,c["bill"])
        for lx,lift in((6,lp[0]),(10,lp[1])):
            put(im,lx,13-lift if lift else 13,c["leg"]); put(im,lx,14-lift,c["leg"]); put(im,lx-1,14-lift,c["leg"]); put(im,lx+1,14-lift,c["leg"])
    else:
        blob(im,8,10+yb,4.4,4,c["body"])
        rect(im,6,6+yb,10,8+yb,c["body"][1]); rect(im,7,5+yb,9,5+yb,c["body"][2]); rect(im,6,8+yb,10,8+yb,c["body"][0])
        hy=5+yb+(1 if hd else 0); blob(im,8,hy,2.4,2.1,c["head"],hi=False)
        if c["comb"]: put(im,8,hy-3,"RD2"); put(im,8,hy-2,"RD2")
        for lx,lift in((6,lp[0]),(10,lp[1])):
            put(im,lx,13-lift if lift else 13,c["leg"]); put(im,lx,14-lift,c["leg"]); put(im,lx-1,14-lift,c["leg"]); put(im,lx+1,14-lift,c["leg"])
    outline(im,c["oc"]); return im

# ======================= QUADRUPEDS 32x32 =======================
CF=("ST3","CR0","CR1","CR1")
QUAD={
 "cow":dict(body=CF,head=CF,legc=("ST3","CR0"),hoof="SO1",muz="RD3",ear="SO3",horns=True,wool=False,patch=True,tail=("CR0","SO2"),eye="OL0",oc="ST1"),
 "sheep":dict(body=CF,head=("OL0","ST0","ST1","ST2"),legc=("ST0","ST1"),hoof="OL0",muz="ST1",ear="ST0",horns=False,wool=True,patch=False,tail=("CR0","ST3"),eye="CR1",oc="ST1"),
}
PATCH={"ST3":"SO2","CR0":"SO3","CR1":"SO4"}
def patch(im,cx,cy,rx,ry):
    for y in range(im.height):
        for x in range(im.width):
            if ((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2<=1:
                p=im.getpixel((x,y))
                for k,v in PATCH.items():
                    if p==C[k]: put(im,x,y,v); break
def woolblob(im,ells,cx,cy):
    mask=set()
    for ex,ey,rx,ry in ells:
        for y in range(im.height):
            for x in range(im.width):
                if ((x+.5-ex)/rx)**2+((y+.5-ey)/ry)**2<=1: mask.add((x,y))
    for x,y in mask:
        s=((x-cx)/12)*.5+((y-cy)/9)*.85
        put(im,x,y,"ST3" if s>.42 else "CR1" if s<-.3 else "CR0")
    return mask
def quad(kind,d,anim,f):
    c=QUAD[kind]; im=new(32,32)
    A=[0,2,0,-2][f] if anim=="walk" else 0
    hd=[0,5,3][f] if anim=="eat" else 0
    yb=[0,1][f%2] if anim=="idle" else 0
    if d=="left":
        legs=[("bf",18+A,"far"),("ff",13-A,"far"),("bn",22-A,"near"),("fn",9+A,"near")]
        for role,x0,k in legs:
            v=(x0-({"bf":18,"ff":13,"bn":22,"fn":9}[role])); lift=-1 if (v>0 and anim=="walk") else 0
            col=c["legc"][0] if k=="far" else c["legc"][1]
            rect(im,x0,20,x0+2,27+lift,col); rect(im,x0,27+lift,x0+2,28+lift,c["hoof"])
        if c["wool"]: woolblob(im,[(16,16.5+yb,9,5.5),(10,15+yb,5.5,4.5),(22,15+yb,5.5,4.5),(16,13+yb,7,4),(12,19+yb,5,3.5),(21,19+yb,5,3.5)],15,15)
        else:
            blob(im,16,16.5+yb,10.5,6.5,c["body"],hi=False)
            if c["patch"]: patch(im,12,14+yb,3.6,3); patch(im,21,17+yb,4.2,3.3); patch(im,24,12+yb,2.8,2.4)
            rect(im,19,22+yb,21,23+yb,"RD3"); put(im,19,24+yb,"RD3"); put(im,21,24+yb,"RD3")
        rect(im,27,12+yb,28,18+yb,c["tail"][0]); rect(im,27,19+yb,28,21+yb,c["tail"][1])
        hy=15.5+hd+yb
        if hd: rect(im,8,15,12,int(hy)+3,c["body"][1] if not c["wool"] else "CR0")
        blob(im,7,hy,4.8,4.4,c["head"],hi=False)
        if c["patch"]: patch(im,8,hy-2,2.2,2)
        rect(im,2,int(hy)+1,5,int(hy)+4,c["muz"]); put(im,3,int(hy)+2,"RD1" if kind=="cow" else "OL0"); put(im,3,int(hy)+4,"SO1")
        put(im,7,hy-1.5,c["eye"]); put(im,7,hy-0.5,c["eye"]) if kind=="cow" else None
        rect(im,10,int(hy)-3,11,int(hy)-2,c["ear"])
        if c["horns"]: put(im,8,int(hy)-5,"CR0"); put(im,9,int(hy)-6,"CR0"); put(im,7,int(hy)-5,"CR0")
        else: rect(im,5,int(hy)-5,8,int(hy)-4,"CR0")
    elif d=="down":
        for x0,dy in((10,0),(19,0)):
            lift=-1 if (anim=="walk" and ((x0==10 and A>0) or (x0==19 and A<0))) else 0
            rect(im,x0,20,x0+3,27+lift,c["legc"][1]); rect(im,x0,27+lift,x0+3,28+lift,c["hoof"])
        if c["wool"]: woolblob(im,[(16,17+yb,9,7),(9,16+yb,5,5),(23,16+yb,5,5),(16,12+yb,7,5)],16,14)
        else:
            blob(im,16,17+yb,9.8,8,c["body"],hi=False)
            if c["patch"]: patch(im,10,18+yb,3.5,4); patch(im,23,15+yb,3.5,3)
        hy=13+hd+yb
        blob(im,16,hy,6.6,6.2,c["head"],hi=False)
        if c["patch"]: patch(im,19.5,hy-2,3,2.8)
        rect(im,13,int(hy)+3,18,int(hy)+6,c["muz"]); put(im,14,int(hy)+4,"RD1" if kind=="cow" else "OL0"); put(im,17,int(hy)+4,"RD1" if kind=="cow" else "OL0")
        put(im,12,hy-1,c["eye"]); put(im,19,hy-1,c["eye"])
        rect(im,8,int(hy)-2,9,int(hy)-1,c["ear"]); rect(im,22,int(hy)-2,23,int(hy)-1,c["ear"])
        if c["horns"]: [put(im,x,int(hy)-7+yy,"CR0") for x,yy in((11,0),(10,-1),(20,0),(21,-1))]
        else: blob(im,16,hy-6,5,3.2,("ST3","CR0","CR1","CR1"),hi=False)
    else:
        for x0 in(10,19):
            lift=-1 if (anim=="walk" and ((x0==10 and A>0) or (x0==19 and A<0))) else 0
            rect(im,x0,20,x0+3,27+lift,c["legc"][1]); rect(im,x0,27+lift,x0+3,28+lift,c["hoof"])
        if c["wool"]: woolblob(im,[(16,16+yb,10,7.5),(9,15+yb,5,5),(23,15+yb,5,5),(16,11+yb,7,4.5)],16,13)
        else:
            blob(im,16,16+yb,10,8.2,c["body"],hi=False)
            if c["patch"]: patch(im,11,15+yb,3.8,3.5); patch(im,21,19+yb,3.5,3)
        blob(im,16,8.5+yb,4.2,2.6,c["head"],hi=False)
        rect(im,10,8+yb,11,9+yb,c["ear"]); rect(im,21,8+yb,22,9+yb,c["ear"])
        if c["horns"]: put(im,12,6+yb,"CR0"); put(im,20,6+yb,"CR0")
        rect(im,15,13+yb,16,20+yb,c["tail"][0]); rect(im,15,21+yb,16,23+yb,c["tail"][1])
    outline(im,c["oc"]); return im

# ======================= BUILD =======================
def frames(kind):
    fn=bird if kind in BIRD else quad
    imgs=[];names=[]
    for an,n in ANIMS:
        for d in DIRS:
            fr=[ImageOps.mirror(fn(kind,"left",an,f)) if d=="right" else fn(kind,d,an,f) for f in range(n)]
            for c in range(4): imgs.append(fr[c] if c<n else None); names.append(f"animal_{kind}_{an}_{d}_{c:02d}" if c<n else "")
    return imgs,names
if __name__=="__main__":
    bad=[]; prev=[]
    for kind in list(BIRD)+list(QUAD):
        sz=16 if kind in BIRD else 32
        imgs,names=frames(kind); sh=sheet(imgs,4,sz,sz); p=f"{HERE}/Sheets/animal_{kind}_sheet.png"; sh.save(p)
        open(p.replace(".png",".names.txt"),"w").write(f"#cell={sz}x{sz} pivot=bottom\n"+"\n".join(names)+"\n")
        if offpalette(p): bad.append(kind)
        fn=bird if kind in BIRD else quad
        prev.append((kind,sz,[fn(kind,d,"idle",0) for d in("down","up","left")]+[ImageOps.mirror(fn(kind,"left","idle",0))]+[fn(kind,"left","walk",f) for f in range(4)]+[fn(kind,"left","eat",f) for f in range(3)]))
    W=max(len(i)*(s+4) for _,s,i in prev)+4; H=sum(s+4 for _,s,_ in prev)+4
    pv=new(W,H); rect(pv,0,0,W-1,H-1,"GR2"); y=2
    for k,s,ims in prev:
        for i,im in enumerate(ims): pv.alpha_composite(im,(2+i*(s+4),y))
        y+=s+4
    pv.resize((W*4,H*4),Image.NEAREST).save(f"{HERE}/Preview/animals_preview_x4.png"); pv.save(f"{HERE}/Preview/animals_preview.png")
    print("offpalette:",bad or "none")
