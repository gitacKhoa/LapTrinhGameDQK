import os, sys, math
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,".."))
from pxlib import *
def asc(im,rows,m,ox,oy):
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch in m: put(im,ox+i,oy+j,m[ch])
def names_file(path,cell,names,pivot="center"): open(path,"w").write(f"#cell={cell[0]}x{cell[1]} pivot={pivot}\n"+"\n".join(names)+"\n")

# ---------- 16x16 effects ----------
def water(f):
    im=new(16,16)
    if f<4:
        for j,x in enumerate((4,8,12)):
            y=1+((f*3+j*2)%11)
            put(im,x,y,"WA4"); put(im,x,y+1,"WA3"); put(im,x,y+2,"WA2")
    else:
        r=[2,4][f-4]
        for dx,dy,c in((r,0,"WA3"),(-r,0,"WA3"),(r*.6,-1,"WA4"),(-r*.6,-1,"WA4"),(0,-2,"WA3")): put(im,8+dx,13+dy,c)
        for x,y in((3,12),(13,11),(8,10)): put(im,x,y,"WA2") if f==4 else None
        put(im,8,13,"WA2")
    return im
def dirt(f):
    im=new(16,16)
    P=[(35,2.6,"SO4",2),(60,3.0,"SO3",2),(85,2.2,"SO4",2),(110,3.0,"SO3",2),(135,2.6,"SO2",2),(50,1.8,"SO2",1),(120,1.8,"SO4",1),(90,3.4,"SO3",1)]
    for a,s,c,sz in P:
        vx=s*math.cos(math.radians(a))*.9; vy=-s*math.sin(math.radians(a))
        x=8+vx*f*1.1; y=12+vy*f+0.75*f*f
        if f>=3: sz=1
        if y<15 and f<5: rect(im,int(x),int(y),int(x)+sz-1,int(y)+sz-1,c)
    if f==0: rect(im,6,12,9,13,"SO3"); put(im,7,11,"SO4")
    return im
def harvest(f):
    im=new(16,16); l=[1,3,4,3,2,1][f]
    put(im,8,8,"SU4")
    for k in range(1,l+1):
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)): put(im,8+dx*k,8+dy*k,"SU4" if k<l else "SU3")
    if f in(1,2,3):
        for dx,dy in((1,1),(-1,1),(1,-1),(-1,-1)): put(im,8+dx*(l//2+1),8+dy*(l//2+1),"SU3")
    for a,c in((30,"GR3"),(150,"GR2"),(270,"GR3")):
        if f>=1:
            d=2+f*1.6; x=8+d*math.cos(math.radians(a)); y=8-d*math.sin(math.radians(a))+0.25*f*f
            put(im,x,y,c); put(im,x+1,y,"GR4") if f<4 else None
    return im
def pop(f):
    im=new(16,16); r=[1,3,5,6][f]
    for k in range(16 if f else 4):
        a=k*math.pi*2/(16 if f else 4); put(im,8+r*math.cos(a),8+r*math.sin(a)*.9,"CR1" if f<3 else "CR0")
    if f<2: put(im,8,8,"CR1"); put(im,7,8,"CR0")
    return im
def coin(f):
    im=new(16,16); w=[9,7,4,1,4,7][f]; h=10
    for y in range(16):
        for x in range(16):
            nx=(x+.5-8)/(w/2); ny=(y+.5-8)/(h/2)
            if nx*nx+ny*ny<=1: put(im,x,y,"SU2")
    if w>=7:
        for y in range(16):
            for x in range(16):
                if im.getpixel((x,y))[3] and x<8-w//2+2: put(im,x,y,"SU1")
        put(im,7,6,"SU4"); put(im,8,6,"SU4"); put(im,7,7,"SU4"); rect(im,7,8,8,10,"SU1")
    elif w>1: rect(im,8-w//2,5,7+w//2,10,"SU3"); put(im,8,5,"SU4")
    else: rect(im,8,4,8,11,"SU1")
    outline(im,"SU0"); return im
def smoke(f):
    im=new(16,16); cy=12-f*1.2; cx=8+math.sin(f*.9)*1.5; rx=min(2.2+f*.5,5.2); ry=rx*.85
    for y in range(16):
        for x in range(16):
            nx=(x+.5-cx)/rx; ny=(y+.5-cy)/ry
            if nx*nx+ny*ny<=1:
                s=nx*.5+ny*.7; c="ST3" if s>.35 else ("CR1" if s<-.4 else "CR0")
                rm=[False,False,False,False,(x+y)%4==0,(x+y)%2==0 and y%2==0,(x+y)%2==0,(x+y)%4!=1][f]
                if not rm: put(im,x,y,c)
    return im
FX=[("fx_water",6,water,12),("fx_dirt",5,dirt,14),("fx_harvest",6,harvest,12),("fx_pop",4,pop,12),("fx_coin",6,coin,12),("fx_smoke",8,smoke,8)]

# ---------- 8x8 weather / motes ----------
def rain_drop():
    im=new(8,8)
    for x,y,c in((5,0,"WA4"),(5,1,"WA3"),(4,2,"WA3"),(4,3,"WA2"),(3,4,"WA2"),(3,5,"WA1")): put(im,x,y,c)
    return im
def rain_splash(f):
    im=new(8,8); r=[1,2,3,3][f]
    for dx,dy,c in((r,0,"WA3"),(-r,0,"WA3"),(r*.6,-1,"WA4"),(-r*.6,-1,"WA4")): put(im,4+dx,6+dy,c) if not(f==3 and dy==-1) else None
    if f<2: put(im,4,6,"WA4")
    return im
def snow(v):
    im=new(8,8)
    if v==0: 
        for x,y in((4,3),(3,4),(4,4),(5,4),(4,5)): put(im,x,y,"CR1")
        put(im,4,4,"WA4")
    elif v==1: rect(im,3,3,4,4,"CR1"); put(im,3,3,"WA4")
    else:
        for x,y in((2,2),(5,2),(3,3),(4,3),(3,4),(4,4),(2,5),(5,5)): put(im,x,y,"CR1")
    return im
LEAF=[["..XXX..","XXXXXXX",".YYYYY."],["XXX....",".XXXX..","..XXXX.","...YYY."],["..XX..","..XX..","..XX..","..YY.."],["....XXX","..XXXX.",".XXXX..",".YYY..."]]
def leaf(f,c1,c2):
    im=new(8,8); asc(im,LEAF[f],{"X":c1,"Y":c2},0,2 if f in(0,) else 1); return im
def mote(row,f):
    im=new(8,8); a,b,c=(("SU2","SU3","SU4") if row==0 else ("ST3","CR0","CR1"))
    if f==0 or f==3: put(im,4,4,a if f==0 else b)
    if f==1:
        put(im,4,4,c)
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)): put(im,4+dx,4+dy,b)
    if f==2:
        put(im,4,4,c)
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)): put(im,4+dx,4+dy,c); put(im,4+dx*2,4+dy*2,a)
    return im

