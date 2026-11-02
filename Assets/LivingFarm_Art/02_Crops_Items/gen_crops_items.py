import os, sys
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=HERE
RAMPS = {
"OL":["1b1b2a"],"GR":["2d5a3a","3f7d45","5ea34f","8cc65a","c4e48a"],
"SO":["2c1d1a","3a2620","5b3b2c","7c553b","a67c52"],"WD":["5a3a22","8a5a33","b7814a","dba76a"],
"WA":["1d3f6e","2f6db3","4d9be0","8ecff0","e3f6fb"],"ST":["3d4150","636a7a","8d94a3","b9bfc9","e1e4ea"],
"SU":["b85c1e","e8872c","f7b844","fbe07a","fff3b8"],"RD":["7a1f2b","b5333a","e2574c","f58f7c"],
"SK":["8a5a44","c98b66","f0b894","ffd9b8"],"AC":["5a3a6b","8a5fa0","e78aa8"],"CR":["f4ecd8","fffaf0"]}
C={f"{k}{i}":tuple(int(h[j:j+2],16) for j in (0,2,4))+(255,) for k,l in RAMPS.items() for i,h in enumerate(l)}
PAL=set(C.values())
def new(w,h): return Image.new("RGBA",(w,h),(0,0,0,0))
def put(im,x,y,c):
    x=int(x); y=int(y)
    if 0<=x<im.width and 0<=y<im.height: im.putpixel((x,y),C[c] if isinstance(c,str) else c)
def rect(im,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): put(im,x,y,c)
def line(im,x0,y0,x1,y1,c):
    dx,dy=abs(x1-x0),-abs(y1-y0); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1; e=dx+dy
    while True:
        put(im,x0,y0,c)
        if (x0,y0)==(x1,y1): break
        e2=2*e
        if e2>=dy: e+=dy; x0+=sx
        if e2<=dx: e+=dx; y0+=sy
def outline(im,c):
    src=im.copy()
    for y in range(im.height):
        for x in range(im.width):
            if src.getpixel((x,y))[3]==0:
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<im.width and 0<=ny<im.height and src.getpixel((nx,ny))[3]>0: put(im,x,y,c); break
def blob(im,cx,cy,rx,ry,cols,hi=True):
    d,m,l,h=cols
    for y in range(im.height):
        for x in range(im.width):
            nx=(x+.5-cx)/rx; ny=(y+.5-cy)/ry
            if nx*nx+ny*ny<=1:
                s=nx*.6+ny*.8; put(im,x,y,d if s>.35 else (l if s<-.45 else m))
    if hi: put(im,cx-rx*.45,cy-ry*.5,h); put(im,cx-rx*.25,cy-ry*.62,h)
def layer(im,fn,oc=None):
    l=new(im.width,im.height); fn(l)
    if oc: outline(l,oc)
    im.alpha_composite(l)
G4=("GR1","GR2","GR3","GR4")

# ================= CROPS (cell 16x32, plant base y=27, bottom 16 rows = soil tile) =================
B=27
def mound(im,seed=None,small=False):
    if not small:
        rect(im,7,25,8,25,"SO4"); rect(im,6,26,9,26,"SO4"); rect(im,5,27,10,27,"SO3"); rect(im,6,28,9,28,"SO1")
        if seed: put(im,8,26,seed); put(im,7,26,"SO3")
    else: rect(im,6,27,9,27,"SO3"); put(im,6,27,"SO4")
def blade(im,x,y,dx,n,c1="GR2",c2="GR3"):
    for i in range(n):
        px=x+dx*i; py=y-(i+1)//2; put(im,px,py,c1)
        if 0<i<n-1: put(im,px,py-1,c2)
def sprout(im):
    mound(im,small=True); put(im,8,26,"GR2"); put(im,8,25,"GR2"); put(im,7,24,"GR3"); put(im,9,24,"GR3"); put(im,6,23,"GR4"); put(im,10,23,"GR4")
