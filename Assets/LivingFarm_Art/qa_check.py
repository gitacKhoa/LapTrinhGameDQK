"""Kiểm thử chất lượng toàn bộ asset Living Farm. Chạy: python3 qa_check.py  -> QA_REPORT.md + QA/contact_light_dark.png"""
import os, re, sys, collections
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pxlib import C, PAL, new, rect
ROOT=os.path.dirname(os.path.abspath(__file__))
SEMI_OK={"Shadows"}                     # bóng đổ được phép bán trong suốt (alpha 96)
pngs=[os.path.join(d,f) for d,_,fs in os.walk(ROOT) for f in fs if f.endswith(".png")]
rel=lambda p:os.path.relpath(p,ROOT)
def lum(p): return .299*p[0]+.587*p[1]+.114*p[2]
rep=[]; warn=[]; err=[]; used=collections.Counter()

# 1. palette + alpha
for p in pngs:
    if "Preview" in p or "/QA/" in p: continue
    im=Image.open(p).convert("RGBA"); semi=any(part in SEMI_OK for part in rel(p).split(os.sep))
    for px in im.getdata():
        if px[3]==0: continue
        if semi: continue
        if px[3]!=255: err.append(f"Pixel bán trong suốt: {rel(p)}"); break
        if px not in PAL: err.append(f"Màu ngoài bảng màu: {rel(p)} {px}"); break
        used[px]+=1
# 2. sheets vs names.txt
sheets=[]
for d,_,fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".names.txt"):
            png=os.path.join(d,f.replace(".names.txt",".png"))
            if not os.path.exists(png): err.append(f"names.txt không có PNG: {rel(os.path.join(d,f))}"); continue
            lines=open(os.path.join(d,f),encoding="utf-8").read().split("\n")
            m=re.match(r"#cell=(\d+)x(\d+)",lines[0])
            if m: cw,ch=int(m.group(1)),int(m.group(2)); names=lines[1:]
            else: cw=ch=16; names=lines   # sheet Giai đoạn 2 không có header: mặc định 16x16
            while names and names[-1]=="": names.pop()
            sheets.append((png,cw,ch,names))