# ---------- emotes ----------
def bubble():
    im=new(16,16); rect(im,1,2,14,12,"CR1"); rect(im,2,1,13,13,"CR1"); rect(im,7,14,8,14,"CR1"); put(im,7,15,"CR1") if False else None
    rect(im,6,13,9,13,"CR1"); put(im,7,14,"CR1"); put(im,8,14,"CR1")
    outline(im,"SO0"); return im
def emote(name):
    im=bubble(); oy=1
    def A(rows,m,ox,oy_): asc(im,rows,m,ox,oy_+oy)
    if name=="heart": A(["..XXX.XXX.".replace("..","",1) if False else ".XXX.XXX.","XRRRXRRRX","XRHRRRRRX","XRRRRRRRX",".XRRRRRX.","..XRRRX..","...XRX...","....X...."],{"X":"RD0","R":"RD2","H":"RD3"},3,3)
    if name=="exclaim": rect(im,7,3+oy,8,8+oy,"RD2"); put(im,7,3+oy,"RD3"); rect(im,7,10+oy,8,11+oy,"RD2")
    if name=="question": A([".XXX.","X...X","....X","...X.","..X..","..X..",".....","..X.."],{"X":"WA1"},6,2)
    if name=="anger":
        for x,y in((4,4),(5,4),(4,5),(11,4),(10,4),(11,5),(4,10),(5,10),(4,9),(11,10),(10,10),(11,9),(8,7),(7,6),(9,8),(9,6),(7,8)): put(im,x,y+oy-1,"RD2")
    if name=="idea":
        blob(im,8,5+oy,3.2,3.2,("SU1","SU2","SU3","SU4")); rect(im,7,8+oy,9,9+oy,"ST2"); put(im,7,10+oy,"ST1"); put(im,8,10+oy,"ST1")
        for x,y in((3,3),(13,3),(8,0)): put(im,x,y+oy+1,"SU2")
    if name=="sleep":
        A(["XXXX","..X.",".X..","XXXX"],{"X":"ST1"},4,6); A(["XXX",".X.","XXX"],{"X":"ST2"},9,3)
    if name=="music": A(["..XXXX","..X..X","..X..X",".XX.XX",".XX.XX"],{"X":"AC1"},4,3)
    if name=="happy":
        blob(im,8,6+oy,3.8,3.8,("SU1","SU2","SU3","SU3"),hi=False); put(im,7,5+oy,"SO0"); put(im,10,5+oy,"SO0"); 
        for x,y in((6,7),(7,8),(8,8),(9,8),(10,7)): put(im,x,y+oy,"SO0")
    if name=="sad": A(["..X..",".XXX.","XXXXX","XXXXX",".XXX."],{"X":"WA2"},6,3); put(im,7,6+oy,"WA4")
    if name=="coin":
        blob(im,8,6+oy,3.6,3.6,("SU1","SU2","SU3","SU4")); rect(im,7,4+oy,8,8+oy,"SU1")
    return im
