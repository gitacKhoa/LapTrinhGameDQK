import os, random
from PIL import Image
OUT = os.path.dirname(os.path.abspath(__file__))
RAMPS = {
"OL":["1b1b2a"],"GR":["2d5a3a","3f7d45","5ea34f","8cc65a","c4e48a"],
"SO":["2c1d1a","3a2620","5b3b2c","7c553b","a67c52"],"WD":["5a3a22","8a5a33","b7814a","dba76a"],
"WA":["1d3f6e","2f6db3","4d9be0","8ecff0","e3f6fb"],"ST":["3d4150","636a7a","8d94a3","b9bfc9","e1e4ea"],
"SU":["b85c1e","e8872c","f7b844","fbe07a","fff3b8"],"RD":["7a1f2b","b5333a","e2574c","f58f7c"],
"SK":["8a5a44","c98b66","f0b894","ffd9b8"],"AC":["5a3a6b","8a5fa0","e78aa8"],"CR":["f4ecd8","fffaf0"]}
C = {f"{k}{i}": tuple(int(h[j:j+2],16) for j in (0,2,4))+(255,) for k,l in RAMPS.items() for i,h in enumerate(l)}
PALSET = set(C.values())
def new(w,h): return Image.new("RGBA",(w,h),(0,0,0,0))
def put(im,x,y,c):
    x=int(x); y=int(y)
    if 0<=x<im.width and 0<=y<im.height: im.putpixel((x,y), C[c] if isinstance(c,str) else c)
def rect(im,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): put(im,x,y,c)
def outline(im,c):
    src=im.copy()
    for y in range(im.height):
        for x in range(im.width):
            if src.getpixel((x,y))[3]==0:
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<im.width and 0<=ny<im.height and src.getpixel((nx,ny))[3]>0:
                        put(im,x,y,c); break
def blob(im,cx,cy,rx,ry,cols):
    d,m,l,h=cols
    for y in range(im.height):
        for x in range(im.width):
            nx=(x+.5-cx)/rx; ny=(y+.5-cy)/ry
            if nx*nx+ny*ny<=1:
                s=nx*.6+ny*.8
                put(im,x,y, d if s>.35 else (l if s<-.45 else m))
    put(im,cx-rx*.45,cy-ry*.5,h); put(im,cx-rx*.25,cy-ry*.62,h)

# ---------- GROUND TILES (16x16) ----------
def grass(seed,tufts=0):
    r=random.Random(seed); im=new(16,16); rect(im,0,0,15,15,"GR2")
    for y in range(16):
        for x in range(16):
            v=r.random()
            if v<.08: put(im,x,y,"GR1")
            elif v<.14: put(im,x,y,"GR3")
    for _ in range(tufts):
        x,y=r.randint(1,14),r.randint(2,14); put(im,x,y,"GR1"); put(im,x,y-1,"GR3"); put(im,x+1,y-1,"GR3"); put(im,x,y-2,"GR4")
    return im
def dirt(seed,pebble=False):
    r=random.Random(seed); im=new(16,16); rect(im,0,0,15,15,"SO3")
    for y in range(16):
        for x in range(16):
            v=r.random()
            if v<.10: put(im,x,y,"SO2")
            elif v<.17: put(im,x,y,"SO4")
    if pebble: put(im,4,9,"ST2"); put(im,5,9,"ST3"); put(im,4,10,"ST1"); put(im,5,10,"ST1")
    return im
def tilled(wet=False):
    m={"SO1":"SO0","SO2":"SO1","SO3":"SO2","SO4":"SO2"} if wet else {}
    g=lambda k:m.get(k,k); r=random.Random(7); im=new(16,16)
    for y in range(16):
        for x in range(16):
            k=y%4
            c={0:"SO1",1:"SO2",2:"SO4" if (x+y)%3==0 else "SO3",3:"SO3"}[k]
            if k==0 and r.random()<.2: c="SO2"
            put(im,x,y,g(c))
    return im
