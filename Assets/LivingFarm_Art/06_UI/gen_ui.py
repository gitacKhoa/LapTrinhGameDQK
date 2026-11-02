import os, sys, csv, math
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,".."))
from pxlib import *
OC="SO0"
def cdist(x,y,w,h): return min(x+y,(w-1-x)+y,x+(h-1-y),(w-1-x)+(h-1-y))
def pan(w,h,tl,br,fill,fsh=None,oc=OC):
    im=new(w,h); fw=len(tl); fsh=fsh or fill
    for y in range(h):
        for x in range(w):
            c=cdist(x,y,w,h)
            if c<2: continue
            dl,dr,dt,db=x,w-1-x,y,h-1-y; d=min(dl,dr,dt,db)
            if c==2 or d==0: col=oc
            elif d<=fw: col=(tl if (dt==d or dl==d) else br)[d-1]
            elif d==fw+1 and (dt==d or dl==d): col=fsh
            else: col=fill
            put(im,x,y,col)
    return im
def wood(fw=3): 
    tl=["WD3"]+["WD2"]*(fw-1); br=(["WD2"] if fw>=3 else [])+["WD1"]*(fw-2 if fw>=3 else fw-1)+["WD0"]; return tl,br
def panel(w,h,kind,fw=3):
    tl,br=wood(fw)
    if kind=="parchment": return pan(w,h,tl,br,"CR0","SK3")
    if kind=="wood": return pan(w,h,tl,br,"WD1","WD0")
    if kind=="dark": return pan(w,h,["WD2"]+["WD1"]*(fw-1),(["WD1"] if fw>=3 else [])+["WD0"]*(fw-1 if fw>=3 else fw),"SO1","SO0")
def dialog_box(w,h):
    im=panel(w,h,"parchment",3)
    for x,y in((4,4),(w-5,4),(4,h-5),(w-5,h-5)): put(im,x,y,"SU3"); put(im,x+0,y+1,"SU1") if False else None
    return im
def slot(sel=False):
    if sel: return pan(20,20,["SU3","SU2"],["SU3","SU2"],"SO2","SO1")
    return pan(20,20,["SO0","SO1"],["WD3","WD2"],"SO2","SO1")
def btn(w,h,theme,state):
    T={"wood":("WD3","WD2","WD1"),"green":("GR4","GR3","GR2"),"red":("RD3","RD2","RD1"),"gray":("ST3","ST2","ST1")}
    hi,face,sh=T["gray" if state=="disabled" else theme]
    if state=="hover": face,hi=hi,"CR1"
    im=new(w,h)
    for y in range(h):
        for x in range(w):
            c=cdist(x,y,w,h)
            if c<2: continue
            dt,db,dl,dr=y,h-1-y,x,w-1-x; d=min(dt,db,dl,dr)
            if c==2 or d==0: col=OC
            elif state=="pressed": col=sh if dt<=2 else face
            else: col=hi if dt==1 else (sh if db<=2 else face)
            put(im,x,y,col)
    return im
def keycap(pressed=False):
    im=new(16,16)
    for y in range(16):
        for x in range(16):
            c=cdist(x,y,16,16)
            if c<2: continue
            d=min(x,y,15-x,15-y)
            if c==2 or d==0: col=OC
            elif pressed: col="ST3" if y<=2 else "CR0"
            else: col="CR1" if y==1 else ("ST3" if y>=13 else "CR0")
            put(im,x,y,col)
    return im
def ribbon(w=48,h=20):
    im=new(w,h)
    for side in(0,1):
        for y in range(5,17):
            depth=max(0,5-int(abs(y-10.5)))
            for x in range(0,10):
                xx=x if side==0 else w-1-x
                if x>=depth: put(im,xx,y,"RD1")
    rect(im,6,1,w-7,12,"RD2"); rect(im,6,1,w-7,1,"RD3"); rect(im,6,11,w-7,12,"RD1")
    for side in(0,1):
        for y in range(12,17): 
            for x in range(6,10):
                xx=x if side==0 else w-1-x; put(im,xx,y,"RD0") if y-12<=9-x else None
    outline(im,OC); return im