def wheat(s):
    im=new(16,32)
    if s==0: mound(im,"SU2"); return im
    if s==1: sprout(im); return im
    xs=[[5,8,11],[4,6,8,10,12],[3,5,7,9,11,13]][s-2]; hs=[[6,8,6],[10,12,11,12,10],[12,14,13,14,13,12]][s-2]
    for x,h in zip(xs,hs):
        for i in range(h): put(im,x,B-i,["GR2","GR3","SU3"][s-2] if not(s==4 and i<4) else "SU2")
        t=B-h
        if s==2: put(im,x,t,"GR3")
        if s==3: put(im,x,t,"SU2"); put(im,x,t-1,"SU2"); put(im,x+1,t,"GR3")
        if s==4:
            for k in range(3): put(im,x,t-k,"SU4" if k<2 else "SU3")
            put(im,x-1,t-1,"SU3"); put(im,x+1,t-2,"SU3"); put(im,x-1,t,"SU2")
    return im
def carrot(s):
    im=new(16,32)
    if s==0: mound(im,"SU1"); return im
    if s==1: sprout(im); return im
    fr=[[(6,5),(8,7),(10,5)],[(5,6),(7,9),(9,9),(11,6)],[(4,6),(6,9),(8,11),(10,9),(12,6)]][s-2]
    for x,h in fr:
        for i in range(h):
            put(im,x,B-i,"GR2" if i<h-2 else "GR3")
            if i in(2,4) and i<h-2: put(im,x-1,B-i,"GR3"); put(im,x+1,B-i-1,"GR3")
        put(im,x,B-h,"GR4")
    if s==4:
        rect(im,6,B-1,9,B,"SU1"); put(im,7,B-1,"SU2"); put(im,6,B-1,"SU2"); rect(im,7,B+1,8,B+1,"SU0"); put(im,9,B,"SU0")
    return im
def potato(s):
    im=new(16,32)
    if s==0: mound(im,"WD3"); return im
    if s==1: sprout(im); return im
    if s==2: blob(im,8,B-4,4,3.5,G4)
    else:
        blob(im,8,B-6,6,5.5,G4); blob(im,4,B-3,3,3,G4); blob(im,12,B-3,3,3,G4)
    if s==4:
        for x,y in((6,B-9),(10,B-8),(8,B-11)): put(im,x,y,"CR1"); put(im,x+1,y,"CR1"); put(im,x,y+1,"SU2")
        for cx in(4,11): blob(im,cx,B+1.5,2.6,1.9,("SO3","SO4","WD3","WD3"),hi=False)
    return im
def tomato_fruit(im,x,y,red):
    if red:
        rect(im,x,y,x+2,y+2,"RD2"); put(im,x,y,"RD3"); put(im,x+1,y+2,"RD1"); put(im,x+2,y+1,"RD1"); put(im,x+2,y+2,"RD1")
    else:
        rect(im,x,y,x+2,y+2,"GR3"); put(im,x,y,"GR4"); put(im,x+2,y+2,"GR2")
    put(im,x+1,y-1,"GR1")
def tomato(s):
    im=new(16,32)
    if s==0: mound(im,"RD2"); return im
    if s==1: sprout(im); return im
    h=[10,16,18][s-2]
    for i in range(h): put(im,8,B-i,"WD2")
    put(im,7,B-h,"WD3")
    lv=[[(5,B-5),(11,B-8)],[(5,B-5),(11,B-8),(5,B-11),(11,B-14)],[(5,B-5),(11,B-8),(5,B-11),(11,B-15)]][s-2]
    for x,y in lv: blob(im,x,y,3.4,2.7,G4)
    if s==3: tomato_fruit(im,9,B-6,False); tomato_fruit(im,3,B-12,False)
    if s==4:
        for x,y in((9,B-5),(2,B-10),(10,B-11),(4,B-3)): tomato_fruit(im,x,y,True)
    return im
def berry(im,x,y):
    rect(im,x,y,x+2,y+1,"RD2"); put(im,x+1,y+2,"RD1"); put(im,x,y,"RD3"); put(im,x+2,y+1,"RD1"); put(im,x+1,y-1,"GR3")
def strawberry(s):
    im=new(16,32)
    if s==0: mound(im,"RD3"); return im
    if s==1: sprout(im); return im
    if s==2: blob(im,8,B-2,4.5,2.5,G4)
    else:
        blob(im,5,B-3,3.8,2.8,G4); blob(im,11,B-3,3.8,2.8,G4); blob(im,8,B-5,3.8,3,G4)
    if s==3:
        for x,y in((5,B-7),(11,B-6),(8,B-9)): put(im,x,y,"CR1"); put(im,x+1,y,"CR1"); put(im,x,y+1,"SU2")
    if s==4:
        for x,y in((3,B-2),(10,B-2),(6,B-5),(11,B-5)): berry(im,x,y)
    return im
