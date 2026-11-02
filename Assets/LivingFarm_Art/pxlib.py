"""Thư viện vẽ pixel dùng chung cho Living Farm (bảng màu 43 màu)."""
from PIL import Image
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
def line_pts(x0,y0,x1,y1):
    pts=[]; dx,dy=abs(x1-x0),-abs(y1-y0); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1; e=dx+dy
    while True:
        pts.append((x0,y0))
        if (x0,y0)==(x1,y1): break
        e2=2*e
        if e2>=dy: e+=dy; x0+=sx
        if e2<=dx: e+=dx; y0+=sy
    return pts
def line(im,x0,y0,x1,y1,c):
    for x,y in line_pts(x0,y0,x1,y1): put(im,x,y,c)
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
def sheet(imgs,cols,cw,ch):
    rows=(len(imgs)+cols-1)//cols; sh=new(cols*cw,rows*ch)
    for i,im in enumerate(imgs):
        if im is not None: sh.paste(im,((i%cols)*cw,(i//cols)*ch))
    return sh
def offpalette(path):
    im=Image.open(path).convert("RGBA")
    return any(p[3] not in(0,255) or (p[3]==255 and p not in PAL) for p in im.getdata())
