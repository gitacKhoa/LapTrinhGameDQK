import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,".."))
from pxlib import *
from PIL import ImageOps
TOOLDIR=os.path.join(HERE,"..","02_Crops_Items","Items")
DIRS=["down","up","left","right"]

# ---------- palettes ----------
SKIN={"light":("SK3","SK2","SK1"),"tan":("SK2","SK1","SK0"),"dark":("SK1","SK0","SO2"),"pale":("CR0","SK3","SK2")}
HAIR={"brown":("SO1","SO2","SO3"),"black":("OL0","ST0","ST1"),"blond":("SU0","SU3","SU4"),"gray":("ST2","ST3","ST4"),"red":("RD0","SU0","SU1"),"white":("ST3","ST4","CR1"),"auburn":("SO0","RD0","SU0")}
CLO={"red":("RD1","RD2","RD3"),"blue":("WA1","WA2","WA3"),"green":("GR1","GR2","GR3"),"yellow":("SU1","SU2","SU3"),"purple":("AC0","AC1","AC2"),
     "pink":("AC1","AC2","RD3"),"white":("ST3","CR0","CR1"),"brown":("WD0","WD1","WD2"),"gray":("ST1","ST2","ST3"),"orange":("SU0","SU1","SU2"),"teal":("WA0","WA1","WA2")}
PANTS={"denim":("WA0","WA1"),"brown":("SO1","SO2"),"gray":("ST0","ST1"),"green":("GR0","GR1"),"dark":("OL0","ST0")}
def outfit(**k):
    o=dict(skin="light",hair="brown",hstyle="short",hat=None,hatc="red",beard=None,glasses=False,shirt="red",pants="denim",kind="overalls",boots=("WD0","WD1"),overc="blue")
    o.update(k); return o

# ---------- body ----------
def face(L,o,b,expr):
    s=o["skin"]; ey=9+b
    def eyes(*pts): [put(L,x,y+b,"OL0") for x,y in pts]
    if expr=="neutral": eyes((5,9),(5,10),(10,9),(10,10))
    elif expr=="happy":
        eyes((5,10),(6,9),(10,10),(9,9)); put(L,6,11+b,"SO0"); put(L,9,11+b,"SO0"); put(L,7,12+b,"SO0"); put(L,8,12+b,"SO0"); put(L,4,11+b,"RD3"); put(L,11,11+b,"RD3")
    elif expr=="sad":
        eyes((5,9),(5,10),(10,9),(10,10)); put(L,5,11+b,"WA3"); put(L,7,11+b,"SO0"); put(L,8,11+b,"SO0"); put(L,6,12+b,"SO0"); put(L,9,12+b,"SO0")
    elif expr=="surprised":
        rect(L,5,8+b,6,9+b,"CR1"); rect(L,9,8+b,10,9+b,"CR1"); put(L,6,9+b,"OL0"); put(L,9,9+b,"OL0"); rect(L,7,11+b,8,12+b,"SO0")
    elif expr=="angry":
        eyes((5,10),(10,10),(5,8),(6,9),(10,8),(9,9)); put(L,7,12+b,"SO0"); put(L,8,12+b,"SO0"); put(L,4,11+b,"RD2"); put(L,11,11+b,"RD2")
    elif expr=="confused":
        eyes((5,9),(5,10),(10,10),(9,8),(10,8)); put(L,6,12+b,"SO0"); put(L,7,11+b,"SO0"); put(L,8,12+b,"SO0"); put(L,9,11+b,"SO0")
def legs_front(L,o,ldy,rdy,lt,dress):
    pa=PANTS[o["pants"]]; bo=o["boots"]; sk=SKIN[o["skin"]]
    for x0,dy in((5,ldy),(8,rdy)):
        fb=29+dy; col=sk[1] if dress else pa[1]; shc=sk[2] if dress else pa[0]
        rect(L,x0,lt,x0+2,fb-2,col); rect(L,x0+2,lt,x0+2,fb-2,shc)
        rect(L,x0,fb-2,x0+2,fb,bo[1]); rect(L,x0,fb,x0+2,fb,bo[0])