def pumpkin(s):
    im=new(16,32)
    if s==0: mound(im,"SU0"); return im
    if s==1: sprout(im); return im
    for x,y,rx,ry in((4,B-3,4,2.6),(12,B-3,4,2.6),(8,B-6,3.8,3.2)): blob(im,x,y,rx,ry,G4)
    line(im,6,B-1,10,B-1,"GR1")
    if s==3: layer(im,lambda l:blob(l,8,B-1.5,3,2.4,("GR1","GR2","GR3","GR4")),"GR0")
    if s==4:
        def p(l):
            blob(l,8,B-3,6,4.6,("SU0","SU1","SU2","SU3"))
            for x,y0,y1 in((5,B-5,B-1),(8,B-7,B+1),(11,B-5,B-1)): 
                for y in range(y0,y1+1): put(l,x,y,"SU0")
            put(l,8,B-8,"GR1"); put(l,8,B-9,"GR1"); put(l,9,B-9,"GR2")
        layer(im,p,"SU0")
    return im
def corn(s):
    im=new(16,32)
    if s==0: mound(im,"SU4"); return im
    if s==1: sprout(im); return im
    h=[12,20,26][s-2]
    for i in range(h): put(im,7,B-i,"GR3"); put(im,8,B-i,"GR2")
    steps=[[3,6],[3,7,11,15],[3,8,13,18,22]][s-2]
    for k,i in enumerate(steps):
        blade(im,9,B-i,1,5); blade(im,6,B-i-2,-1,5)
    if s>=3:
        for k in range(3): put(im,7,B-h-1-k,"SU2") if k<2 else None
        put(im,6,B-h,"SU2"); put(im,9,B-h,"SU2")
    if s==4:
        for x,y in((9,B-12),(5,B-17)):
            rect(im,x,y,x+1,y+3,"SU3"); put(im,x+1,y+1,"SU2"); put(im,x+1,y+3,"SU2"); put(im,x,y,"SU4")
            rect(im,x-(1 if x>7 else -2),y+3,x+(2 if x>7 else 1),y+4,"GR3")
    return im
CROPS={"wheat":wheat,"carrot":carrot,"potato":potato,"tomato":tomato,"strawberry":strawberry,"pumpkin":pumpkin,"corn":corn}
STAGES=["seed","sprout","growing","mature","ready"]
WILT={"GR0":"SO0","GR1":"WD0","GR2":"WD1","GR3":"SO4","GR4":"WD3"}
def wilted(im):
    w=im.copy(); m={C[k]:C[v] for k,v in WILT.items()}
    for y in range(w.height):
        for x in range(w.width):
            p=w.getpixel((x,y))
            if p in m: w.putpixel((x,y),m[p])
    return w
crop_imgs=[]; crop_names=[]
for cn,fn in CROPS.items():
    st=[fn(i) for i in range(5)]+[wilted(fn(3))]
    for n,im in zip(STAGES+["wilted"],st): crop_imgs.append(im); crop_names.append(f"crop_{cn}_{n}")