def dial():
    im=new(32,32); cx=cy=15.5
    for y in range(32):
        for x in range(32):
            d=math.hypot(x-cx,y-cy)
            if d>16: continue
            if d>15: c=OC
            elif d>11: c="WD3" if (x+y)<28 else ("WD1" if (x+y)>34 else "WD2")
            elif d>10: c="SK3"
            else: c="CR0"
            put(im,x,y,c)
    for k in range(12):
        a=k*math.pi/6; 
        for r in((8,9) if k%3 else (7,8,9)): put(im,cx+r*math.sin(a),cy-r*math.cos(a),"SO2")
    rect(im,15,15,16,16,"SU3"); put(im,15,15,"SU4"); return im
def hand():
    im=new(3,13); rect(im,0,0,2,12,"SO1"); rect(im,1,0,1,12,"SO1"); rect(im,0,0,2,3,"RD2"); put(im,1,0,"RD3"); return im
def bar(w,h,fillc=None):
    return pan(w,h,["SO0"],["WD2"],"SO1")
def barfill(w,h,hi,mid,sh):
    im=new(w,h); rect(im,0,0,w-1,h-1,mid); rect(im,0,0,w-1,0,hi); rect(im,0,h-1,w-1,h-1,sh); return im
def arrow(f):
    im=new(8,8)
    for i,(x0,x1) in enumerate(((1,6),(2,5),(3,4))): rect(im,x0,1+i+f,x1,1+i+f,"SU3")
    put(im,1,1+f,"SU4"); put(im,2,1+f,"SU4"); outline(im,OC); return im
def divider():
    im=new(8,3); rect(im,0,0,7,0,"WD1"); rect(im,0,1,7,1,"WD3"); rect(im,0,2,7,2,"WD1"); return im

# ---------- icons 16x16 ----------
def asc(im,rows,m,ox,oy):
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch in m: put(im,ox+i,oy+j,m[ch])
def I(fn,oc):
    im=new(16,16); fn(im); outline(im,oc) if oc else None; return im
def coin(im): blob(im,8,8,5.2,5.2,("SU1","SU2","SU3","SU4")); rect(im,7,5,8,10,"SU1"); put(im,7,5,"SU3")
def sun(im):
    for x,y in((7,1),(8,1),(7,14),(8,14),(1,7),(1,8),(14,7),(14,8),(3,3),(12,3),(3,12),(12,12),(7,2),(8,2),(7,13),(8,13)): put(im,x,y,"SU3")
    blob(im,8,8,4.2,4.2,("SU1","SU2","SU3","SU4"))
def moon(im):
    for y in range(16):
        for x in range(16):
            a=((x+.5-7.5)/5.5)**2+((y+.5-8)/5.5)**2<=1; b=((x+.5-11)/4.6)**2+((y+.5-6)/4.6)**2<=1
            if a and not b: put(im,x,y,"SU4" if x+y<12 else "SU3")
    put(im,12,11,"CR1"); put(im,13,3,"CR1"); put(im,3,3,"CR1")
def calendar(im):
    rect(im,2,3,13,13,"CR1"); rect(im,2,3,13,5,"RD2"); rect(im,2,5,13,5,"RD1"); rect(im,5,1,5,3,"ST2"); rect(im,10,1,10,3,"ST2")
    for x,y in((4,8),(7,8),(10,8),(4,11),(7,11),(10,11)): rect(im,x,y,x+1,y,"SO3")
def cloud(im,cols=("ST3","CR0","CR1","CR1"),dy=0):
    for cx,cy,rx,ry in((5.5,9+dy,3.5,3),(10.5,8.5+dy,4.2,3.6),(8,10+dy,6.5,2.8)): blob(im,cx,cy,rx,ry,cols,hi=False)