nsheet=0; ncell=0; nframes=0
for png,cw,ch,names in sheets:
    im=Image.open(png).convert("RGBA"); nsheet+=1
    if im.width%cw or im.height%ch: err.append(f"Kích thước không chia hết ô {cw}x{ch}: {rel(png)} {im.size}"); continue
    cols,rows=im.width//cw,im.height//ch
    if len(names)>cols*rows: err.append(f"Số tên ({len(names)}) > số ô ({cols*rows}): {rel(png)}")
    dup=[n for n,c in collections.Counter([n for n in names if n]).items() if c>1]
    if dup: err.append(f"Tên trùng trong {rel(png)}: {dup[:3]}")
    ground="env_" in names[0] if names else False
    for i in range(cols*rows):
        cell=im.crop(((i%cols)*cw,(i//cols)*ch,(i%cols)*cw+cw,(i//cols)*ch+ch)); bb=cell.getbbox(); name=names[i] if i<len(names) else ""
        if name and bb is None: err.append(f"Ô rỗng nhưng có tên: {rel(png)} #{i} {name}")
        if not name and bb is not None: err.append(f"Ô có hình nhưng không có tên: {rel(png)} #{i}")
        if name and bb:
            ncell+=1
            if not ground and not name.startswith(("env_","crop_")) and not any(k in name for k in("bridge","gate","fence")) and not name.startswith("fx_"):
                # nghi bị cắt: pixel NỘI DUNG (không phải viền tối) nằm sát mép ô
                cut=set()
                for x in range(cw):
                    for y,side in((0,"trên"),(ch-1,"dưới")):
                        q=cell.getpixel((x,y))
                        if q[3] and lum(q)>=115: cut.add(side)
                for y in range(ch):
                    for x,side in((0,"trái"),(cw-1,"phải")):
                        q=cell.getpixel((x,y))
                        if q[3] and lum(q)>=115: cut.add(side)
                if cut: warn.append(f"Nội dung chạm viền ô ({'/'.join(sorted(cut))}), có thể bị cắt: {name} ({rel(png)})")
# 3. căn chân theo nhóm animation
groups=collections.defaultdict(list)
for png,cw,ch,names in sheets:
    if not any(k in png for k in("Player","NPC","Animals","Sheets/animal")) : continue
    im=Image.open(png).convert("RGBA"); cols=im.width//cw
    for i,n in enumerate(names):
        m=re.match(r"(.+)_(idle|walk|hoe|water|harvest|chop|mine|carry_idle|carry_walk|eat)_(down|up|left|right)_(\d+)$",n)
        if not m or m.group(2) in("hoe","water","chop","mine"): continue   # công cụ thò xuống dưới chân, không đo
        cell=im.crop(((i%cols)*cw,(i//cols)*ch,(i%cols)*cw+cw,(i//cols)*ch+ch)); bb=cell.getbbox()
        groups[(m.group(1),m.group(2),m.group(3))].append(bb[3])
bad_feet=[(k,max(v)-min(v)) for k,v in groups.items() if max(v)-min(v)>2]
for k,dv in bad_feet: warn.append(f"Chân lệch {dv}px giữa các frame: {'_'.join(k)}")
# 4. tương phản nền sáng/tối
LIGHT,DARK=lum(C["CR1"]),lum(C["OL0"]); lowc=[]
for p in pngs:
    r=rel(p)
    if not any(r.startswith(x) for x in("02_Crops_Items/Items","01_Environment/Objects","06_UI/Icons")) or "names" in p: continue
    im=Image.open(p).convert("RGBA"); px=[q for q in im.getdata() if q[3]]
    for bgn,bg in(("sáng",LIGHT),("tối",DARK)):
        low=sum(1 for q in px if abs(lum(q)-bg)<35)/len(px)
        if low>.6: lowc.append(f"{r} (nền {bgn}: {low:.0%} pixel tương phản thấp)")
for x in lowc: warn.append("Tương phản thấp: "+x)
# 5. bảng màu chưa dùng
unused=[k for k,v in C.items() if v not in used]
# 6. contact sheet sáng/tối
pick=["02_Crops_Items/Items/items_16.png","01_Environment/Objects/objects_16.png","06_UI/Icons/icons_16.png","05_Buildings/Machines/machines_sheet.png","07_Effects/Sheets/fx_sheet_16.png","07_Effects/Emotes/emote_sheet.png","04_Animals/Sheets/animal_cow_sheet.png","03_Characters/NPC/npc_baker_sheet.png","02_Crops_Items/Crops/crops_sheet.png"]
ims=[Image.open(os.path.join(ROOT,p)).convert("RGBA") for p in pick]
H=max(i.height for i in ims)+8; W=sum(i.width+8 for i in ims)+8
cs=Image.new("RGBA",(W,H*2),C["CR1"]); rect(cs,0,H,W-1,H*2-1,"OL0"); x=8
for im in ims:
    cs.alpha_composite(im,(x,4)); cs.alpha_composite(im,(x,H+4)); x+=im.width+8
os.makedirs(f"{ROOT}/QA",exist_ok=True); cs.save(f"{ROOT}/QA/contact_light_dark.png")
# report
out=["# Báo cáo QA — Living Farm","",f"- File PNG quét: **{len([p for p in pngs if 'Preview' not in p and '/QA/' not in p])}**",f"- Sheet có names.txt: **{nsheet}**, ô sprite có tên: **{ncell}**",
     f"- Lỗi: **{len(err)}** · Cảnh báo: **{len(warn)}**",f"- Màu bảng màu đã dùng: **{43-len(unused)}/43**"+(f" (chưa dùng: {', '.join(k for k in unused)})" if unused else ""),""]
out+=["## Lỗi",""]+([f"- {e}" for e in err] if err else ["Không có."])
out+=["","## Cảnh báo",""]+([f"- {w}" for w in warn[:80]] if warn else ["Không có."])
if len(warn)>80: out.append(f"- ... và {len(warn)-80} cảnh báo khác")
out+=["","## Kiểm tra đã chạy","","1. Mọi PNG (trừ Shadows) chỉ dùng 43 màu trong bảng màu, pixel alpha 0 hoặc 255.","2. Kích thước sheet chia hết cho ô; số tên ≤ số ô; không trùng tên; ô có tên không rỗng; ô không tên rỗng.",
 "3. Sprite (nhân vật/vật thể/máy/vật phẩm/emote) không có nội dung sáng màu chạm viền ô (nguy cơ bị cắt). Hiệu ứng hạt `fx_*` được loại trừ vì hạt bay ra mép là chủ ý; cầu/cổng/hàng rào chủ ý liền mạch giữa các ô.","4. Chân nhân vật/động vật giữa các frame của cùng animation lệch ≤ 2 px (bỏ qua animation có công cụ).","5. Vật phẩm/vật thể/icon có đủ tương phản trên nền sáng (`CR1`) và tối (`OL0`).","6. `QA/contact_light_dark.png`: ảnh tổng hợp để kiểm tra mắt."]
open(f"{ROOT}/QA_REPORT.md","w",encoding="utf-8").write("\n".join(out)+"\n")
print("errors",len(err),"warnings",len(warn),"sheets",nsheet,"cells",ncell,"unused colors",unused)
for e in err[:15]: print("ERR",e)
for w in warn[:25]: print("WARN",w)