def sheet(imgs,cols,cw,ch):
    rows=(len(imgs)+cols-1)//cols; sh=new(cols*cw,rows*ch)
    for i,im in enumerate(imgs): sh.paste(im,((i%cols)*cw,(i//cols)*ch))
    return sh
cs=sheet(crop_imgs,6,16,32); cs.save(f"{OUT}/Crops/crops_sheet.png")
open(f"{OUT}/Crops/crops_sheet.names.txt","w").write("#cell=16x32 pivot=bottom\n"+"\n".join(crop_names)+"\n")
for n,im in zip(crop_names,crop_imgs): im.save(f"{OUT}/Crops/{n}.png")

# ================= ITEMS 16x16 =================
def item(fn,oc):
    im=new(16,16); fn(im)
    if oc: outline(im,oc)
    return im
def handle(im): line(im,3,13,11,5,"WD2"); line(im,3,12,10,5,"WD3")
def hoe(im):
    handle(im); line(im,9,3,13,7,"ST3"); line(im,9,4,12,7,"ST2"); put(im,9,3,"ST4"); put(im,10,4,"ST4"); put(im,13,7,"ST1")
def axe(im):
    handle(im)
    for y,x1 in((2,11),(3,12),(4,13),(5,13),(6,12),(7,11)): rect(im,9,y,x1,y,"ST3"); put(im,x1,y,"ST4")
    for y in(6,7): rect(im,9,y,10,y,"ST2")
    put(im,9,2,"ST4")
def hammer(im):
    handle(im); rect(im,8,2,14,5,"ST3"); rect(im,8,2,14,2,"ST4"); rect(im,8,5,14,5,"ST1"); put(im,9,3,"ST4")
def pickaxe(im):
    handle(im)
    for x,y in((4,6),(5,5),(6,4),(7,3),(8,3),(9,3),(10,3),(11,4),(12,5),(13,7)): put(im,x,y,"ST3")
    for x,y in((6,5),(7,4),(8,4),(9,4),(10,4),(11,5)): put(im,x,y,"ST2")
    put(im,8,3,"ST4"); put(im,9,3,"ST4")
def can(im):
    rect(im,3,7,10,12,"WA2"); rect(im,3,7,4,12,"WA3"); rect(im,9,7,10,12,"WA1"); rect(im,3,12,10,12,"WA1"); rect(im,3,7,10,7,"WA3")
    rect(im,4,6,9,6,"ST2"); line(im,11,10,13,6,"ST2"); line(im,11,11,13,7,"ST3"); rect(im,13,5,14,5,"ST1")
    for y in(8,9,10): put(im,2,y,"ST2")
    put(im,1,8,"ST2"); put(im,1,9,"ST2"); put(im,1,10,"ST2")
def packet(col):
    def f(im):
        rect(im,4,3,11,13,"CR0"); rect(im,4,3,11,5,col); rect(im,11,6,11,13,"SK3"); rect(im,4,3,11,3,"CR1")
        for x,y in((6,8),(9,8),(7,10),(9,11),(6,12)): put(im,x,y,col)
        put(im,8,7,"GR2")
    return item(f,"WD0")
def carrot_i(im):
    for y in range(5,14):
        w=max(0,3-(y-5)//3); cx=8-(y-5)//5
        rect(im,cx-w,y,cx+w,y,"SU1"); put(im,cx-w,y,"SU2")
        if w>0: put(im,cx+w,y,"SU0")
    for x,y in((7,8),(9,11)): put(im,x,y,"SU0"); put(im,x+1,y,"SU0")
    for x,y in((7,4),(8,3),(9,4),(8,4),(7,3),(9,2),(8,2)): put(im,x,y,"GR2")
    put(im,8,2,"GR3"); put(im,7,3,"GR3")
def wheat_i(im):
    for x0,x1 in((5,4),(8,8),(11,12)): line(im,x0 if x0!=8 else 7,14,x1,6,"SU2")
    for x in(4,8,12):
        for k in range(4): put(im,x,5-k+ (1 if k>2 else 0),"SU4" if k<3 else "SU3")
    rect(im,5,10,11,11,"RD1"); put(im,6,10,"RD2")
def potato_i(im):
    blob(im,8,9,5.8,4.2,("WD1","WD2","WD3","CR0"))
    for x,y in((6,9),(10,8),(8,11),(5,11)): put(im,x,y,"WD1")
def tomato_i(im):
    blob(im,8,9.5,5.6,5,("RD1","RD2","RD3","CR1"))
    rect(im,5,4,11,4,"GR2"); put(im,8,3,"GR3"); put(im,6,5,"GR1"); put(im,10,5,"GR1"); put(im,8,5,"GR2")
def straw_i(im):
    for y,w in zip(range(5,15),[6,6,6,5,5,4,3,2,2,1]):
        st=8-w//2; rect(im,st,y,st+w-1,y,"RD2")
    put(im,5,6,"RD3"); put(im,6,6,"RD3"); put(im,5,7,"RD3")
    for x,y in((7,8),(10,8),(6,10),(8,10),(8,12)): put(im,x,y,"SU3")
    rect(im,5,4,10,4,"GR2"); put(im,7,3,"GR3"); put(im,8,3,"GR3"); put(im,6,5,"GR1"); put(im,9,5,"GR1")
def pumpkin_i(im):
    blob(im,8,10,6.5,4.8,("SU0","SU1","SU2","SU3"))
    for x,y0,y1 in((5,8,12),(8,6,14),(11,8,12)):
        for y in range(y0,y1+1): put(im,x,y,"SU0")
    put(im,8,4,"GR1"); put(im,8,5,"GR1"); put(im,9,4,"GR2")
def corn_i(im):
    blob(im,8,8.5,3.2,6,("SU2","SU3","SU4","SU4"),hi=False)
    for y in range(3,14):
        for x in range(5,12):
            if im.getpixel((x,y))[3] and (x+y)%2==0: put(im,x,y,"SU2" if x>8 else "SU4")
    rect(im,4,8,6,14,"GR3"); rect(im,10,8,12,14,"GR2"); rect(im,6,12,10,14,"GR2"); put(im,5,9,"GR4"); put(im,4,8,"GR3")
def wood_i(im):
    rect(im,2,6,13,11,"WD1"); rect(im,2,6,13,7,"WD2"); rect(im,11,6,13,11,"WD3"); put(im,12,8,"WD2"); put(im,12,9,"WD2"); put(im,13,8,"WD1")
    for x,y in((4,9),(6,10),(8,9)): put(im,x,y,"WD0")
def stone_i(im): blob(im,8,9,6,5,("ST1","ST2","ST3","ST4"))
def ore_i(im):
    blob(im,8,9,6,5,("ST1","ST2","ST3","ST3"),hi=False)
    for x,y in((5,8),(9,7),(10,11),(6,11)): put(im,x,y,"SU2"); put(im,x+1,y,"SU1")
    put(im,5,7,"SU4")
def milk_i(im):
    rect(im,5,6,10,13,"CR1"); rect(im,10,6,10,13,"CR0"); rect(im,6,3,9,5,"CR1"); rect(im,6,2,9,2,"RD2"); rect(im,5,9,10,11,"WA2"); rect(im,5,9,5,11,"WA3")
def egg_i(im): blob(im,8,9,4.2,5.2,("SK3","CR1","CR1","CR1"),hi=False); put(im,6,6,"CR1"); put(im,7,5,"CR1"); put(im,10,10,"SK2")
def wool_i(im):
    for cx,cy,rx,ry in((5.5,9,3.8,3.4),(10.5,9,3.8,3.4),(8,6.5,4,3.4),(8,10.5,5,3)): blob(im,cx,cy,rx,ry,("ST3","CR0","CR1","CR1"),hi=False)
def fert_i(im):
    rect(im,4,5,11,13,"WD2"); rect(im,4,5,4,13,"WD3"); rect(im,11,5,11,13,"WD1"); rect(im,5,3,10,4,"WD2"); put(im,5,3,"WD3"); rect(im,6,4,9,4,"RD1")
    rect(im,6,8,9,11,"CR0"); put(im,7,10,"GR2"); put(im,7,9,"GR2"); put(im,6,8,"GR3"); put(im,8,8,"GR3"); put(im,8,10,"SO3")
def plank_i(im):
    rect(im,2,4,13,7,"WD3"); rect(im,3,9,14,12,"WD3")
    for y in(5,10): rect(im,3 if y==5 else 4,y,12 if y==5 else 13,y,"WD2")
    rect(im,2,7,13,7,"WD2"); rect(im,3,12,14,12,"WD2"); put(im,3,5,"ST3"); put(im,12,5,"ST3"); put(im,4,10,"ST3"); put(im,13,10,"ST3")
def fiber_i(im):
    for x0,x1,c in((4,3,"GR3"),(6,6,"GR4"),(8,9,"GR3"),(10,12,"GR4")): line(im,x0,14,x1,3,c)
    rect(im,3,9,12,10,"SO4"); put(im,3,9,"WD3")
def coal_i(im): blob(im,8,9,5.5,4.8,("OL0","ST0","ST1","ST2"))
def bread_i(im):
    blob(im,8,9.5,6.5,4.2,("SU0","SU1","SU2","SU3"))
    for x,y in((5,9),(6,8),(8,8),(9,7),(11,9),(12,8)): put(im,x,y,"SU4")
def jam_i(im):
    rect(im,4,6,11,13,"RD1"); rect(im,4,6,5,13,"RD2"); put(im,4,7,"RD3"); put(im,4,8,"RD3"); rect(im,4,3,11,5,"ST2"); rect(im,4,3,11,3,"ST3"); rect(im,5,9,10,11,"CR0")
def cheese_i(im):
    rect(im,4,4,13,7,"SU4"); rect(im,3,8,12,13,"SU3"); rect(im,11,8,12,13,"SU2"); rect(im,13,5,13,7,"SU3")
    for x,y in((5,10),(8,12),(9,9)): put(im,x,y,"SU1"); put(im,x+1,y,"SU1")
IT=[]
def add(n,im): IT.append((n,im))
sc={"wheat":"SU2","carrot":"SU1","potato":"WD1","tomato":"RD2","strawberry":"AC2","pumpkin":"SU0","corn":"SU4"}
for k,c in sc.items(): add(f"item_seed_{k}",packet(c))
for k,fn,oc in(("wheat",wheat_i,"SU0"),("carrot",carrot_i,"SU0"),("potato",potato_i,"WD0"),("tomato",tomato_i,"RD0"),("strawberry",straw_i,"RD0"),("pumpkin",pumpkin_i,"SU0"),("corn",corn_i,"GR0")): add(f"item_{k}",item(fn,oc))
for k,fn in(("hoe",hoe),("watering_can",can),("axe",axe),("hammer",hammer),("pickaxe",pickaxe)): add(f"tool_{k}",item(fn,"WD0" if k!="watering_can" else "WA0"))
for k,fn,oc in(("wood",wood_i,"WD0"),("stone",stone_i,"ST0"),("ore_copper",ore_i,"ST0"),("milk",milk_i,"ST1"),("egg",egg_i,"WD1"),("wool",wool_i,"ST2"),
   ("fertilizer",fert_i,"SO1"),("plank",plank_i,"WD0"),("fiber",fiber_i,"GR0"),("coal",coal_i,"ST1"),("bread",bread_i,"SU0"),("jam",jam_i,"RD0"),("cheese",cheese_i,"SU0")): add(f"item_{k}",item(fn,oc))
assert len(IT)==32
isheet=sheet([i for _,i in IT],8,16,16); isheet.save(f"{OUT}/Items/items_16.png")
open(f"{OUT}/Items/items_16.names.txt","w").write("#cell=16x16 pivot=center\n"+"\n".join(n for n,_ in IT)+"\n")
for n,im in IT: im.save(f"{OUT}/Items/{n}.png")

# ================= PREVIEWS =================
tg=Image.open(f"{HERE}/../01_Environment/Tiles/tiles_ground.png").convert("RGBA")
tile=lambda i:tg.crop(((i%4)*16,(i//4)*16,(i%4)*16+16,(i//4)*16+16))
grass=[tile(i) for i in range(4)]; tilled=tile(6); wet=tile(7)
cols=6; rows=7; P=1
pv=new((cols+2)*16,(rows*2+3)*16)
for ty in range(pv.height//16):
    for tx in range(pv.width//16): pv.paste(grass[(tx*3+ty*5)%4],(tx*16,ty*16))
for r in range(rows):
    for c in range(cols):
        [pv.paste(wet if c==1 else tilled,((c+1)*16,(r*2+2+k)*16)) for k in(0,1)]
for r in range(rows):
    for c in range(cols):
        pv.alpha_composite(crop_imgs[r*6+c],((c+1)*16,(r*2+2)*16+32-32))
pv.save(f"{OUT}/Preview/crops_preview.png"); pv.resize((pv.width*4,pv.height*4),Image.NEAREST).save(f"{OUT}/Preview/crops_preview_x4.png")
W=8*16+8*2+2*0; chk=new(8*20+4,2*4*20+4)
for b,bg in enumerate(("CR1","OL0")):
    rect(chk,0,b*4*20,chk.width-1,b*4*20+4*20-1,bg)
    for i,(n,im) in enumerate(IT): chk.alpha_composite(im,(2+(i%8)*20+2,b*80+(i//8)*20+2))
chk.save(f"{OUT}/Preview/items_check_light_dark.png"); chk.resize((chk.width*5,chk.height*5),Image.NEAREST).save(f"{OUT}/Preview/items_check_x5.png")

bad=[]
for root,_,fs in os.walk(OUT):
    for f in fs:
        if f.endswith(".png") and "Preview" not in root:
            im=Image.open(os.path.join(root,f)).convert("RGBA")
            if any(p[3] not in(0,255) or (p[3]==255 and p not in PAL) for p in im.get_flattened_data() if hasattr(im,"get_flattened_data")) if hasattr(im,"get_flattened_data") else any(p[3] not in(0,255) or (p[3]==255 and p not in PAL) for p in im.getdata()): bad.append(f)
print("off-palette/semi-alpha:",bad or "none", "| crops sheet",cs.size,"items sheet",isheet.size)