def rain(im):
    cloud(im,dy=-3); 
    for x,y in((4,12),(7,13),(10,12),(13,13),(5,14),(11,14)): put(im,x,y,"WA2"); put(im,x,y+0,"WA3")
def storm(im):
    cloud(im,("ST0","ST1","ST2","ST2"),dy=-3); asc(im,["..XX","..XY",".XYX",".XYY","XYYX","..XY"],{"X":"SU0","Y":"SU3"},6,9) if False else None
    for x,y in((8,10),(7,11),(8,11),(6,12),(7,12),(8,12),(7,13),(6,14),(7,14)): put(im,x,y,"SU3")
    for x,y in((9,10),(9,11),(8,13)): put(im,x,y,"SU1")
def snow(im):
    cloud(im,dy=-3)
    for x,y in((4,12),(8,13),(12,12),(6,14),(10,14)): put(im,x,y,"WA4"); put(im,x+1,y,"WA3")
def heart(im): asc(im,[".XXX.XXX.","XRRRXRRRX","XRHRRRRRX","XRRRRRRRX",".XRRRRRX.","..XRRRX..","...XRX...","....X...."],{"X":"RD0","R":"RD2","H":"RD3"},3,4)
def star(im,full=True):
    m={"X":"SU0" if full else "ST1","Y":"SU3" if full else "ST2","Z":"SU4" if full else "ST3"}
    asc(im,["....X....","...XZX...","..XYYYX..","XXXYYYXXX",".XYYYYYX.","..XYYYX..","..XYXYX..",".XYX.XYX.",".XX...XX."],m,3,3)
def energy(im): asc(im,["...XXX.","..XYYX.",".XYYX..","XYYYYXX","XXXYYYX","...XYX.","..XYX..","..XYX..","...XX.."],{"X":"SU0","Y":"SU3"},4,2)
def quest(im):
    rect(im,3,3,12,12,"CR0"); rect(im,2,2,13,4,"CR1"); rect(im,2,11,13,13,"CR1"); rect(im,2,4,13,4,"SK3"); rect(im,2,13,13,13,"SK3")
    for y in(6,8): rect(im,5,y,10,y,"SO3")
    rect(im,7,10,8,11,"RD2")
def alert(im): rect(im,6,2,9,9,"RD2"); rect(im,6,2,6,9,"RD3"); rect(im,6,11,9,13,"RD2"); put(im,6,11,"RD3")
def backpack(im):
    blob(im,8,9.5,5.2,5,("WD0","WD1","WD2","WD3")); rect(im,5,5,10,7,"WD1"); rect(im,5,5,10,5,"WD2"); rect(im,7,8,8,9,"SU3"); rect(im,6,2,9,3,"WD1"); rect(im,7,3,8,3,"WD0")
def bag(im):
    blob(im,8,10,5.2,4.5,("WD1","WD2","WD3","WD3")); rect(im,6,3,9,6,"WD2"); rect(im,5,6,10,6,"RD2"); put(im,5,3,"WD3"); put(im,10,3,"WD3"); blob(im,8,10,2.2,2.2,("SU1","SU2","SU3","SU3"),hi=False)
def gear(im):
    for r in((7,1,8,3),(7,12,8,14),(1,7,3,8),(12,7,14,8)): rect(im,*r,"ST2")
    for x,y in((3,3),(12,3),(3,12),(12,12),(4,4),(11,4),(4,11),(11,11)): put(im,x,y,"ST2")
    blob(im,8,8,5,5,("ST1","ST2","ST3","ST4"))
    for y in range(16):
        for x in range(16):
            if math.hypot(x+.5-8,y+.5-8)<=1.9: im.putpixel((x,y),(0,0,0,0))
