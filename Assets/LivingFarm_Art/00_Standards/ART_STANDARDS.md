# Living Farm — Art Standards (Giai đoạn 1)

## 1. Quyết định kỹ thuật cốt lõi

| Hạng mục | Quyết định | Lý do |
|---|---|---|
| Tile chuẩn | **16x16 px** | Nhẹ công sức, dễ nhất quán, chuẩn phổ biến cho farming sim |
| Pixels Per Unit | **16** | 1 tile = 1 Unity unit |
| Góc nhìn | Top-down hơi nghiêng (3/4), vật thể đứng thấy mặt trước | Dễ đọc, sort theo Y |
| Reference resolution | **480x270** (30x16.875 tile) | Scale nguyên x4 ở 1080p, x8 ở 4K; 1440p dùng x5 kèm viền |
| Viền (outline) | Viền tối **1 px**, selective (màu đậm của chính vật thể, không dùng đen thuần) | Silhouette rõ ở kích thước nhỏ |
| Hướng sáng | **Trên-trái**; bóng đổ xuống dưới-phải | Cố định toàn game |
| Anti-aliasing | **Cấm** | Pixel art thuần |
| Dithering | Hạn chế, chỉ dùng trên tile nền (cỏ, nước) | Tránh nhiễu |
| Sprite sheet | Lưới đều, không padding giữa ô, kích thước sheet là bội số frame | Dễ slice bằng Grid By Cell Size |

## 2. Kích thước sprite

| Nhóm | Frame | Ghi chú |
|---|---|---|
| Tile môi trường | 16x16 | Autotile dùng bố cục Rule Tile 47 hoặc 16-mask |
| Cây trồng | 16x16 (cây cao như bắp: 16x32) | 5 stage / cây |
| Vật phẩm / icon inventory | 16x16 | Silhouette chiếm ≥ 10px |
| Gà, vịt | 16x16 | |
| Cừu, bò | 32x32 (2x2 tile) | |
| Player, NPC | **16x32** | Chân nằm đáy frame, pivot Bottom Center |
| Công trình | Bội số 16 (vd. nhà 64x64, chuồng gà 32x32) | Footprint tính theo tile |
| Hiệu ứng | 16x16 hoặc 32x32 | |
| UI | 9-slice, góc 4–6 px, bội số 2 | Không chứa chữ |

## 3. Bảng màu — 43 màu (`LivingFarm.hex / .gpl / palette PNG`)

Mỗi "ramp" xếp từ tối → sáng. Chỉ dùng màu trong bảng này.

| Ramp | Mã | Dùng cho |
|---|---|---|
| Outline | OL0 | Viền ngoài, khe tối nhất |
| Grass | GR0–GR4 | Cỏ, lá, cây trồng |
| Soil | SO0–SO4 | Đất; SO0–SO1 = đất đã tưới/cày sâu |
| Wood | WD0–WD3 | Gỗ, hàng rào, thùng, cán công cụ |
| Water | WA0–WA4 | Nước, giọt tưới, mưa; WA4 = bọt/highlight |
| Stone | ST0–ST4 | Đá, đường lát, kim loại, máy móc |
| Sun | SU0–SU4 | Lúa mì, bắp, bí, ánh sáng, xu |
| Red | RD0–RD3 | Cà chua, dâu, mái nhà, nút cảnh báo |
| Skin | SK0–SK3 | Da nhân vật, động vật |
| Accent | AC0–AC2 | Hoa, quả mọng, váy áo dân làng |
| Cream | CR0–CR1 | Len, trứng, trắng ấm, panel UI sáng |

### Quy tắc dùng màu
- **Tối/bóng:** bước xuống 1 mức trong cùng ramp; bóng đổ xuống đất dùng GR0/SO1 (không dùng đen).
- **Highlight:** bước lên 1 mức, chỉ ở cạnh trên-trái, tối đa 1–2 px.
- **Viền:** dùng màu ramp tối nhất của chính vật thể (vd. cà chua viền RD0); OL0 chỉ cho viền nhân vật và vật thể trung tính.
- Mỗi sprite tối đa **4–5 màu chính + viền**.
- Tương phản: cây trồng phải tách khỏi đất (GR2–GR3 trên SO2–SO3). Không đặt màu cùng độ sáng cạnh nhau cho vật thể cần tương tác.
- Hiệu ứng ngày/đêm/mưa làm bằng Light 2D + Color Grading, **không** vẽ lại sprite.