def path_dirt(seed):
    r=random.Random(seed); im=new(16,16); rect(im,0,0,15,15,"SO4")
    for y in range(16):
        for x in range(16):
            v=r.random()
            if v<.12: put(im,x,y,"SO3")
            elif v<.14: put(im,x,y,"ST2")
    return im
def path_stone(offs,seed):
    r=random.Random(seed); im=new(16,16)
    for y in range(16):
        for x in range(16):
            ry=y%8; row=y//8; bx=(x+offs[row])%8
            if ry==7 or bx==7: c="ST1"
            elif ry==0 or bx==0: c="ST3"
            else: c="ST2"
            if c=="ST2" and r.random()<.07: c="ST3"
            put(im,x,y,c)
    return im

# ---------- WATER 16-mask: N=1 E=2 S=4 W=8 (bit set = LAND on that side) ----------
def water_base(f):
    im=new(16,16); rect(im,0,0,15,15,"WA2")
    for wx,wy in((2,3),(10,7),(5,11),(13,14),(8,0)):
        for k in range(3): put(im,(wx+k+f)%16,wy,"WA3")
    for x,y in((7,1),(1,8),(12,12),(4,5)): put(im,x,y,"WA1")
    if f%2==1: put(im,(11+f)%16,7,"WA4")
    return im
def shore(mask,f):
    N,E,S,W=mask&1,mask&2,mask&4,mask&8
    pairs=[(N and W,(3,3)),(N and E,(12,3)),(S and W,(3,12)),(S and E,(12,12))]
    def land(x,y):
        x=min(15,max(0,x)); y=min(15,max(0,y))
        if (N and y<3) or (S and y>=13) or (W and x<3) or (E and x>=13): return True
        return any(p and (x,y)==pt for p,pt in pairs)
    im=water_base(f)
    for y in range(16):
        for x in range(16):
            nb=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            nbw=[n for n in nb if 0<=n[0]<16 and 0<=n[1]<16 and not land(*n)]
            if land(x,y):
                h=(x*7+y*13)%11
                put(im,x,y,"GR1" if nbw else ("GR1" if h==0 else "GR3" if h==1 else "GR2"))
            else:
                if any(land(*n) for n in nb if 0<=n[0]<16 and 0<=n[1]<16): put(im,x,y,"WA3")
    return im

# ---------- FENCE 16-mask ----------
def fence(mask):
    N,E,S,W=mask&1,mask&2,mask&4,mask&8; im=new(16,16)
    def hrail(x0,x1):
        for y0 in (5,9): rect(im,x0,y0,x1,y0,"WD3"); rect(im,x0,y0+1,x1,y0+1,"WD2")
    if E: hrail(8,15)
    if W: hrail(0,7)
    if N: rect(im,7,0,7,7,"WD3"); rect(im,8,0,8,7,"WD1")
    if S: rect(im,7,9,7,15,"WD3"); rect(im,8,9,8,15,"WD1")
    rect(im,6,3,9,12,"WD2"); rect(im,6,3,6,12,"WD3"); rect(im,9,3,9,12,"WD1"); rect(im,6,3,9,3,"WD3"); rect(im,6,12,9,12,"WD1")
    outline(im,"WD0"); return im

# ---------- OBJECTS ----------
def rock_small():
    im=new(16,16); blob(im,8,9.5,6,4.5,("ST1","ST2","ST3","ST4")); put(im,9,11,"ST1"); outline(im,"ST0"); return im
def rock_large():
    im=new(32,32); blob(im,16,19,13,10,("ST1","ST2","ST3","ST4"))
    for x,y in((18,12),(19,13),(19,14),(20,15),(9,20),(10,21),(11,21)): put(im,x,y,"ST1")
    for x,y in((8,16),(9,15),(12,13)): put(im,x,y,"ST4")
    outline(im,"ST0"); return im