def pause(im): rect(im,4,3,6,12,"CR1"); rect(im,9,3,11,12,"CR1"); rect(im,6,3,6,12,"ST3"); rect(im,11,3,11,12,"ST3")
def play(im):
    for i in range(10): rect(im,5,3+i,max(5,12-abs(i-4.5)*1.6//1),3+i,"CR1") if False else rect(im,5,3+i,int(12-abs(i-4.5)*1.8),3+i,"CR1")
def close(im): line(im,4,4,11,11,"RD2"); line(im,11,4,4,11,"RD2"); line(im,5,4,12,11,"RD2"); line(im,12,4,5,11,"RD2")
def check(im):
    for a,b in(((3,8),(6,11)),((6,11),(12,4))): line(im,*a,*b,"GR3"); line(im,a[0],a[1]+1,b[0],b[1]+1,"GR3")
def plus(im): rect(im,7,3,8,12,"GR3"); rect(im,3,7,12,8,"GR3")
def minus(im): rect(im,3,7,12,8,"RD2")
def arrows(d):
    def f(im):
        t=[(r,c) for r in range(8) for c in range(8) if abs(c-3.5)<=3.5-r*0.5+0.1 and r<7]
        sh=new(16,16)
        for r in range(7):
            w=(7-r)//1; rect(sh,8-w//2-(0 if w%2 else 0),3+r,8-w//2-(0 if w%2 else 0)+w-1,3+r,"SU3")
        if d=="up": sh=sh.transpose(Image.FLIP_TOP_BOTTOM)
        if d=="left": sh=sh.rotate(-90)
        if d=="right": sh=sh.rotate(90)
        im.alpha_composite(sh)
    return f
def lock(im):
    rect(im,4,7,11,13,"SU2"); rect(im,4,7,11,7,"SU3"); rect(im,4,13,11,13,"SU1"); rect(im,5,3,10,3,"ST2"); rect(im,5,4,5,7,"ST2"); rect(im,10,4,10,7,"ST2"); rect(im,7,9,8,11,"SO0")
def home(im):
    for i in range(6): rect(im,8-i-1,2+i,8+i,2+i,"RD2")
    rect(im,3,8,12,13,"CR1"); rect(im,3,8,12,8,"CR0"); rect(im,7,10,9,13,"WD2"); rect(im,4,9,5,10,"WA3"); rect(im,10,9,11,10,"WA3")
def clock(im): blob(im,8,8,5.8,5.8,("ST3","CR0","CR1","CR1"),hi=False); rect(im,7,4,7,8,"SO2"); rect(im,7,8,10,8,"SO2")
def trash(im): rect(im,4,4,11,5,"ST2"); rect(im,6,2,9,3,"ST2"); rect(im,5,6,10,13,"ST3"); rect(im,5,6,5,13,"ST4"); 
def trash2(im):
    trash(im)
    for x in(6,8,10): rect(im,x,7,x,12,"ST1")
def map_(im):
    rect(im,2,3,13,12,"CR0"); rect(im,2,3,13,3,"CR1")
    for x in(6,10): rect(im,x,3,x,12,"SK3")
    line(im,4,5,5,10,"RD2") if False else None
    for a,b in(((7,5),(9,9)),((9,5),(7,9))): line(im,*a,*b,"RD2")
ICONS=[("coin",coin,"SU0"),("sun",sun,"SU0"),("moon",moon,"SU0"),("calendar",calendar,"RD0"),("cloud",cloud,"ST1"),("rain",rain,"ST1"),("storm",storm,"ST0"),("snow",snow,"ST1"),
 ("heart",heart,None),("energy",energy,None),("star",star,None),("star_empty",lambda im:star(im,False),None),("quest",quest,"WD0"),("alert",alert,"RD0"),("backpack",backpack,"WD0"),("bag",bag,"WD0"),
 ("gear",gear,"ST0"),("pause",pause,OC),("play",play,OC),("close",close,"RD0"),("check",check,"GR0"),("plus",plus,"GR0"),("minus",minus,"RD0"),("arrow_left",arrows("left"),OC),
 ("arrow_right",arrows("right"),OC),("arrow_up",arrows("up"),OC),("arrow_down",arrows("down"),OC),("lock",lock,"SU0"),("home",home,"RD0"),("clock",clock,"ST1"),("trash",trash2,"ST1"),("map",map_,"WD0")]

if __name__=="__main__":
    S={}
    S["ui_panel_parchment"]=(panel(24,24,"parchment"),(6,6,6,6)); S["ui_panel_wood"]=(panel(24,24,"wood"),(6,6,6,6)); S["ui_panel_dark"]=(panel(24,24,"dark"),(6,6,6,6))
    S["ui_dialogue_box"]=(dialog_box(32,32),(6,6,6,6)); S["ui_nameplate"]=(panel(24,14,"parchment",2),(5,5,5,5)); S["ui_hud_plate"]=(panel(24,16,"dark",2),(5,5,5,5)); S["ui_prompt_bubble"]=(panel(20,20,"parchment",2),(5,5,5,5))
    S["ui_slot"]=(slot(),(3,3,3,3)); S["ui_slot_selected"]=(slot(True),(3,3,3,3))
    for th in("wood","green","red"):
        for st in("normal","hover","pressed","disabled"):
            if th!="wood" and st=="disabled": continue
            S[f"ui_btn_{th}_{st}"]=(btn(32,16,th,st),(6,6,6,6))
    S["ui_btn_disabled"]=(btn(32,16,"wood","disabled"),(6,6,6,6))
    S["ui_keycap"]=(keycap(),(0,0,0,0)); S["ui_keycap_pressed"]=(keycap(True),(0,0,0,0))
    S["ui_ribbon_red"]=(ribbon(),(10,0,10,0))
    S["ui_bar_frame"]=(bar(24,8),(3,3,3,3)); S["ui_bar_v_frame"]=(pan(10,40,["SO0"],["WD2"],"SO1"),(3,3,3,3))
    S["ui_bar_fill_green"]=(barfill(8,4,"GR4","GR3","GR2"),(0,0,0,0)); S["ui_bar_fill_orange"]=(barfill(8,4,"SU4","SU2","SU1"),(0,0,0,0))
    S["ui_bar_fill_blue"]=(barfill(8,4,"WA3","WA2","WA1"),(0,0,0,0)); S["ui_bar_fill_red"]=(barfill(8,4,"RD3","RD2","RD1"),(0,0,0,0))
    S["ui_bar_mini_frame"]=(pan(14,5,["SO0"],["WD2"],"SO1"),(2,2,2,2)); S["ui_bar_mini_fill_green"]=(barfill(4,3,"GR4","GR3","GR2"),(0,0,0,0)); S["ui_bar_mini_fill_yellow"]=(barfill(4,3,"SU4","SU3","SU2"),(0,0,0,0))
    S["ui_scroll_track"]=(pan(6,16,["SO1"],["SO2"],"SO1"),(3,3,3,3)); S["ui_scroll_handle"]=(pan(6,12,["WD3"],["WD1"],"WD2"),(3,3,3,3))
    S["ui_divider"]=(divider(),(3,0,3,0)); S["ui_arrow_down_0"]=(arrow(0),(0,0,0,0)); S["ui_arrow_down_1"]=(arrow(1),(0,0,0,0))
    S["ui_clock_dial"]=(dial(),(0,0,0,0)); S["ui_clock_hand"]=(hand(),(0,0,0,0))
    rows=[]
    for n,(im,b) in S.items():
        im.save(f"{HERE}/Sprites/{n}.png"); rows.append((n,im.width,im.height,b[0],b[3],b[2],b[1]))  # Unity: left,bottom,right,top (mapping: l,t,r,b -> l,b,r,t)
    icons=[I(f,oc) for _,f,oc in ICONS]
    for (n,_,_),im in zip(ICONS,icons): im.save(f"{HERE}/Icons/icon_{n}.png")
    sheet(icons,8,16,16).save(f"{HERE}/Icons/icons_16.png")
    open(f"{HERE}/Icons/icons_16.names.txt","w").write("#cell=16x16 pivot=center\n"+"\n".join("icon_"+n for n,_,_ in ICONS)+"\n")
    with open(f"{HERE}/Unity/ui_sprites.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["name","w","h","border_left","border_bottom","border_right","border_top"])
        for n,wd,ht,l,b,r,t in rows: w.writerow([n,wd,ht,l,b,r,t])
    # ---------- preview screens ----------
    ITD=os.path.join(HERE,"..","02_Crops_Items","Items"); IT=lambda n:Image.open(f"{ITD}/{n}.png").convert("RGBA")
    ICON=lambda n:Image.open(f"{HERE}/Icons/icon_{n}.png").convert("RGBA")
    def nine(img,b,w,h):
        l,t,r,bm=b; sw,sh=img.size; out=new(w,h)
        xs=[(0,l,0,l),(l,sw-r,l,w-r),(sw-r,sw,w-r,w)]; ys=[(0,t,0,t),(t,sh-bm,t,h-bm),(sh-bm,sh,h-bm,h)]
        for sx0,sx1,dx0,dx1 in xs:
            for sy0,sy1,dy0,dy1 in ys:
                if sx1>sx0 and sy1>sy0 and dx1>dx0 and dy1>dy0: out.paste(img.crop((sx0,sy0,sx1,sy1)).resize((dx1-dx0,dy1-dy0),Image.NEAREST),(dx0,dy0))
        return out
    def N(name,w,h): im,b=S[name]; return nine(im,b,w,h)
    def txt(cv,x,y,w,col="SO3",hh=2): rect(cv,x,y,x+w-1,y+hh-1,col)
    bg0=Image.open(f"{HERE}/../01_Environment/Preview/preview_scene_480x272.png").convert("RGBA").crop((0,0,480,270))
    def scene(dim=0):
        s=bg0.copy()
        if dim: s=Image.alpha_composite(s,Image.new("RGBA",s.size,(15,12,20,dim)))
        return s
    def put_slots(cv,x0,y0,cols,rows,items,sel=-1):
        k=0
        for r in range(rows):
            for c in range(cols):
                cv.alpha_composite(S["ui_slot_selected"][0] if k==sel else S["ui_slot"][0],(x0+c*20,y0+r*20))
                if k<len(items) and items[k]: cv.alpha_composite(IT(items[k]),(x0+c*20+2,y0+r*20+2))
                k+=1
    scr=[]
    # 1 HUD
    s=scene(); s.alpha_composite(N("ui_hud_plate",56,20),(4,4)); s.alpha_composite(ICON("coin"),(8,6)); txt(s,28,12,24,"SU3")
    s.alpha_composite(dial(),(444,4)); d=dial()
    for k in range(5): put(s,460+k*3*math.sin(math.radians(50)),20-k*3*math.cos(math.radians(50)),"SO1")
    s.alpha_composite(N("ui_hud_plate",36,20),(440,40)); s.alpha_composite(ICON("sun"),(446,42)); txt(s,448,60,0)
    s.alpha_composite(N("ui_hud_plate",64,20),(4,28)); s.alpha_composite(ICON("calendar"),(8,30)); txt(s,28,36,32,"CR0")
    hb=N("ui_panel_wood",212,28); s.alpha_composite(hb,(134,238))
    its=["tool_hoe","tool_watering_can","tool_axe","tool_pickaxe","item_seed_carrot","item_seed_tomato","item_wood","item_stone","item_egg",None]
    put_slots(s,140,242,10,1,its,2)
    s.alpha_composite(N("ui_bar_v_frame",10,40),(466,224)); s.alpha_composite(barfill(6,26,"SU4","SU2","SU1"),(468,238)); s.alpha_composite(ICON("energy"),(463,206))
    scr.append(s)
    # 2 Inventory
    s=scene(130); s.alpha_composite(N("ui_panel_parchment",360,196),(60,40)); s.alpha_composite(N("ui_ribbon_red",120,20),(180,28))
    allit=["tool_hoe","tool_watering_can","tool_axe","tool_hammer","tool_pickaxe","item_seed_wheat","item_seed_carrot","item_seed_tomato","item_wheat","item_carrot","item_potato","item_tomato","item_strawberry","item_pumpkin","item_corn","item_wood","item_stone","item_ore_copper","item_milk","item_egg","item_wool","item_fertilizer","item_plank","item_fiber","item_coal","item_bread","item_jam","item_cheese"]
    put_slots(s,78,70,8,5,allit,9)
    s.alpha_composite(N("ui_panel_dark",132,150),(272,70)); s.alpha_composite(IT("item_tomato").resize((32,32),Image.NEAREST),(300,80)); txt(s,284,122,60,"CR1"); txt(s,284,130,100,"ST3"); txt(s,284,136,90,"ST3"); txt(s,284,142,96,"ST3"); s.alpha_composite(ICON("coin"),(284,176)); txt(s,304,184,30,"SU3")
    s.alpha_composite(N("ui_btn_red_normal",24,16),(384,28)); s.alpha_composite(ICON("close"),(388,28))
    scr.append(s)
    # 3 Shop
    s=scene(130); s.alpha_composite(N("ui_panel_parchment",380,200),(50,36)); s.alpha_composite(N("ui_ribbon_red",110,20),(185,24))
    shop=["item_seed_wheat","item_seed_carrot","item_seed_tomato","item_seed_corn","item_fertilizer"]
    for i,n in enumerate(shop):
        y=62+i*28; s.alpha_composite(S["ui_slot_selected"][0] if i==1 else S["ui_slot"][0],(66,y)); s.alpha_composite(IT(n),(68,y+2)); txt(s,92,y+4,70,"SO2"); txt(s,92,y+11,44,"SO3"); s.alpha_composite(ICON("coin"),(176,y+2)); txt(s,194,y+8,22,"WD1")
    s.alpha_composite(N("ui_panel_dark",150,160),(262,62)); s.alpha_composite(IT("item_seed_carrot").resize((48,48),Image.NEAREST),(312,72)); 
    for k,w in enumerate((90,110,100,80)): txt(s,274,130+k*8,w,"ST3")
    s.alpha_composite(N("ui_btn_green_normal",60,18),(274,196)); s.alpha_composite(N("ui_btn_wood_normal",60,18),(346,196)); s.alpha_composite(ICON("plus"),(290,196)) if False else None
    scr.append(s)
    # 4 Quests
    s=scene(130); s.alpha_composite(N("ui_panel_parchment",340,196),(70,40)); s.alpha_composite(N("ui_ribbon_red",120,20),(180,28))
    for i in range(3):
        y=66+i*50; s.alpha_composite(N("ui_slot",24,24),(86,y)); s.alpha_composite(ICON("quest"),(90,y+4)); txt(s,120,y+3,120,"SO2"); txt(s,120,y+11,150,"SO3"); txt(s,120,y+17,100,"SO3")
        s.alpha_composite(N("ui_bar_mini_frame",90,7),(120,y+28)); s.alpha_composite(N("ui_bar_mini_fill_green",[86,52,20][i],3),(122,y+30)) if False else rect(s,122,y+30,121+[86,52,20][i],y+32,"GR3")
        if i==0: s.alpha_composite(ICON("check"),(380,y+4))
        else: s.alpha_composite(ICON("coin"),(376,y+4)); txt(s,394,y+10,10,"WD1")
    scr.append(s)
    # 5 Dialogue
    s=scene(); npc=Image.open(f"{HERE}/../03_Characters/NPC/npc_baker_sheet.png").convert("RGBA").crop((0,0,16,32)); s.alpha_composite(npc,(232,150))
    s.alpha_composite(N("ui_dialogue_box",440,72),(20,186)); s.alpha_composite(N("ui_nameplate",80,16),(34,176)); txt(s,46,182,50,"SO2")
    for k,w in enumerate((380,360,200)): txt(s,38,202+k*10,w,"SO3")
    s.alpha_composite(arrow(0),(440,240)); s.alpha_composite(keycap(),(40,150)) if False else None; s.alpha_composite(N("ui_prompt_bubble",30,22),(228,120)); s.alpha_composite(keycap(),(235,123))
    scr.append(s)
    # 6 Pause
    s=scene(150); s.alpha_composite(N("ui_panel_dark",150,176),(165,47))
    for i in range(4):
        th="red" if i==3 else "wood"; s.alpha_composite(N(f"ui_btn_{th}_normal" if i!=1 else "ui_btn_wood_hover",110,22),(185,67+i*36)); txt(s,215,76+i*36,50,"SO0",3)
    scr.append(s)
    # 7 Day summary
    s=scene(150); s.alpha_composite(N("ui_panel_parchment",260,200),(110,35)); s.alpha_composite(N("ui_ribbon_red",130,22),(175,23))
    for i,n in enumerate(("item_wheat","item_carrot","item_milk","item_egg")):
        y=68+i*24; s.alpha_composite(S["ui_slot"][0],(130,y)); s.alpha_composite(IT(n),(132,y+2)); txt(s,160,y+8,60,"SO3"); s.alpha_composite(ICON("coin"),(290,y+2)); txt(s,310,y+8,36,"WD1")
    s.alpha_composite(divider().resize((220,3),Image.NEAREST),(130,165))
    for i in range(3): s.alpha_composite(ICON("star" if i<2 else "star_empty"),(210+i*20,176))
    s.alpha_composite(N("ui_btn_green_normal",80,20),(200,205)); scr.append(s)
    # 8 build/crafting mini
    s=scene(130); s.alpha_composite(N("ui_panel_parchment",300,180),(90,45)); s.alpha_composite(N("ui_nameplate",100,16),(100,38))
    for i,n in enumerate(("item_plank","item_fiber","item_fertilizer","item_bread")): s.alpha_composite(S["ui_slot_selected"][0] if i==0 else S["ui_slot"][0],(106+i*22,66)); s.alpha_composite(IT(n),(108+i*22,68))
    s.alpha_composite(N("ui_panel_dark",120,100),(106,100)); s.alpha_composite(N("ui_scroll_track",6,100),(374,100)); s.alpha_composite(N("ui_scroll_handle",6,30),(374,108))
    s.alpha_composite(N("ui_btn_gray_normal" if False else "ui_btn_disabled",80,18),(250,190)); scr.append(s)
    G=Image.new("RGBA",(480*3,270*3),C["OL0"])
    for i,im in enumerate(scr): G.paste(im,((i%3)*480,(i//3)*270))
    G.save(f"{HERE}/Preview/ui_screens_preview.png")
    # sprite catalogue
    cat=new(300,230); rect(cat,0,0,299,229,"CR1"); x=y=4; rowh=0
    for n,(im,b) in S.items():
        if x+im.width+4>296: x=4; y+=rowh+4; rowh=0
        cat.alpha_composite(im,(x,y)); x+=im.width+4; rowh=max(rowh,im.height)
    ic=sheet(icons,8,16,16); big=new(max(cat.width,128),y+rowh+4+70); rect(big,0,0,big.width-1,big.height-1,"CR1"); big.alpha_composite(cat.crop((0,0,300,y+rowh+4)),(0,0)); 
    row=new(128,64); rect(row,0,0,127,63,"GR2"); row.alpha_composite(ic,(0,0)); big.alpha_composite(row,(4,y+rowh+4+2)) if False else None
    big.resize((big.width*3,big.height*3),Image.NEAREST).save(f"{HERE}/Preview/ui_catalogue_x3.png")
    row.resize((512,256),Image.NEAREST).save(f"{HERE}/Preview/icons_x4.png")
    bad=[f for d in("Sprites","Icons") for f in os.listdir(f"{HERE}/{d}") if f.endswith(".png") and offpalette(f"{HERE}/{d}/{f}")]
    print("sprites:",len(S),"icons:",len(icons),"offpalette:",bad or "none")