def body(d,o,b=0,ldy=0,rdy=0,sdx=0,expr="neutral"):
    L=new(16,32); sk=SKIN[o["skin"]]; hr=HAIR[o["hair"]]; sh=CLO[o["shirt"]]; pa=PANTS[o["pants"]]; ov=CLO[o["overc"]]
    kind=o["kind"]; dress=kind=="dress"; coat=kind=="coat"; lt=25 if (dress or coat) else 22
    back=d=="up"; side=d=="left"
    if not side:
        legs_front(L,o,ldy,rdy,lt,dress)
        # torso
        rect(L,4,14+b,11,21 if not(dress or coat) else 18,sh[1]); rect(L,4,14+b,4,21 if not(dress or coat) else 18,sh[2]); rect(L,11,14+b,11,21 if not(dress or coat) else 18,sh[0])
        if not back: rect(L,7,14+b,8,14+b,sk[2])
        if kind=="overalls":
            c=ov; rect(L,5,17,10,21,c[1]); rect(L,10,17,10,21,c[0]); rect(L,5,14+b,5,16,c[1]); rect(L,10,14+b,10,16,c[1])
            if not back: put(L,5,17,"SU3"); put(L,10,17,"SU3")
        if dress:
            for y,(x0,x1) in zip(range(19,25),[(4,11),(4,11),(3,12),(3,12),(3,12),(2,13)]): rect(L,x0,y,x1,y,sh[1]); put(L,x0,y,sh[2]); put(L,x1,y,sh[0])
            rect(L,2,24,13,24,sh[2]) if False else None
        if coat:
            c=CLO[o["overc"]]; rect(L,3,14+b,12,24,c[1]); rect(L,3,14+b,3,24,c[2]); rect(L,12,14+b,12,24,c[0]); rect(L,3,24,12,24,c[0])
            if not back: line(L,8,15+b,8,24,c[0]); put(L,7,18,"SU3"); put(L,9,21,"SU3")
        if kind=="apron":
            rect(L,5,15+b,10,23,"CR1"); rect(L,10,15+b,10,23,"ST4"); rect(L,5,23,10,23,"ST4"); put(L,4,19,"CR0"); put(L,11,19,"CR0")
            if back: rect(L,5,15+b,10,23,sh[1]); put(L,7,19,"CR1"); put(L,8,19,"CR1")
        if kind=="vest":
            c=CLO[o["overc"]]; rect(L,5,15+b,10,21,c[1]); rect(L,5,15+b,5,21,c[2]); rect(L,10,15+b,10,21,c[0]); 
            if not back: put(L,8,17,"SU3"); put(L,8,19,"SU3")
        # head
        if back:
            rect(L,4,7+b,11,12+b,sk[1]); rect(L,3,7+b,12,12+b,hr[1]); rect(L,3,7+b,3,12+b,hr[2]); rect(L,12,7+b,12,12+b,hr[0]); rect(L,4,12+b,11,12+b,hr[0])
            rect(L,7,13+b,8,13+b,sk[2])
        else:
            rect(L,4,7+b,11,12+b,sk[1]); rect(L,4,7+b,4,11+b,sk[0] if False else sk[1]); rect(L,4,12+b,4,12+b,sk[2]); rect(L,11,12+b,11,12+b,sk[2]); rect(L,6,8+b,9,8+b,sk[0]) if False else None
            put(L,5,8+b,sk[0]) if False else None
            rect(L,7,13+b,8,13+b,sk[2])
        hs=o["hstyle"]; hat=o["hat"]
        if hs!="bald" and not back:
            top=hr
            if not hat: rect(L,3,4+b,12,6+b,top[1]); rect(L,3,4+b,12,4+b,top[2]) if False else None; put(L,5,4+b,top[2]); put(L,6,4+b,top[2]); put(L,7,5+b,top[2])
            rect(L,3,7+b,4,10+b,top[1]); rect(L,11,7+b,12,10+b,top[1]); rect(L,3,7+b,3,10+b,top[2]); rect(L,12,7+b,12,10+b,top[0])
            rect(L,5,7+b,10,7+b,top[1]); put(L,8,7+b,sk[1]); put(L,7,7+b,sk[1]) if hs!="long" else None
            if hs=="long": rect(L,3,11+b,4,16+b,top[1]); rect(L,11,11+b,12,16+b,top[0]); rect(L,3,11+b,3,16+b,top[2])
            if hs=="bun" and not hat: rect(L,6,2+b,9,3+b,top[1]); put(L,6,2+b,top[2]); put(L,7,2+b,top[2])
            if hs=="pigtails": rect(L,1,8+b,2,12+b,top[1]); rect(L,13,8+b,14,12+b,top[0]); put(L,2,8+b,"RD2"); put(L,13,8+b,"RD2")
        if back and hs=="long": rect(L,3,13+b,12,17+b,hr[1]); rect(L,12,13+b,12,17+b,hr[0]); rect(L,3,13+b,3,17+b,hr[2])
        if back and hs=="pigtails": rect(L,1,8+b,2,12+b,hr[1]); rect(L,13,8+b,14,12+b,hr[0])
        if back and hs=="bun": rect(L,6,2+b,9,4+b,hr[1])
        if not back:
            face(L,o,b,expr)
            if o["beard"]:
                bc=HAIR[o["beard"]]; rect(L,4,11+b,11,13+b,bc[1]); rect(L,4,11+b,4,13+b,bc[2]); rect(L,11,11+b,11,13+b,bc[0]); rect(L,4,13+b,11,13+b,bc[0]); rect(L,6,11+b,9,11+b,sk[2]) if False else None
                put(L,7,12+b,bc[0]); put(L,8,12+b,bc[0])
            if o["glasses"]:
                for x0 in(4,9): rect(L,x0,8+b,x0+2,8+b,"ST2"); rect(L,x0,11+b,x0+2,11+b,"ST2"); put(L,x0,9+b,"ST2"); put(L,x0,10+b,"ST2"); put(L,x0+2,9+b,"ST2"); put(L,x0+2,10+b,"ST2")
                put(L,7,9+b,"ST2"); put(L,8,9+b,"ST2")
                put(L,5,9+b,"OL0"); put(L,5,10+b,"OL0"); put(L,10,9+b,"OL0"); put(L,10,10+b,"OL0")
        if hat=="straw":
            hc=("SU2","SU3","SU4"); rect(L,4,2+b,11,4+b,hc[1]); rect(L,4,2+b,11,2+b,hc[2]); rect(L,4,4+b,11,4+b,CLO[o["hatc"]][0]); rect(L,2,5+b,13,5+b,hc[1]); rect(L,2,6+b,13,6+b,hc[0])
            if back: pass
        if hat=="cap":
            c=CLO[o["hatc"]]; rect(L,3,3+b,12,5+b,c[1]); rect(L,3,3+b,12,3+b,c[2]); rect(L,3,5+b,12,5+b,c[0])
            if not back: rect(L,4,6+b,11,6+b,c[0])
        if hat=="bonnet":
            c=CLO[o["hatc"]]; rect(L,3,3+b,12,6+b,c[1]); rect(L,3,3+b,12,3+b,c[2]); rect(L,3,7+b,3,10+b,c[1]); rect(L,12,7+b,12,10+b,c[0])
    else:
        # ---- side view (facing left) ----
        pa=PANTS[o["pants"]]; bo=o["boots"]
        def leg(x0,dy,back_leg):
            fb=29+dy; col=(sk[2] if dress else pa[0]) if back_leg else (sk[1] if dress else pa[1]); bc=bo[0] if back_leg else bo[1]
            rect(L,x0,lt,x0+2,fb-2,col); rect(L,x0-1,fb-2,x0+2,fb,bc); rect(L,x0-1,fb,x0+2,fb,bo[0])
        fx=6-sdx; bx=6+sdx
        leg(bx,-1 if sdx<0 else 0,True); leg(fx,-1 if sdx>0 else 0,False)
        bot=21 if not(dress or coat) else 18
        rect(L,5,14+b,10,bot,sh[1]); rect(L,5,14+b,5,bot,sh[2]); rect(L,10,14+b,10,bot,sh[0])
        if kind=="overalls": rect(L,5,17,10,21,ov[1]) if False else rect(L,6,17,10,21,CLO[o["overc"]][1]); rect(L,10,17,10,21,CLO[o["overc"]][0]); rect(L,7,14+b,8,16,CLO[o["overc"]][1]); put(L,6,17,"SU3")
        if dress:
            for y,(x0,x1) in zip(range(19,25),[(5,10),(5,10),(4,11),(4,11),(4,11),(3,12)]): rect(L,x0,y,x1,y,sh[1]); put(L,x0,y,sh[2]); put(L,x1,y,sh[0])
        if coat:
            c=CLO[o["overc"]]; rect(L,4,14+b,11,24,c[1]); rect(L,4,14+b,4,24,c[2]); rect(L,11,14+b,11,24,c[0]); rect(L,4,24,11,24,c[0]); put(L,5,18,"SU3")
        if kind=="apron": rect(L,4,16+b,6,23,"CR1"); rect(L,6,16+b,6,23,"ST4"); put(L,6,15+b,"CR0")
        if kind=="vest": c=CLO[o["overc"]]; rect(L,5,15+b,10,21,c[1]); rect(L,10,15+b,10,21,c[0]); put(L,5,17,"SU3")
        rect(L,4,7+b,11,12+b,sk[1]); put(L,3,10+b,sk[1]); rect(L,6,13+b,8,13+b,sk[2]); put(L,8,10+b,sk[2])
        hs=o["hstyle"]; hat=o["hat"]; top=hr
        if hs!="bald":
            rect(L,8,7+b,11,11+b,top[1]); rect(L,11,7+b,11,11+b,top[0]); rect(L,4,7+b,6,7+b,top[1])
            if not hat: rect(L,4,4+b,11,6+b,top[1]); rect(L,4,4+b,8,4+b,top[2]); put(L,5,5+b,top[2])
            if hs=="long": rect(L,8,12+b,11,17+b,top[1]); rect(L,11,12+b,11,17+b,top[0]); rect(L,8,12+b,8,17+b,top[2]) if False else None
            if hs=="bun" and not hat: rect(L,10,2+b,12,4+b,top[1]); put(L,10,2+b,top[2])
            if hs=="pigtails": rect(L,11,8+b,12,13+b,top[1]); put(L,11,8+b,"RD2")
        put(L,5,9+b,"OL0"); put(L,5,10+b,"OL0")
        if expr=="happy": put(L,4,11+b,"RD3")
        if o["beard"]:
            bc=HAIR[o["beard"]]; rect(L,4,11+b,7,13+b,bc[1]); rect(L,4,11+b,4,13+b,bc[2]); rect(L,4,13+b,7,13+b,bc[0]); put(L,3,11+b,bc[1])
        if o["glasses"]: put(L,4,9+b,"ST2"); put(L,3,9+b,"ST2"); put(L,6,9+b,"ST2"); put(L,5,8+b,"ST2"); put(L,6,10+b,"ST2"); put(L,5,11+b,"ST2")
        if hat=="straw":
            hc=("SU2","SU3","SU4"); rect(L,4,2+b,10,4+b,hc[1]); rect(L,4,2+b,10,2+b,hc[2]); rect(L,4,4+b,10,4+b,CLO[o["hatc"]][0]); rect(L,1,5+b,11,5+b,hc[1]); rect(L,1,6+b,11,6+b,hc[0])
        if hat=="cap":
            c=CLO[o["hatc"]]; rect(L,4,3+b,11,5+b,c[1]); rect(L,4,3+b,11,3+b,c[2]); rect(L,4,5+b,11,5+b,c[0]); rect(L,2,6+b,5,6+b,c[0])
        if hat=="bonnet":
            c=CLO[o["hatc"]]; rect(L,4,3+b,11,6+b,c[1]); rect(L,4,3+b,11,3+b,c[2]); rect(L,9,7+b,11,10+b,c[1])
    return L