def stump():
    im=new(16,16); rect(im,4,7,11,12,"WD1"); rect(im,4,7,5,12,"WD2"); rect(im,3,12,12,12,"WD1")
    for y in (9,10,11): put(im,7,y,"WD0"); put(im,10,y-1,"WD0")
    blob(im,8,6,4.6,2.8,("WD2","WD3","WD3","WD3")); 
    for x,y in((6,6),(7,6),(8,5),(9,6),(8,7)): put(im,x,y,"WD2")
    outline(im,"WD0"); return im
def bush(berries=False):
    im=new(16,16)
    for cx,cy,rx,ry in((8,9,6.3,4.8),(5.5,8.5,3.8,3.6),(10.5,8.5,3.8,3.6)): blob(im,cx,cy,rx,ry,("GR1","GR2","GR3","GR4"))
    if berries:
        for x,y in((5,8),(9,7),(11,10),(7,11)): put(im,x,y,"RD2"); put(im,x,y+0,"RD2")
        for x,y in((5,9),(9,8)): put(im,x,y,"RD0")
    outline(im,"GR0"); return im
def tuft():
    im=new(16,16)
    for x,h in((5,5),(8,7),(11,5)):
        for i in range(h):
            y=14-i; put(im,x,y,"GR1" if i<2 else "GR2" if i<h-2 else "GR3")
        put(im,x,14-h,"GR4")
    put(im,6,12,"GR3"); put(im,10,12,"GR3"); return im
def flowers(petal,center):
    im=new(16,16)
    for fx,fy in((4,5),(10,4),(8,9)):
        for k in range(1,5): put(im,fx,fy+k,"GR2")
        put(im,fx+1,fy+3,"GR3")
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)): put(im,fx+dx,fy+dy,petal)
        put(im,fx,fy,center)
    return im
