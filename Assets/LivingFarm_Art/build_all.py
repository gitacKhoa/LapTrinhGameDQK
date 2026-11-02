"""Sinh lại TOÀN BỘ asset theo thứ tự phụ thuộc, chạy QA và đóng gói. Chạy: python3 build_all.py  (cần Pillow)"""
import subprocess, sys, os, shutil
ROOT=os.path.dirname(os.path.abspath(__file__))
STEPS=["00_Standards/gen_palette.py","01_Environment/gen_environment.py","02_Crops_Items/gen_crops_items.py","03_Characters/gen_characters.py",
       "04_Animals/gen_animals.py","05_Buildings/gen_buildings.py","06_UI/gen_ui.py","07_Effects/gen_effects.py","qa_check.py"]
for s in STEPS:
    p=os.path.join(ROOT,s); print(">>",s)
    r=subprocess.run([sys.executable,"-W","ignore",p],cwd=os.path.dirname(p)); 
    if r.returncode: sys.exit(f"Lỗi ở {s}")
# gói chỉ ảnh
OUT=os.path.join(ROOT,"..","LivingFarm_Assets")
if os.path.isdir(OUT): shutil.rmtree(OUT)
MAP={"Palette":["00_Standards"],"Environment/Tiles":["01_Environment/Tiles"],"Environment/Objects":["01_Environment/Objects"],"Crops":["02_Crops_Items/Crops"],"Items":["02_Crops_Items/Items"],
     "Characters/Player":["03_Characters/Player"],"Characters/NPC":["03_Characters/NPC"],"Animals":["04_Animals/Sheets"],"Buildings":["05_Buildings/Buildings"],
     "Machines":["05_Buildings/Machines"],"UI/Sprites":["06_UI/Sprites"],"UI/Icons":["06_UI/Icons"],"Effects":["07_Effects/Sheets"],"Emotes":["07_Effects/Emotes"],"Shadows":["07_Effects/Shadows"],
     "Previews":["01_Environment/Preview","02_Crops_Items/Preview","03_Characters/Preview","04_Animals/Preview","05_Buildings/Preview","06_UI/Preview","07_Effects/Preview","QA"]}
for dst,srcs in MAP.items():
    os.makedirs(os.path.join(OUT,dst),exist_ok=True)
    for s in srcs:
        for f in os.listdir(os.path.join(ROOT,s)):
            if f.endswith(".png"): shutil.copy(os.path.join(ROOT,s,f),os.path.join(OUT,dst,f))
shutil.make_archive(os.path.join(ROOT,"..","LivingFarm_Assets"),"zip",OUT)
print("Xong: LivingFarm_Assets/ và LivingFarm_Assets.zip")