# ---------- arms + tools ----------
GRIP={"watering_can":(2,9)}; TOOLS={}
def tool_img(name):
    if name not in TOOLS: TOOLS[name]=Image.open(f"{TOOLDIR}/tool_{name}.png").convert("RGBA")
    return TOOLS[name]
def tf(name,rot,flip):
    im=tool_img(name); g=GRIP.get(name,(3,13))
    if flip: im=ImageOps.mirror(im); g=(15-g[0],g[1])
    for _ in range(rot): im=im.rotate(-90); g=(15-g[1],g[0])
    return im,g
def arm(cv,o,sx,sy,hx,hy,ox,oy):
    sl=CLO[o["shirt"]]; sk=SKIN[o["skin"]]
    for x,y in line_pts(sx,sy,hx,hy):
        put(cv,x+ox,y+oy,sl[2]); put(cv,x+1+ox,y+oy,sl[1])
    for x,y in line_pts(sx,sy,hx,hy): put(cv,x+1+ox,y+oy,sl[0]) if False else None
    rect(cv,hx+ox,hy+oy,hx+1+ox,hy+1+oy,sk[1]); put(cv,hx+ox,hy+oy,sk[0])

def pose(anim,d,f):
    side=d=="left"; P=dict(b=0,ldy=0,rdy=0,sdx=0,hands=None,tool=None)
    rest={"L":(2,19),"R":(12,19)} if not side else {"N":(6,19)}
    P["hands"]=dict(rest)
    if anim=="idle": P["b"]=[0,1][f]
    elif anim in("walk","carry_walk"):
        if not side:
            P["ldy"],P["rdy"]=[(0,0),(0,-1),(0,0),(-1,0)][f]
            if anim=="walk": P["hands"]={"L":[(2,19),(2,18),(2,19),(2,20)][f],"R":[(12,19),(12,20),(12,19),(12,18)][f]}
        else:
            P["sdx"]=[0,2,0,-2][f]
            if anim=="walk": P["hands"]={"N":(6+P["sdx"],19)}
    swing={"down":[(13,9,0),(14,14,1),(11,21,2)],"up":[(13,9,0),(14,14,1),(11,12,3)],"left":[(9,9,0),(6,8,3),(3,18,2)]}
    if anim in("hoe","chop","mine"):
        t={"hoe":"hoe","chop":"axe","mine":"pickaxe"}[anim]; hx,hy,rot=swing[d][f]; P["b"]=[0,0,1][f]
        if not side: P["hands"]={"L":(3,18),"R":(hx,hy)}; P["tool"]=(t,rot,False,"R")
        else: P["hands"]={"N":(hx,hy)}; P["tool"]=(t,rot,False,"N")
    if anim=="water":
        y=[17,16,15][f]
        if not side: P["hands"]={"L":(3,18),"R":(12,y)}; P["tool"]=("watering_can",0,False,"R")
        else: P["hands"]={"N":(4,y)}; P["tool"]=("watering_can",0,True,"N")
    if anim=="harvest":
        P["b"]=[1,2,1][f]
        if not side: P["hands"]={"L":[(4,20),(4,22),(5,18)][f],"R":[(11,20),(11,22),(10,18)][f]}
        else: P["hands"]={"N":[(3,19),(3,22),(4,17)][f]}
    if anim in("carry_idle","carry_walk"):
        if anim=="carry_idle": P["b"]=[0,1][f]
        P["hands"]={"L":(5,19),"R":(9,19)} if not side else {"N":(3,18)}
    return P
