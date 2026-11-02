from PIL import Image, ImageDraw
P = [
("outline","OL","1b1b2a",["1b1b2a"]),
("grass","GR",None,["2d5a3a","3f7d45","5ea34f","8cc65a","c4e48a"]),
("soil","SO",None,["2c1d1a","3a2620","5b3b2c","7c553b","a67c52"]),
("wood","WD",None,["5a3a22","8a5a33","b7814a","dba76a"]),
("water","WA",None,["1d3f6e","2f6db3","4d9be0","8ecff0","e3f6fb"]),
("stone","ST",None,["3d4150","636a7a","8d94a3","b9bfc9","e1e4ea"]),
("sun","SU",None,["b85c1e","e8872c","f7b844","fbe07a","fff3b8"]),
("red","RD",None,["7a1f2b","b5333a","e2574c","f58f7c"]),
("skin","SK",None,["8a5a44","c98b66","f0b894","ffd9b8"]),
("accent","AC",None,["5a3a6b","8a5fa0","e78aa8"]),
("cream","CR",None,["f4ecd8","fffaf0"]),
]
cols=[]
for n,c,_,l in P:
    for i,h in enumerate(l): cols.append((f"{c}{i}",n,h))
open("LivingFarm.hex","w").write("\n".join(h for _,_,h in cols)+"\n")
with open("LivingFarm.gpl","w") as f:
    f.write("GIMP Palette\nName: LivingFarm\nColumns: 8\n#\n")
    for k,n,h in cols:
        r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
        f.write(f"{r:3d} {g:3d} {b:3d}\t{k} ({n})\n")
# swatch 1px-per-cell strip (importable palette) + preview
Image.new("RGBA",(len(cols),1)).putdata([tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,) for _,_,h in cols])
s=Image.new("RGBA",(len(cols),1)); s.putdata([tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,) for _,_,h in cols]); s.save("LivingFarm_palette_1px.png")
W=8; rows=(len(cols)+W-1)//W; cell=32
im=Image.new("RGBA",(W*cell,rows*cell),(0,0,0,0)); d=ImageDraw.Draw(im)
for i,(k,n,h) in enumerate(cols):
    x,y=(i%W)*cell,(i//W)*cell
    d.rectangle([x,y,x+cell-1,y+cell-1],fill="#"+h)
im.save("LivingFarm_palette_preview.png")
print(len(cols),"colors", im.size, s.size)