EMO=["heart","exclaim","question","anger","idea","sleep","music","happy","sad","coin"]
def shadow(w,h):
    im=new(w,h)
    for y in range(h):
        for x in range(w):
            if ((x+.5-w/2)/(w/2))**2+((y+.5-h/2)/(h/2))**2<=1: im.putpixel((x,y),(27,27,42,96))
    return im

if __name__=="__main__":
    imgs=[];nm=[]
    for n,k,fn,fps in FX:
        for c in range(8):
            imgs.append(fn(c) if c<k else None); nm.append(f"{n}_{c:02d}" if c<k else "")
    sheet(imgs,8,16,16).save(f"{HERE}/Sheets/fx_sheet_16.png"); names_file(f"{HERE}/Sheets/fx_sheet_16.names.txt",(16,16),nm)
    w=[rain_drop()]+[rain_splash(f) for f in range(4)]+[snow(v) for v in range(3)]+[leaf(f,"SU1","SU0") for f in range(4)]+[leaf(f,"RD2","RD0") for f in range(4)]
    wn=["fx_rain_drop"]+[f"fx_rain_splash_{f:02d}" for f in range(4)]+[f"fx_snow_{v:02d}" for v in range(3)]+[f"fx_leaf_orange_{f:02d}" for f in range(4)]+[f"fx_leaf_red_{f:02d}" for f in range(4)]
    sheet(w,8,8,8).save(f"{HERE}/Sheets/fx_weather_sheet_8.png"); names_file(f"{HERE}/Sheets/fx_weather_sheet_8.names.txt",(8,8),wn)
    m=[mote(r,f) for r in range(2) for f in range(4)]; mn=[f"fx_mote_{t}_{f:02d}" for t in("gold","white") for f in range(4)]
    sheet(m,8,8,8).save(f"{HERE}/Sheets/fx_mote_sheet_8.png"); names_file(f"{HERE}/Sheets/fx_mote_sheet_8.names.txt",(8,8),mn)
    e=[emote(n) for n in EMO]; sheet(e,5,16,16).save(f"{HERE}/Emotes/emote_sheet.png"); names_file(f"{HERE}/Emotes/emote_sheet.names.txt",(16,16),["emote_"+n for n in EMO],"bottom")
    SH={"shadow_s":(10,4),"shadow_m":(14,5),"shadow_l":(20,6),"shadow_xl":(30,9),"shadow_tree":(26,9)}
    for n,(a,b) in SH.items(): shadow(a,b).save(f"{HERE}/Shadows/{n}.png")
    # previews (light grass / dark)
    rows=[(n,[fn(c) for c in range(k)]) for n,k,fn,_ in FX]
    PW=8*20+8; PH=len(rows)*20+8+24+24+24
    pv=new(PW,PH); rect(pv,0,0,PW-1,PH-1,"GR2"); half=PW//2
    for i,(n,fr) in enumerate(rows):
        for c,im in enumerate(fr): pv.alpha_composite(im,(4+c*20,4+i*20))
    y=4+len(rows)*20
    for i,im in enumerate(w): pv.alpha_composite(im,(4+i*10,y))
    for i,im in enumerate(m): pv.alpha_composite(im,(4+i*10,y+12))
    pv2=new(PW,PH); rect(pv2,0,0,PW-1,PH-1,"OL0")
    for i,(n,fr) in enumerate(rows):
        for c,im in enumerate(fr): pv2.alpha_composite(im,(4+c*20,4+i*20))
    for i,im in enumerate(w): pv2.alpha_composite(im,(4+i*10,y))
    for i,im in enumerate(m): pv2.alpha_composite(im,(4+i*10,y+12))
    both=new(PW*2+4,PH); both.alpha_composite(pv,(0,0)); both.alpha_composite(pv2,(PW+4,0))
    both.resize((both.width*3,both.height*3),Image.NEAREST).save(f"{HERE}/Preview/fx_x3.png")
    # emotes + shadows preview
    ev=new(10*20+8,50); rect(ev,0,0,ev.width-1,49,"GR2")
    for i,im in enumerate(e): ev.alpha_composite(im,(4+i*20,4))
    x=4
    for n,(a,b) in SH.items():
        ev.alpha_composite(shadow(a,b),(x,32)); x+=a+6
    ev.resize((ev.width*5,ev.height*5),Image.NEAREST).save(f"{HERE}/Preview/emotes_shadows_x5.png")
    bad=[f"{d}/{f}" for d in("Sheets","Emotes") for f in os.listdir(f"{HERE}/{d}") if f.endswith(".png") and offpalette(f"{HERE}/{d}/{f}")]
    print("offpalette (shadows excluded by design):",bad or "none")