SH={"L":(2,15),"R":(12,15),"N":(6,15)}
def render(o,anim,d,f,big=True,expr="neutral"):
    P=pose(anim,d,f); ox,oy=(16,12) if big else (0,0)
    cv=new(48,48) if big else new(16,32)
    L=body(d,o,P["b"],P["ldy"],P["rdy"],P["sdx"],expr); cv.alpha_composite(L,(ox,oy))
    for k,(hx,hy) in P["hands"].items():
        sx,sy=SH[k]; arm(cv,o,sx,sy+P["b"],hx,hy,ox,oy)
    outline(cv,"OL0")
    if P["tool"]:
        name,rot,flip,k=P["tool"]; im,g=tf(name,rot,flip); hx,hy=P["hands"][k]
        lay=new(cv.width,cv.height); lay.paste(im,(hx+1+ox-g[0],hy+1+oy-g[1]),im); cv.alpha_composite(lay)
    return cv

ANIMS=[("idle",2),("walk",4),("hoe",3),("water",3),("harvest",3),("chop",3),("mine",3),("carry_idle",2),("carry_walk",4)]
def build_player(o,prefix):
    imgs=[];names=[]
    for ai,(an,n) in enumerate(ANIMS):
        for d in DIRS:
            fr=[]
            for f in range(n):
                if d=="right": fr.append(ImageOps.mirror(render(o,an,"left",f)))
                else: fr.append(render(o,an,d,f))
            for c in range(4):
                imgs.append(fr[c] if c<n else None); names.append(f"{prefix}_{an}_{d}_{c:02d}" if c<n else "")
    return sheet(imgs,4,48,48),names

