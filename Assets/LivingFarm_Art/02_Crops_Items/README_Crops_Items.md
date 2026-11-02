# Living Farm — Giai đoạn 3: Cây trồng, vật phẩm, công cụ

Sinh bằng `gen_crops_items.py` (Pillow). Đúng 43 màu của bảng màu, không pixel bán trong suốt (đã kiểm tra tự động).

## File
| File | Kích thước | Nội dung |
|---|---|---|
| `Crops/crops_sheet.png` | 96x224 (6 cột x 7 hàng, ô **16x32**) | 7 cây x [seed, sprout, growing, mature, ready, wilted] |
| `Crops/crop_<cây>_<giai đoạn>.png` | 16x32 | Bản lẻ (42 file) |
| `Items/items_16.png` | 128x64 (8x4 ô 16x16) | 32 vật phẩm |
| `Items/<tên>.png` | 16x16 | Bản lẻ (32 file) |
| `*.names.txt` | | Tên sprite theo thứ tự ô; dòng đầu `#cell=WxH pivot=...` |
| `Data/items.csv`, `Data/crops.csv` | | Dữ liệu gameplay **mẫu** (giá, số ngày... cần cân bằng lại) |
| `Unity/*.cs` | | ItemData, CropData, AnimalData, Slicer (bản mới), DataImporter |
| `Preview/` | | `crops_preview_x4.png`, `items_check_x5.png` (nền sáng + tối) |

Thứ tự hàng của crops_sheet: wheat, carrot, potato, tomato, strawberry, pumpkin, corn.
Thứ tự items_16: 7 hạt giống → 7 nông sản → hoe, watering_can, axe, hammer, pickaxe → wood, stone, ore_copper → milk, egg, wool → fertilizer, plank, fiber, coal → bread, jam, cheese.

## Quy ước sprite cây trồng
- Ô 16x32, **pivot Bottom Center**; cạnh dưới ô = cạnh dưới ô đất. Cây mọc từ y=27 (cách đáy 5px), nửa dưới 16px nằm trên ô đất, phần cây cao (bắp) vươn lên ô phía trên.
- Đặt GameObject cây tại **giữa cạnh dưới** của ô đất. Sorting theo Y.
- Chỉ số giai đoạn: 0 seed, 1 sprout, 2 growing, 3 mature, 4 ready. `wilted` dùng khi thiếu nước / thời tiết xấu.
- Giai đoạn `sprout` dùng chung hình cho cả 7 loại (cố ý, để tiết kiệm; có thể vẽ riêng sau).
- Sprite hạt giống (stage 0) rất nhỏ; hãy xem thử trên ruộng thật.

## Import vào Unity
1. Chép `Crops/`, `Items/` vào `Assets/Art/Crops`, `Assets/Art/Items`; chép `Unity/*.cs` vào `Assets/Scripts/Data/` (ItemData, CropData, AnimalData) và `Assets/Editor/` (Slicer, DataImporter); chép `Data/*.csv` vào `Assets/Data/Source/`.
2. Chọn `crops_sheet.png` và `items_16.png` → chuột phải → **Living Farm > Slice Sheet (names.txt)**. Tool đọc dòng `#cell=` nên tự đặt ô 16x32/pivot bottom cho cây.
   - Thủ công: Multiple → Sprite Editor → Grid By Cell Size (16x32 cho cây, 16x16 cho vật phẩm); pivot Bottom Center cho cây.
3. Menu **Tools > Living Farm > Create Data Assets From CSV** tạo `ItemData` và `CropData` trong `Assets/Data/Items|Crops`, tự gán sprite. Chạy lại để cập nhật khi sửa CSV.
4. Ví dụ dùng: `sr.sprite = crop.GetSprite(daysGrown, isWilted);`

| Thiết lập | Giá trị |
|---|---|
| PPU / Filter / Compression | 16 / Point / None |
| Sprite Atlas | `Atlas_Crops`, `Atlas_Items` (padding 2–4, Allow Rotation tắt) |
| Pivot | Cây: Bottom Center · Vật phẩm: Center |

## Tách visual và dữ liệu
PNG chỉ chứa hình. Giá bán, số ngày sinh trưởng, mùa vụ nằm trong CSV/ScriptableObject. `daysPerStage` có 4 số (ngày ở stage 0–3), sau đó cây ở trạng thái `ready`.

## Việc cần kiểm tra / hạn chế
- Script C# (`Slicer`, `DataImporter`) chưa chạy thử trong Unity 6000.3.11f1; nếu lỗi API, dùng cách cắt thủ công và tạo asset bằng menu Create.
- Chưa có icon hạt giống dạng từng loại cây (hiện là gói giấy khác màu viền).
- Cây héo là bản đổi màu của stage `mature`; chưa có biến thể "bị ảnh hưởng bởi thời tiết" khác (sương giá, ngập).
- Sprite sheet cây tính cho ô 16x32 nên nhiều ô trống phía trên; chấp nhận để đồng bộ.
- Cà chua/dâu "ready" nên được kiểm tra độ nhìn rõ ở zoom thật của game.