def tree(seed=3):
    r=random.Random(seed); im=new(32,48)
    rect(im,13,28,18,45,"WD1"); rect(im,13,28,14,45,"WD2"); rect(im,18,28,18,45,"WD0")
    rect(im,11,44,20,45,"WD1"); rect(im,12,43,12,43,"WD1"); rect(im,19,43,19,43,"WD1")
    for y in (33,37,41): put(im,16,y,"WD0"); put(im,16,y+1,"WD0")
    outline(im,"WD0")
    cv=new(32,48); mask=set()
    for cx,cy,rx,ry in((16,14,12,10),(9,20,7,6),(23,20,7,6),(16,22,11,7),(11,12,7,6),(21,12,7,6)):
        for y in range(48):
            for x in range(32):
                if ((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2<=1: mask.add((x,y))
    for x,y in mask:
        s=((x-13)/14)*.55+((y-16)/13)*.85+(r.random()-.5)*.35
        put(cv,x,y,"GR1" if s>.55 else "GR2" if s>-.05 else "GR3" if s>-.6 else "GR4")
    outline(cv,"GR0"); im.alpha_composite(cv); return im
def sign():
    im=new(16,16); rect(im,7,8,8,14,"WD1"); rect(im,7,8,7,14,"WD2")
    rect(im,2,2,13,8,"WD3"); rect(im,2,2,13,2,"WD3"); rect(im,2,8,13,8,"WD2"); rect(im,2,2,2,8,"WD2"); rect(im,13,2,13,8,"WD1")
    outline(im,"WD0"); return im
def gate(open_=False):
    im=new(16,16)
    for x0 in (1,12): rect(im,x0,3,x0+2,13,"WD2"); rect(im,x0,3,x0,13,"WD3"); rect(im,x0+2,3,x0+2,13,"WD1")
    if not open_:
        for y0 in (5,9): rect(im,4,y0,11,y0,"WD3"); rect(im,4,y0+1,11,y0+1,"WD2")
        for i in range(8): put(im,4+i,10-int(i*5/7),"WD1")
    else:
        rect(im,4,1,5,11,"WD3"); rect(im,5,1,5,11,"WD2")
        for y in (4,8): rect(im,6,y,7,y,"WD2")
    outline(im,"WD0"); return im
def bridge_h():
    im=new(16,16)
    rect(im,0,3,15,12,"WD2")
    for x in range(16):
        if x%4==3: rect(im,x,3,x,12,"WD1")
    rect(im,0,3,15,3,"WD3")
    rect(im,0,1,15,1,"WD3"); rect(im,0,2,15,2,"WD1")
    rect(im,0,13,15,13,"WD3"); rect(im,0,14,15,14,"WD2")
    outline(im,"WD0"); return im

# ---------- BUILD OUTPUT ----------
def sheet(imgs,cols,cell=(16,16)):
    rows=(len(imgs)+cols-1)//cols; sh=new(cols*cell[0],rows*cell[1])
    for i,im in enumerate(imgs): sh.paste(im,((i%cols)*cell[0],(i//cols)*cell[1]))
    return sh
def save(im,rel):
    p=os.path.join(OUT,rel); im.save(p); return p
def names(lst,rel): open(os.path.join(OUT,rel),"w").write("\n".join(lst)+"\n")

ground={"env_grass_a":grass(1),"env_grass_b":grass(2,2),"env_grass_c":grass(3,3),"env_grass_d":grass(4,1),
 "env_dirt_a":dirt(5),"env_dirt_b":dirt(6,True),"env_tilled":tilled(),"env_tilled_wet":tilled(True),
 "env_path_dirt_a":path_dirt(8),"env_path_dirt_b":path_dirt(9),"env_path_stone_a":path_stone((0,4),10),"env_path_stone_b":path_stone((2,6),11)}
save(sheet(list(ground.values()),4),"Tiles/tiles_ground.png"); names(list(ground),"Tiles/tiles_ground.names.txt")
for k,v in ground.items(): save(v,f"Tiles/{k}.png") if False else None
wl=[(m,f) for f in range(4) for m in range(16)]
save(sheet([shore(m,f) for m,f in wl],16),"Tiles/tiles_water_16mask.png")
names([f"env_water_mask{m:02d}_f{f}" for m,f in wl],"Tiles/tiles_water_16mask.names.txt")
save(sheet([fence(m) for m in range(16)],16),"Tiles/tiles_fence_16mask.png")
names([f"env_fence_mask{m:02d}" for m in range(16)],"Tiles/tiles_fence_16mask.names.txt")
obj16={"obj_rock_small":rock_small(),"obj_stump":stump(),"obj_bush":bush(),"obj_bush_berry":bush(True),"obj_tuft":tuft(),
 "obj_flower_pink":flowers("AC2","SU3"),"obj_flower_yellow":flowers("SU3","SU1"),"obj_flower_white":flowers("CR1","SU2"),
 "obj_sign":sign(),"obj_gate_closed":gate(),"obj_gate_open":gate(True),"obj_bridge_h":bridge_h(),"obj_bridge_v":bridge_h().transpose(Image.TRANSPOSE)}
save(sheet(list(obj16.values()),13),"Objects/objects_16.png"); names(list(obj16),"Objects/objects_16.names.txt")
big={"obj_tree_a":tree(3),"obj_tree_b":tree(9),"obj_rock_large":rock_large()}
for k,v in {**obj16,**big}.items(): save(v,f"Objects/{k}.png")

# ---------- PREVIEW SCENE (30x17 tiles) ----------
rng=random.Random(42); T=16; GW,GH=30,17
scene=new(GW*T,GH*T); G=list(ground.values())
for ty in range(GH):
    for tx in range(GW):
        v=rng.random(); scene.paste(ground["env_grass_a" if v<.5 else "env_grass_b" if v<.67 else "env_grass_c" if v<.84 else "env_grass_d"],(tx*T,ty*T))
for tx in range(0,30):
    if not 4<=tx<=10: scene.paste(ground["env_path_dirt_a" if tx%2 else "env_path_dirt_b"],(tx*T,5*T))
for ty in range(8,11):
    for tx in range(24,27): scene.paste(ground["env_path_stone_a" if (tx+ty)%2 else "env_path_stone_b"],(tx*T,ty*T))
for ty in range(2,4):
    for tx in range(22,25): scene.paste(ground["env_dirt_a" if (tx+ty)%2 else "env_dirt_b"],(tx*T,ty*T))
lake={(x,y) for x in range(4,11) for y in range(2,9)}
for (x,y) in lake:
    m=sum(b for b,(dx,dy) in((1,(0,-1)),(2,(1,0)),(4,(0,1)),(8,(-1,0))) if (x+dx,y+dy) not in lake)
    scene.paste(shore(m,0),(x*T,y*T))
for x in range(4,11): scene.alpha_composite(obj16["obj_bridge_h"],(x*T,5*T))
for ty in range(9,12):
    for tx in range(13,19): scene.paste(ground["env_tilled_wet" if ty==10 and tx<16 else "env_tilled"],(tx*T,ty*T))
ring={(x,8) for x in range(12,20)}|{(x,12) for x in range(12,20)}|{(12,y) for y in range(8,13)}|{(19,y) for y in range(8,13)}
for (x,y) in ring:
    m=sum(b for b,(dx,dy) in((1,(0,-1)),(2,(1,0)),(4,(0,1)),(8,(-1,0))) if (x+dx,y+dy) in ring)
    scene.alpha_composite(fence(m),(x*T,y*T))
scene.paste(grass(1),(15*T,12*T)); scene.alpha_composite(obj16["obj_gate_closed"],(15*T,12*T))
items=[]
used=set(lake)|ring|{(x,5) for x in range(30)}
for t,x,y in(("obj_tree_a",1,3),("obj_tree_b",27,3),("obj_tree_a",28,13),("obj_tree_b",2,12),("obj_tree_a",25,15)): items.append((big[t],x*T+8-16,(y+1)*T-48,y))
items.append((big["obj_rock_large"],20*T+8-16,(14+1)*T-32,14))
for t,x,y in(("obj_rock_small",9,11),("obj_rock_small",26,6),("obj_stump",22,7),("obj_bush",7,12),("obj_bush_berry",12,3),("obj_bush",17,3),("obj_sign",11,12),("obj_bush_berry",24,12)): items.append((obj16[t],x*T,y*T,y))
fl=["obj_tuft","obj_flower_pink","obj_flower_yellow","obj_flower_white"]
for _ in range(26):
    x,y=rng.randint(0,29),rng.randint(0,16)
    if (x,y) in used or (13<=x<=18 and 9<=y<=11): continue
    items.append((obj16[rng.choice(fl)],x*T,y*T,y))
for im,x,y,_k in sorted(items,key=lambda i:i[3]): scene.alpha_composite(im,(x,y))
save(scene,"Preview/preview_scene_480x272.png")
save(scene.resize((scene.width*3,scene.height*3),Image.NEAREST),"Preview/preview_scene_x3.png")
# transparency check on light + dark
allo=list(obj16.values())+list(big.values()); W=sum(i.width+4 for i in allo)+4
chk=new(W,2*52+2)
for r,bg in enumerate(("CR1","OL0")):
    rect(chk,0,r*53,W-1,r*53+51,bg); x=4
    for im in allo: chk.alpha_composite(im,(x,r*53+52-im.height-2 if im.height<=50 else r*53+2)); x+=im.width+4
save(chk,"Preview/transparency_check_light_dark.png")
save(chk.resize((chk.width*3,chk.height*3),Image.NEAREST),"Preview/transparency_check_x3.png")

# ---------- VERIFY ----------
bad=[]
for root,_,fs in os.walk(OUT):
    for f in fs:
        if f.endswith(".png") and "Preview" not in root:
            im=Image.open(os.path.join(root,f)).convert("RGBA")
            for px in im.getdata():
                if px[3] not in (0,255) or (px[3]==255 and px not in PALSET): bad.append(f); break
print("files with off-palette/semi-transparent pixels:",bad or "none")