PLAYERS={
 "player_a":outfit(skin="light",hair="brown",hat="straw",shirt="red",pants="denim",overc="blue",hatc="red"),
 "player_b":outfit(skin="dark",hair="black",hat="straw",shirt="green",pants="brown",overc="brown",hatc="blue"),
 "player_c":outfit(skin="pale",hair="blond",hstyle="long",hat=None,shirt="yellow",pants="denim",overc="teal"),
 "player_d":outfit(skin="tan",hair="red",hstyle="pigtails",hat=None,shirt="white",pants="green",overc="purple"),
}
NPCS={
 "npc_farmer_old":outfit(skin="light",hair="gray",hat="straw",beard="white",shirt="green",pants="brown",overc="brown",hatc="green"),
 "npc_baker":outfit(skin="tan",hair="brown",hstyle="bun",kind="apron",shirt="pink",pants="brown"),
 "npc_merchant":outfit(skin="light",hair="black",hat="cap",kind="coat",shirt="white",pants="dark",overc="blue",hatc="yellow"),
 "npc_girl":outfit(skin="pale",hair="blond",hstyle="pigtails",kind="dress",shirt="pink",pants="brown"),
 "npc_smith":outfit(skin="dark",hair="red",hstyle="bald",beard="red",kind="apron",shirt="gray",pants="dark"),
 "npc_scholar":outfit(skin="tan",hair="black",glasses=True,kind="vest",shirt="white",pants="gray",overc="purple"),
}
EXPR=["neutral","happy","sad","surprised","angry","confused"]
def build_npc(o,prefix):
    imgs=[];names=[]
    for an,n in(("idle",2),("walk",4)):
        for d in DIRS:
            fr=[]
            for f in range(n):
                fr.append(ImageOps.mirror(render(o,an,"left",f,False)) if d=="right" else render(o,an,d,f,False))
            for c in range(6): imgs.append(fr[c] if c<n else None); names.append(f"{prefix}_{an}_{d}_{c:02d}" if c<n else "")
    for c,e in enumerate(EXPR): imgs.append(render(o,"idle","down",0,False,e)); names.append(f"{prefix}_expr_{e}")
    return sheet(imgs,6,16,32),names

