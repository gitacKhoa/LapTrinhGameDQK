# Living Farm — Giai đoạn 2: Environment

Tất cả PNG sinh bằng `gen_environment.py` (Python + Pillow), chỉ dùng 43 màu của `00_Standards`, không có pixel bán trong suốt (đã kiểm tra tự động).
Chạy lại: `python3 gen_environment.py` (tạo sẵn các thư mục Tiles/Objects/Preview).

## Danh sách file

| File | Kích thước | Nội dung |
|---|---|---|
| `Tiles/tiles_ground.png` | 64x48 (4x3 ô 16px) | grass a–d, dirt a–b, tilled, tilled_wet, path_dirt a–b, path_stone a–b |
| `Tiles/tiles_water_16mask.png` | 256x64 (16x4) | Nước + bờ, 16 mask x 4 frame animation (hàng = frame) |
| `Tiles/tiles_fence_16mask.png` | 256x16 (16x1) | Hàng rào 16 mask |
| `Objects/objects_16.png` | 208x16 (13x1) | rock_small, stump, bush, bush_berry, tuft, 3 hoa, sign, gate_closed, gate_open, bridge_h, bridge_v |
| `Objects/obj_tree_a/b.png` | 32x48 | Cây (pivot gốc cây) |
| `Objects/obj_rock_large.png` | 32x32 | Đá lớn |
| `Objects/obj_*.png` | 16x16 | Bản lẻ của từng vật thể trong objects_16 |
| `*.names.txt` | | Tên sprite theo thứ tự ô, dùng cho script cắt |
| `Preview/` | | Cảnh thử 480x272 (+x3), kiểm tra nền sáng/tối |
| `Unity/LivingFarmSpriteSlicer.cs` | | Editor tool cắt sheet theo names.txt |

## Quy ước mask (water, fence)
Index = N(1) + E(2) + S(4) + W(8). Bit = 1 nghĩa là:
- **Water:** ô hướng đó **không phải nước** (đất liền). Mask 0 = nước mở, 15 = ao 1 ô.
- **Fence:** ô hướng đó **có hàng rào** nối vào.

Hạn chế: mask 4 hướng không xử lý góc chỉ-chéo. Hãy vẽ hồ dạng **hình chữ nhật hoặc đa giác không có bậc thang chéo**; nếu cần hồ tròn mềm, cần bổ sung bộ 47 tile (giai đoạn sau).
Animation nước: 4 frame, gợi ý 4 fps, dùng Animated Tile (2D Tilemap Extras) hoặc chỉ dùng frame 0 (hàng đầu).

## Import vào Unity
1. Chép các thư mục vào `Assets/Art/Environment/`, bảng màu vào `Assets/Art/Palette/`.
2. Chép `LivingFarmSpriteSlicer.cs` vào `Assets/Editor/`.
3. Chọn 3 sheet trong `Tiles/` và `objects_16.png` → chuột phải → **Living Farm > Slice Sheet (names.txt)**. Tool tự đặt Sprite Multiple, PPU 16, Point, không nén, và đặt tên sprite theo names.txt. *(Chưa chạy thử trong Unity; nếu lỗi API, dùng cách thủ công bên dưới.)*
   - Thủ công: Sprite Mode Multiple → Sprite Editor → Slice → Grid By Cell Size 16x16.
4. Sprite lẻ trong `Objects/` (cây, đá lớn): Sprite Mode Single, PPU 16, Point, Compression None. **Pivot cây: Bottom Center; đá lớn: Bottom Center.**

| Thiết lập | Giá trị |
|---|---|
| Pixels Per Unit | 16 |
| Filter Mode | Point (no filter) |
| Compression | None |
| Mesh Type | Full Rect cho tile |
| Sprite Atlas | `Atlas_Environment` (tile) và `Atlas_Objects`; Filter Point, padding 2–4, Allow Rotation tắt |

## Tile Palette và Tilemap
Tạo Grid với các Tilemap layer (Order in Layer tăng dần):
1. `Water` (mask water) → 2. `Ground` (grass/dirt/path) → 3. `Soil` (tilled, tilled_wet) → 4. `Fence` → 5. `Objects` (Tilemap Renderer, Mode: **Individual**, hoặc đặt object bằng Prefab).

- Tạo Tile Palette (Window > 2D > Tile Palette), kéo từng sprite vào để tạo Tile.
- **Grass:** tạo Rule Tile (hoặc Random Tile) từ grass a–d với trọng số a=50%, b/c/d≈17% để giảm lặp.
- **Water / Fence:** tạo Rule Tile; mỗi quy tắc gán 1 trong 16 mask theo quy ước phía trên (water: "This" = đất liền, "Not This" = nước).
- **Collider:** thêm `Tilemap Collider 2D` (+ Composite Collider 2D, Rigidbody2D Static) cho layer `Water` (chặn đi bộ, trừ ô cầu) và `Fence`. `Ground` và `Soil` không cần collider.
- **Sắp xếp theo Y:** Project Settings > Graphics > Transparency Sort Mode = Custom Axis (0,1,0).

## Footprint và collider gợi ý
| Vật thể | Chiếm (tile) | Collider (px, từ pivot) | Pivot |
|---|---|---|---|
| Cây | 1x1 | Box 6x4 tại gốc | Bottom Center |
| Đá nhỏ / gốc cây | 1x1 | Box 12x8 | Center |
| Đá lớn | 2x1 | Box 24x10 | Bottom Center |
| Bụi cây | 1x1 | Box 12x8 | Center |
| Hàng rào | 1x1 | Box 16x6 ở giữa ô | Center |
| Cổng đóng | 1x1 | Box 16x6; tắt collider khi mở | Center |
| Tuft/hoa | 1x1 | Không | Center |
| Biển báo | 1x1 | Box 4x4 gốc cột | Bottom Center |

Đây là gợi ý ban đầu, cần chỉnh khi thử với nhân vật.

## Việc cần kiểm tra / hạn chế đã biết
- Chưa có bóng đổ dưới vật thể (để tránh pixel bán trong suốt); nên thêm sprite bóng riêng ở Giai đoạn 6.
- `obj_gate_open` và `obj_stump` còn đơn giản, có thể tinh chỉnh.
- Hoa trắng hơi yếu trên nền sáng.
- Tile `tilled` chưa có biến thể rìa (viền đất cày giáp cỏ); nên thêm nếu muốn ruộng có bo viền.
- Chưa kiểm thử import trong Unity.
