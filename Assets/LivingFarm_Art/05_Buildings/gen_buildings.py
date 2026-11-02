import os, sys, csv
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,".."))
from pxlib import *
OC="SO0"
def roof(im,x0,y0,x1,y1,xt0,xt1,cols,w=8,h=4):
    sh,mid,hi=cols
    for y in range(y0,y1+1):
        t=(y-y0)/(y1-y0); xl=round(xt0+(x0-xt0)*t); xr=round(xt1+(x1-xt1)*t)
        r=(y-y0)//h; yy=(y-y0)%h
        for x in range(xl,xr+1):
            xx=(x+(w//2 if r%2 else 0))%w
            c=mid
            if yy==h-1 or xx==w-1: c=sh
            elif yy==0: c=hi
            put(im,x,y,c)
    for x in range(round(xt0),round(xt1)+1): put(im,x,y0,hi)
def siding(im,x0,y0,x1,y1,cols,step=4,horizontal=True):
    sh,mid,hi=cols
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            k=(y-y0) if horizontal else (x-x0)
            c=mid
            if k%step==step-1: c=sh
            elif k%step==0: c=hi if horizontal else mid
            put(im,x,y,c)
def stones(im,x0,y0,x1,y1):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            r=(y-y0)//3; xx=(x+(3 if r%2 else 0))%7; yy=(y-y0)%3
            put(im,x,y,"ST1" if yy==2 or xx==6 else ("ST3" if yy==0 else "ST2"))
def window(im,wx,wy,ww,wh,frame="CR1"):
    rect(im,wx-1,wy-1,wx+ww,wy+wh,frame); rect(im,wx,wy,wx+ww-1,wy+wh-1,"WA2"); rect(im,wx,wy,wx+ww-1,wy+wh//2-1,"WA3")
    rect(im,wx+ww//2-1,wy,wx+ww//2,wy+wh-1,frame); rect(im,wx,wy+wh//2-1,wx+ww-1,wy+wh//2,frame)
    put(im,wx+1,wy+1,"WA4"); put(im,wx+2,wy+1,"WA4")

def house():
    im=new(80,64)
    siding(im,1,30,78,57,("WD1","WD2","WD3")); rect(im,1,30,78,31,"WD1"); rect(im,1,30,2,57,"WD1"); rect(im,77,30,78,57,"WD1")
    stones(im,1,58,78,62)
    roof(im,1,4,78,29,14,65,("RD0","RD1","RD2")); rect(im,1,29,78,29,"RD0")
    for y in range(1,17):
        for x in range(54,64): put(im,x,y,"ST1" if (y%3==0 or (x+y//3)%5==0) else "ST2")
    rect(im,53,0,64,2,"ST3"); rect(im,53,2,64,2,"ST1"); rect(im,54,0,63,0,"ST4")
    rect(im,33,39,46,61,"WD0"); rect(im,34,40,45,61,"WD1")
    for x in(37,42): rect(im,x,50,x,61,"WD0")
    rect(im,36,42,43,48,"WA3"); rect(im,36,42,43,42,"WD0"); rect(im,36,48,43,48,"WD0"); rect(im,36,42,36,48,"WD0"); rect(im,43,42,43,48,"WD0"); rect(im,39,43,40,47,"WA2")
    put(im,43,53,"SU3"); put(im,43,54,"SU2")
    rect(im,31,60,48,62,"ST3"); rect(im,31,62,48,62,"ST1")
    for wx in(11,57):
        window(im,wx,36,14,15); rect(im,wx-2,52,wx+15,53,"CR0"); rect(im,wx-1,54,wx+14,57,"WD1"); rect(im,wx-1,54,wx+14,54,"GR2")
        for i,c in enumerate(("RD2","SU3","CR1","RD2","SU3","CR1","RD2")): put(im,wx+i*2,53,c); put(im,wx+i*2,54,"GR3")
    outline(im,OC); return im
def barn():
    im=new(64,48)
    siding(im,1,18,62,43,("RD0","RD1","RD2"),4,False); rect(im,1,18,62,19,"CR1"); rect(im,1,18,3,43,"CR0"); rect(im,60,18,62,43,"CR0")
    stones(im,1,44,62,47)
    roof(im,1,0,62,17,16,47,("ST0","ST1","ST2")); rect(im,1,17,62,17,"ST0")
    rect(im,27,5,36,14,"CR1"); rect(im,28,6,35,13,"SO0"); rect(im,28,12,35,13,"SU3"); put(im,30,12,"SU2"); put(im,33,13,"SU2")
    rect(im,19,23,44,47,"CR1"); rect(im,20,24,43,47,"RD2"); rect(im,31,24,32,47,"RD0")
    for x0,x1 in((20,30),(33,43)):
        for i in range(0,22): 
            t=i/21; put(im,round(x0+(x1-x0)*t),25+i,"CR1"); put(im,round(x1-(x1-x0)*t),25+i,"CR1")
        rect(im,x0,24,x1,24,"CR1")
    rect(im,31,34,32,36,"SU3")
    outline(im,OC); return im
def coop():
    im=new(32,32)
    siding(im,1,14,30,29,("WD1","WD2","WD3"),4,False); rect(im,1,30,30,31,"WD0"); rect(im,1,14,30,15,"WD1")
    roof(im,1,0,30,13,8,23,("SU0","SU1","SU2"),8,4); rect(im,1,13,30,13,"SU0")
    rect(im,11,18,20,29,"WD0"); rect(im,12,19,19,29,"SO0"); put(im,13,20,"SO1")
    for k in range(4): rect(im,11,27+k//2,20,28+k//2,"WD2") if False else None
    rect(im,11,28,20,31,"WD2"); rect(im,11,28,20,28,"WD3"); rect(im,11,30,20,30,"WD1")
    for x in(13,16,19): rect(im,x,28,x,31,"WD1")
    rect(im,3,18,8,23,"CR1"); rect(im,4,19,7,22,"WA2"); put(im,4,19,"WA4")
    rect(im,23,22,29,27,"WD1"); rect(im,23,22,29,22,"WD3"); rect(im,24,21,28,21,"SU3"); put(im,26,20,"SU3"); put(im,26,21,"CR1"); put(im,25,21,"CR1")
    outline(im,OC); return im
def cowbarn():
    im=new(48,48)
    siding(im,1,17,46,43,("WD1","WD3","WD3"),4,False); rect(im,1,17,46,18,"WD1"); rect(im,1,17,3,43,"WD2"); rect(im,44,17,46,43,"WD2")
    stones(im,1,44,46,47)
    roof(im,1,0,46,16,12,35,("WA0","WA1","WA2")); rect(im,1,16,46,16,"WA0")
    rect(im,13,22,34,47,"WD1"); rect(im,15,24,32,47,"SO0")
    for x,y in((15,24),(16,24),(15,25),(32,24),(31,24),(32,25)): put(im,x,y,"WD1")
    rect(im,15,40,32,47,"SU3"); 
    for x,y in((17,41),(21,43),(25,41),(29,44),(19,45),(27,46)): put(im,x,y,"SU2")
    for x,y in((18,43),(23,42),(30,42)): put(im,x,y,"SU4")
    for wx in(4,38): rect(im,wx-1,23,wx+6,30,"WD1"); rect(im,wx,24,wx+5,29,"SO0"); rect(im,wx,24,wx+5,24,"WD2")
    outline(im,OC); return im
def chest(open_):
    im=new(16,16)
    rect(im,2,7,13,13,"WD2"); rect(im,2,7,2,13,"WD3"); rect(im,13,7,13,13,"WD1"); rect(im,2,13,13,13,"WD1")
    for x in(4,10): rect(im,x,7,x+1,13,"ST2"); rect(im,x,7,x,13,"ST3")
    if not open_:
        rect(im,2,3,13,6,"WD3"); rect(im,3,2,12,2,"WD3"); rect(im,2,6,13,6,"WD2")
        for x in(4,10): rect(im,x,3,x+1,6,"ST2")
        rect(im,7,6,8,9,"SU3"); put(im,7,6,"SU4"); put(im,8,9,"SU1")
    else:
        rect(im,3,1,12,3,"WD3"); rect(im,3,3,12,3,"WD2"); rect(im,2,4,13,6,"SO0")
        for x,y in((4,5),(7,4),(9,5),(11,4),(6,6)): put(im,x,y,"SU3")
        put(im,7,5,"SU4"); put(im,10,6,"SU2")
        rect(im,7,7,8,9,"SU3")
    outline(im,OC); return im

# ---- machines ----
def dairy(s):
    im=new(16,16); rect(im,2,8,13,14,"WD2"); rect(im,2,8,2,14,"WD3"); rect(im,13,8,13,14,"WD1"); rect(im,2,14,13,14,"WD0")
    rect(im,5,10,10,12,"WD1"); rect(im,6,11,9,11,"WD3")
    rect(im,3,3,12,7,"ST3"); rect(im,3,3,12,3,"ST4"); rect(im,3,7,12,7,"ST1"); rect(im,3,3,3,7,"ST4"); rect(im,12,3,12,7,"ST2")
    if s==0: rect(im,4,4,11,5,"ST2")
    else:
        rect(im,4,4,11,6,"CR1"); rect(im,4,6,11,6,"CR0")
        x=8 if s==1 else 10
        for y in range(1,5): put(im,x,y,"WD3")
        put(im,x,1,"WD2"); put(im,x-1,5,"CR0"); put(im,x+1,4,"CR0") if s==2 else put(im,x-2,4,"CR0")
    if s==3:
        rect(im,4,4,11,5,"ST2"); blob(im,8,3,4,2.4,("SU2","SU3","SU4","SU4"))
        rect(im,6,1,10,2,"SU3"); put(im,6,2,"SU2")
    rect(im,13,6,14,10,"ST2"); put(im,14,6,"ST3")
    outline(im,OC); return im
def jam(s):
    im=new(16,16); rect(im,3,13,12,14,"WD1"); rect(im,3,13,12,13,"WD2")
    blob(im,8,9,6,5,("SU0","SU1","SU2","SU3")); rect(im,1,8,2,9,"ST2"); rect(im,13,8,14,9,"ST2")
    rect(im,4,4,11,6,"SU0"); blob(im,8,5,4.2,1.7,("RD1","RD2","RD2","RD3"),hi=False)
    if s==0: rect(im,5,5,10,5,"RD1")
    if s==1: put(im,6,4,"RD3"); put(im,9,5,"RD3"); put(im,10,4,"RD3")
    if s==2: put(im,7,5,"RD3"); put(im,5,4,"RD3"); put(im,9,4,"RD3"); put(im,8,3,"RD3")
    if s==3:
        rect(im,6,5,9,5,"RD1"); rect(im,10,9,14,13,"RD1"); rect(im,10,9,14,9,"ST2"); rect(im,10,10,10,13,"RD2"); put(im,12,11,"CR0")
    outline(im,OC); return im
def oven(s):
    im=new(16,16); rect(im,2,5,13,14,"ST2")
    for y in range(5,15):
        for x in range(2,14):
            if y%3==0 or (x+(y//3)*3)%6==0: put(im,x,y,"ST1")
    rect(im,2,5,13,5,"ST3"); rect(im,2,5,2,14,"ST3"); rect(im,13,5,13,14,"ST1"); rect(im,2,14,13,14,"ST0")
    rect(im,10,1,12,4,"ST1"); rect(im,10,1,12,1,"ST3"); put(im,10,2,"ST2")
    rect(im,4,8,11,14,"ST3"); rect(im,5,9,10,14,"SO0")
    if s in(1,2):
        pts=[(7,13),(8,13),(6,13),(9,13),(7,12),(8,12),(8,11)] if s==1 else [(6,13),(7,13),(8,13),(9,13),(7,12),(8,12),(7,11)]
        for x,y in pts: put(im,x,y,"SU2")
        for x,y in pts[:4]: put(im,x,y,"RD2")
        put(im,pts[-1][0],pts[-1][1],"SU4"); put(im,pts[-2][0],pts[-2][1],"SU3")
    if s==3:
        blob(im,8,12,3.2,1.8,("SU1","SU2","SU3","SU3"),hi=False); rect(im,5,13,10,13,"ST2")
    outline(im,OC); return im
def crafting(s):
    im=new(32,16); rect(im,1,5,30,7,"WD3"); rect(im,1,5,30,5,"WD3"); rect(im,1,7,30,7,"WD2"); rect(im,1,8,30,14,"WD2"); rect(im,1,8,30,8,"WD1")
    for x in(1,15,30): rect(im,x,8,x,14,"WD1")
    rect(im,3,10,13,13,"WD1"); rect(im,17,10,28,13,"WD1"); rect(im,7,11,9,11,"ST2"); rect(im,21,11,24,11,"ST2")
    rect(im,1,14,30,14,"WD0")
    rect(im,19,3,27,4,"WD3"); rect(im,19,4,27,4,"WD2")
    if s==0: line(im,5,4,9,4,"WD2"); rect(im,9,2,11,4,"ST3")
    if s==1: line(im,6,3,9,1,"WD2"); rect(im,9,1,12,2,"ST3")
    if s==2: line(im,6,4,10,4,"WD2"); rect(im,10,2,12,5,"ST3"); put(im,13,4,"SU3"); put(im,14,3,"SU3")
    if s==3: line(im,5,4,9,4,"WD2"); rect(im,9,2,11,4,"ST3"); rect(im,13,1,17,4,"RD2"); rect(im,13,1,17,1,"RD3"); rect(im,14,2,16,2,"SU3")
    outline(im,OC); return im
def sprinkler(tier,s):
    im=new(16,16); rect(im,5,13,10,14,"ST1") ; rect(im,5,13,10,13,"ST2")
    pole={"basic":("WD1","WD2"),"quality":("ST1","ST2"),"super":("SU1","SU2")}[tier]
    rect(im,7,7,8,13,pole[1]); rect(im,8,7,8,13,pole[0])
    head={"basic":("ST1","ST2","ST3"),"quality":("ST2","ST3","ST4"),"super":("SU2","SU3","SU4")}[tier]
    rect(im,5,5,10,7,head[1]); rect(im,5,5,10,5,head[2]); rect(im,5,7,10,7,head[0]); rect(im,7,3,8,4,head[1])
    if tier=="quality": rect(im,6,2,9,3,"RD2"); rect(im,6,2,9,2,"RD3")
    if tier=="super": put(im,7,6,"WA3"); put(im,8,6,"WA2"); rect(im,6,2,9,3,"WA2"); rect(im,6,2,9,2,"WA3")
    outline(im,OC)
    if s>0:
        pa=[(2,6),(3,8),(13,6),(12,8),(4,2),(11,2),(1,10),(14,10)] if s==1 else [(3,5),(2,9),(12,5),(13,9),(5,1),(10,1),(1,7),(14,7)]
        n={"basic":4,"quality":6,"super":8}[tier]
        for x,y in pa[:n]: put(im,x,y,"WA3"); 
        for x,y in pa[:n:2]: put(im,x,y,"WA4")
    return im

if __name__=="__main__":
    B={"bld_house":house(),"bld_barn":barn(),"bld_coop":coop(),"bld_cowbarn":cowbarn()}
    for k,v in B.items(): v.save(f"{HERE}/Buildings/{k}.png")
    sheet([chest(False),chest(True)],2,16,16).save(f"{HERE}/Machines/chest_sheet.png")
    open(f"{HERE}/Machines/chest_sheet.names.txt","w").write("#cell=16x16 pivot=bottom\nobj_chest_closed\nobj_chest_open\n")
    st=["idle","work_a","work_b","ready"]; ms=[]; names=[]
    for nm,fn in(("dairy",dairy),("jam",jam),("oven",oven)):
        for i,s in enumerate(st): ms.append(fn(i)); names.append(f"machine_{nm}_{s}")
    sheet(ms,4,16,16).save(f"{HERE}/Machines/machines_sheet.png"); open(f"{HERE}/Machines/machines_sheet.names.txt","w").write("#cell=16x16 pivot=bottom\n"+"\n".join(names)+"\n")
    sheet([crafting(i) for i in range(4)],4,32,16).save(f"{HERE}/Machines/crafting_table_sheet.png")
    open(f"{HERE}/Machines/crafting_table_sheet.names.txt","w").write("#cell=32x16 pivot=bottom\n"+"\n".join(f"machine_crafting_table_{s}" for s in st)+"\n")
    sp=[];sn=[]
    for t in("basic","quality","super"):
        for i,s in enumerate(("idle","active_a","active_b")): sp.append(sprinkler(t,i)); sn.append(f"machine_sprinkler_{t}_{s}")
    sheet(sp,3,16,16).save(f"{HERE}/Machines/sprinklers_sheet.png"); open(f"{HERE}/Machines/sprinklers_sheet.names.txt","w").write("#cell=16x16 pivot=bottom\n"+"\n".join(sn)+"\n")
    # data
    rows=[("house","bld_house",80,64,5,4,"bottom_center",2,0,76,28,2,1,"Cửa ở giữa; điểm vào ô phía dưới cửa"),
          ("barn","bld_barn",64,48,4,3,"bottom_center",2,0,60,28,1,2,"Nhà kho; cửa đôi rộng 2 ô"),
          ("coop","bld_coop",32,32,2,2,"bottom_center",2,0,28,16,0,2,"Chuồng gà; lối vào rộng 2 ô"),
          ("cowbarn","bld_cowbarn",48,48,3,3,"bottom_center",2,0,44,28,1,1,"Chuồng bò; lối vào ở giữa"),
          ("chest","obj_chest_closed",16,16,1,1,"bottom_center",2,0,12,10,0,1,"Rương 2 trạng thái"),
          ("dairy","machine_dairy_idle",16,16,1,1,"bottom_center",2,0,12,10,0,1,"Máy sữa: idle/work_a/work_b/ready"),
          ("jam","machine_jam_idle",16,16,1,1,"bottom_center",2,0,12,10,0,1,"Máy làm mứt"),
          ("oven","machine_oven_idle",16,16,1,1,"bottom_center",2,0,12,10,0,1,"Lò nướng"),
          ("crafting_table","machine_crafting_table_idle",32,16,2,1,"bottom_center",2,0,28,10,0,1,"Bàn chế tạo 2x1"),
          ("sprinkler_basic","machine_sprinkler_basic_idle",16,16,1,1,"bottom_center",6,0,4,4,0,0,"Tưới ô lân cận; không chặn đi lại (trigger)"),
          ("sprinkler_quality","machine_sprinkler_quality_idle",16,16,1,1,"bottom_center",6,0,4,4,0,0,"Tưới vùng rộng hơn"),
          ("sprinkler_super","machine_sprinkler_super_idle",16,16,1,1,"bottom_center",6,0,4,4,0,0,"Tưới vùng lớn nhất")]
    with open(f"{HERE}/Unity/buildings.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow("id,sprite,px_w,px_h,tiles_w,tiles_h,pivot,collider_x,collider_y,collider_w,collider_h,entry_tile_x,entry_tile_w,notes".split(","))
        w.writerows(rows)
    # previews (footprint overlay)
    items=[("bld_house",B["bld_house"],rows[0]),("bld_barn",B["bld_barn"],rows[1]),("bld_cowbarn",B["bld_cowbarn"],rows[3]),("bld_coop",B["bld_coop"],rows[2])]
    W=sum(i[1].width+16 for i in items)+16; H=80+16
    pv=Image.new("RGBA",(W,H),C["GR2"]); x=8
    for n,im,r in items:
        y0=H-8-im.height
        pv.alpha_composite(im,(x,y0))
        ov=Image.new("RGBA",pv.size,(0,0,0,0))
        for gx in range(0,im.width+1,16):
            for yy in range(im.height): 
                if y0+yy>=0: ov.putpixel((x+min(gx,im.width-1),y0+yy),(255,255,255,70))
        for gy in range(0,im.height+1,16):
            for xx in range(im.width): ov.putpixel((x+xx,y0+im.height-1-min(gy,im.height-1)),(255,255,255,70)) if y0+im.height-1-gy>=0 else None
        cx,cy,cw,ch=r[7],r[8],r[9],r[10]
        for xx in range(cx,cx+cw):
            for yy in range(ch): ov.putpixel((x+xx,y0+im.height-1-cy-yy),(255,40,40,90))
        ex=r[11]
        for xx in range(ex*16,(ex+r[12])*16):
            for yy in range(3): 
                if y0+im.height+yy<H: ov.putpixel((x+xx,y0+im.height+yy),(60,160,255,200))
        pv=Image.alpha_composite(pv,ov); x+=im.width+16
    pv.resize((pv.width*3,pv.height*3),Image.NEAREST).save(f"{HERE}/Preview/footprints_x3.png")
    # machine preview
    G=new(16*4+4*8+8,16*3+16*3+60+24); rect(G,0,0,G.width-1,G.height-1,"GR2")
    y=4
    for r in range(3):
        for c in range(4): G.alpha_composite(ms[r*4+c],(4+c*20,y))
        y+=20
    for c in range(4): G.alpha_composite(crafting(c),(4,y)) if False else None
    for r in range(3):
        for c in range(3): G.alpha_composite(sp[r*3+c],(4+c*20,y))
        G.alpha_composite(chest(r%2==1),(4+3*20,y)) if r<2 else None
        y+=20
    ct=new(4*34+4,20); rect(ct,0,0,ct.width-1,19,"GR2")
    for c in range(4): ct.alpha_composite(crafting(c),(2+c*34,2))
    full=new(max(G.width,ct.width),G.height+22); full.alpha_composite(G,(0,0)); full.alpha_composite(ct,(0,G.height+2))
    full.resize((full.width*5,full.height*5),Image.NEAREST).save(f"{HERE}/Preview/machines_x5.png")
    bad=[f for d in("Buildings","Machines") for f in os.listdir(f"{HERE}/{d}") if f.endswith(".png") and offpalette(f"{HERE}/{d}/{f}")]
    print("offpalette:",bad or "none")