if __name__=="__main__":
    out=[]
    for k,o in PLAYERS.items():
        sh,nm=build_player(o,k); sh.save(f"{HERE}/Player/{k}_sheet.png"); open(f"{HERE}/Player/{k}_sheet.names.txt","w").write("#cell=48x48 pivot=0.5,0.125\n"+"\n".join(nm)+"\n"); out.append(sh.size)
    for k,o in NPCS.items():
        sh,nm=build_npc(o,k); sh.save(f"{HERE}/NPC/{k}_sheet.png"); open(f"{HERE}/NPC/{k}_sheet.names.txt","w").write("#cell=16x32 pivot=bottom\n"+"\n".join(nm)+"\n"); out.append(sh.size)
    # previews
    a=PLAYERS["player_a"]; CW=48
    P=Image.new("RGBA",(CW*9+8,CW*3+8),C["GR2"])
    for i in range(4): P.alpha_composite(render(a,"walk","down",i),(4+i*CW,4)); P.alpha_composite(render(a,"walk","left",i),(4+i*CW+4*CW,4)) if i<4 else None
    acts=["hoe","water","harvest","chop","mine"]
    for i,an in enumerate(acts): P.alpha_composite(render(a,an,"down",1),(4+i*CW,CW+4)); P.alpha_composite(render(a,an,"left",2 if an in("hoe","chop","mine") else 1),(4+i*CW,2*CW+4))
    for i,an in enumerate(["idle","carry_idle"]): P.alpha_composite(render(a,an,"up",0),(4+5*CW+i*CW,CW+4)); P.alpha_composite(render(a,an,"down",0),(4+5*CW+i*CW,2*CW+4))
    P.resize((P.width*3,P.height*3),Image.NEAREST).save(f"{HERE}/Preview/player_preview_x4.png")
    LU=Image.new("RGBA",(10*18+4,32*2+8),C["GR2"]); x=2
    for k,o in PLAYERS.items(): LU.alpha_composite(render(o,"idle","down",0).crop((16,12,32,44)).crop((0,0,16,32)),(x,2)); x+=18
    for k,o in NPCS.items(): LU.alpha_composite(render(o,"idle","down",0,False),(x,2)); x+=18
    x=2+4*18
    for k,o in NPCS.items(): LU.alpha_composite(render(o,"walk","left",1,False),(x,38)); x+=18
    LU.resize((LU.width*5,LU.height*5),Image.NEAREST).save(f"{HERE}/Preview/lineup_x5.png")
    EX=Image.new("RGBA",(6*18+4,6*34+4),C["GR2"])
    for i,(k,o) in enumerate(NPCS.items()):
        for j,e in enumerate(EXPR): EX.alpha_composite(render(o,"idle","down",0,False,e),(2+j*18,2+i*34))
    EX.resize((EX.width*4,EX.height*4),Image.NEAREST).save(f"{HERE}/Preview/expressions_x4.png")
    bad=[f for f in os.listdir(f"{HERE}/Player")+os.listdir(f"{HERE}/NPC") if f.endswith(".png")]
    print("sheets",out,"offpalette:",[f for f in os.listdir(f"{HERE}/Player") if f.endswith(".png") and offpalette(f"{HERE}/Player/{f}")]+[f for f in os.listdir(f"{HERE}/NPC") if f.endswith(".png") and offpalette(f"{HERE}/NPC/{f}")] or "none")