## 4. Quy tắc đặt tên

```
<nhóm>_<đối tượng>_<biến thể>_<trạng thái>_<hướng>_<frame>.png
env_grass_a.png            crop_tomato_stage3.png
item_egg.png               player_walk_down_00.png
anim_cow_eat_left_03.png   fx_water_splash_02.png
```
Chữ thường, snake_case, frame 2 chữ số, hướng: `up/down/left/right`.
Cây trồng stage: `seed(0) / sprout(1) / growing(2) / mature(3) / ready(4)`, thêm `_wilted`.

## 5. Cấu trúc thư mục

```
Assets/Art/{Environment,Crops,Items,Characters,Animals,Buildings,UI,FX}/
Assets/Art/Palette/
Assets/Data/{Crops,Items,Animals}/   (ScriptableObject — tách khỏi art)
```

## 6. Cài đặt import Unity (áp dụng toàn bộ pixel art)

| Thiết lập | Giá trị |
|---|---|
| Texture Type | Sprite (2D and UI) |
| Sprite Mode | Multiple (sheet) / Single (icon lẻ) |
| Pixels Per Unit | 16 |
| Mesh Type | Tight (Full Rect cho tile) |
| Filter Mode | **Point (no filter)** |
| Compression | **None** (hoặc Normal Quality nếu cần giảm dung lượng, kiểm tra méo màu) |
| Generate Mip Maps | Tắt |
| Max Size | ≥ kích thước sheet |
| Pivot | Tile: Center · Nhân vật/động vật/công trình: Bottom Center |
| Sprite Atlas | Mỗi nhóm 1 atlas, Filter Point, Tight Packing tắt cho tile, padding 2–4 px |

Project Settings: Pixel Perfect Camera (URP 2D) — Assets PPU 16, Reference 480x270, Crop Frame None, Upscale Render Texture bật. Transparency Sort Mode = Custom Axis (0, 1, 0).

Animation: 8–10 fps cho walk/idle động vật, 6–8 fps cho idle, 12 fps cho dụng cụ/hiệu ứng.

## 7. Bộ asset tối thiểu cho demo chơi được (MVP)

| Nhóm | Danh sách tối thiểu |
|---|---|
| Environment | Cỏ (3 biến thể), đất, đất cày, đất tưới, đường đất, nước + bờ (autotile), hàng rào, 1 cây, 1 đá, 1 gốc cây |
| Crops | **3 loại**: cà rốt, lúa mì, cà chua (5 stage mỗi loại) + 3 vật phẩm thu hoạch |
| Items/Tools | Cuốc, bình tưới, rìu, hạt giống (1 icon chung + tint), gỗ, đá, trứng, sữa |
| Player | 1 nhân vật: idle, walk (4 hướng), cuốc, tưới, thu hoạch |
| Animals | Gà (idle, walk, ăn) làm mẫu; bò ở bản mở rộng |
| NPC | 1 NPC mẫu (idle, walk) |
| Buildings | Nhà chính, rương, chuồng gà, 1 máy chế biến |
| UI | Hotbar, inventory slot, khung thoại, thanh tiền/thời gian, nút, panel 9-slice |
| FX | Nước tưới, bụi đất, xu, mưa |

Mở rộng sau MVP: 4 loại cây còn lại, bò/cừu/vịt, NPC còn lại, máy chế biến, màn tổng kết, decor.

## 8. Việc cần kiểm tra
- Xác minh giấy phép nếu dùng công cụ/mô hình AI hoặc asset ngoài.
- Test palette trên nền sáng và tối trước khi vẽ hàng loạt.
- Chốt Pixel Perfect Camera trước khi import asset.
