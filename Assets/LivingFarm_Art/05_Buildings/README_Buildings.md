# Living Farm — Giai đoạn 5a: Công trình, máy móc

Sinh bằng `gen_buildings.py` (Pillow, bảng màu 43 màu, đã kiểm tra không có pixel bán trong suốt).
Cùng phong cách top-down 3/4, viền ngoài `SO0`, ánh sáng từ trên-trái.

## File
| File | Kích thước | Footprint | Ghi chú |
|---|---|---|---|
| `Buildings/bld_house.png` | 80x64 | 5x4 tile | Nhà chính: mái đỏ, ống khói, 2 cửa sổ, cửa chính |
| `Buildings/bld_barn.png` | 64x48 | 4x3 | Nhà kho đỏ, cửa đôi chữ X, cửa gác mái |
| `Buildings/bld_coop.png` | 32x32 | 2x2 | Chuồng gà, mái cam, dốc chui, hộp ổ trứng |
| `Buildings/bld_cowbarn.png` | 48x48 | 3x3 | Chuồng bò, mái xanh, cửa vòm có rơm |
| `Machines/chest_sheet.png` | 32x16 | 1x1 | Rương: closed, open |
| `Machines/machines_sheet.png` | 64x48 (4x3, ô 16) | 1x1 | Hàng: máy sữa, máy mứt, lò nướng. Cột: idle, work_a, work_b, ready |
| `Machines/crafting_table_sheet.png` | 128x16 (ô 32x16) | 2x1 | Bàn chế tạo: idle, work_a, work_b, ready |
| `Machines/sprinklers_sheet.png` | 48x48 (3x3, ô 16) | 1x1 | 3 cấp (basic, quality, super) x (idle, active_a, active_b) |
| `Unity/buildings.csv` | | | Footprint, collider, lối vào |
| `Preview/` | | | `footprints_x3` (lưới tile, collider đỏ, lối vào xanh), `machines_x5` |

## Footprint và collider
Pivot **Bottom Center**. Collider (px, gốc góc trái-dưới sprite) lấy từ `buildings.csv`: chỉ phủ phần thân tường, **không** phủ mái, để nhân vật đi được "phía sau" mái. Lối vào là các ô ngay dưới đáy công trình (`entry_tile_x`, `entry_tile_w`). Ví dụ nhà chính: 5x4 tile, collider 76x28 px, cửa ở ô số 2.

## Import
1. Chép vào `Assets/Art/Buildings`, `Assets/Art/Machines`. Sheet cắt bằng Slicer (names.txt đã có `#cell=` và `pivot=bottom`); `bld_*.png` để Sprite Single, pivot Bottom Center, PPU 16, Point, Compression None.
2. Tạo prefab: SpriteRenderer + BoxCollider2D (theo CSV, đổi px sang unit = px/16) + (máy) `MachineAnimator` gán 4 sprite.
3. `BuildingData` (ScriptableObject) lưu sprite, footprint, collider, lối vào, chi phí xây (đặt tại `Assets/Data/Buildings`). `OccupiedCells()` trả về các ô bị chiếm để làm hệ thống đặt công trình.
4. Máy tưới: dùng trigger Collider2D thay vì chặn đi lại; hiệu ứng nước là frame `active_a/active_b` tạm (hiệu ứng đầy đủ ở Giai đoạn 6).
5. Sorting: Custom Axis (0,1,0); Sorting Point = Pivot.

## Hạn chế
- Chưa có biến thể ban đêm (cửa sổ sáng đèn); dùng Light 2D/Emission ở Unity hoặc bổ sung ở Giai đoạn 6.
- Mỗi công trình chỉ có 1 cấp độ (chưa có bản nâng cấp).
- Máy sữa/mứt/lò là biểu tượng đơn giản; trạng thái "ready" nên kết hợp icon `alert` (UI) phía trên.
- Script C# chưa chạy thử trong Unity.
