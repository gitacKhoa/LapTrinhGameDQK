# Living Farm — Giai đoạn 4: Nhân vật, NPC, Động vật

Sinh bằng `03_Characters/gen_characters.py` và `04_Animals/gen_animals.py` (cần `pxlib.py` ở thư mục gốc). Đúng 43 màu, không pixel bán trong suốt (đã kiểm tra).
Hướng "right" là bản **lật gương** của "left" (xuất sẵn thành frame riêng).

## Quyết định thay đổi so với Giai đoạn 1
- **Player dùng khung 48x48** (không phải 16x32): thân nhân vật vẫn 16x30 px, phần còn lại là chỗ cho cán công cụ vung ra hai bên, phía trên đầu và 6 px bên dưới chân. Pivot **tùy chỉnh (0.5, 0.125)** = đáy chân (khung chừa 6 px phía dưới cho đầu công cụ khi vung).
- NPC giữ 16x32. Gà/vịt 16x16, bò/cừu 32x32, pivot Bottom Center.

## File
| File | Kích thước | Nội dung |
|---|---|---|
| `Player/player_a..d_sheet.png` | 192x1728 (4 cột x 36 hàng, ô 48x48) | 4 kiểu ngoại hình |
| `NPC/npc_*_sheet.png` (6 file) | 96x288 (6 cột x 9 hàng, ô 16x32) | idle, walk, 6 biểu cảm |
| `Animals/Sheets/animal_*_sheet.png` (4 file) | 64x192 (chim, ô 16) · 128x384 (bò/cừu, ô 32) | idle, walk, eat |
| `*.names.txt` | | Tên sprite theo thứ tự ô (ô trống = dòng trống) |
| `Preview/` | | `player_preview_x4`, `lineup_x5`, `expressions_x4`, `animals_preview_x4` |

### Player (mỗi hướng: down, up, left, right)
| Anim | Frame | fps | Loop |
|---|---|---|---|
| idle | 2 | 4 | có |
| walk | 4 | 8 | có |
| hoe / chop / mine | 3 (nâng, vung, đập) | 10 | không |
| water | 3 | 8 | không |
| harvest | 3 | 8 | không |
| carry_idle / carry_walk | 2 / 4 | 4 / 8 | có |

Sheet: mỗi anim chiếm 4 hàng (down, up, left, right), mỗi hàng tối đa 4 cột. `carry_*` chỉ vẽ tư thế ôm trước ngực; vật phẩm cầm là sprite riêng gắn ở game. Cán công cụ lấy từ sprite công cụ Giai đoạn 3 (nên nếu đổi icon công cụ, vẽ lại bằng script).

Tùy chỉnh ngoại hình mức cơ bản: 4 preset (da, tóc, áo, quần, mũ khác nhau). Muốn thêm kiểu mới, sửa dict `PLAYERS` trong script rồi chạy lại.

### NPC (6 người, chỉ có hình ảnh — không có AI/hội thoại)
`npc_farmer_old`, `npc_baker`, `npc_merchant`, `npc_girl`, `npc_smith`, `npc_scholar`. Hàng 0–3 idle (2 frame), hàng 4–7 walk (4 frame), hàng 8: biểu cảm `neutral, happy, sad, surprised, angry, confused` (khuôn mặt nhìn thẳng, tên `npc_x_expr_<tên>`). Dùng đổi sprite thủ công/script, không đưa vào Animator.

### Động vật
Mỗi con: idle (2), walk (4), eat (3) x 4 hướng. Tên `animal_<loài>_<anim>_<hướng>_<NN>`.

## Import và Animator (Unity)
1. Chép `Player/`, `NPC/`, `Animals/Sheets/` vào `Assets/Art/Characters|Animals`; chép `Unity/*.cs` vào `Assets/Editor/` (Slicer, AnimBuilder) và `Assets/Scripts/` (CharacterAnimDriver).
2. Chọn các sheet → **Living Farm > Slice Sheet (names.txt)** (đọc `#cell=` và pivot bottom).
3. Chọn lại các sheet → **Living Farm > Build Animator From Sheet**. Tool tạo AnimationClip và AnimatorController: tham số int `Anim` (0 idle, 1 walk, 2 hoe, 3 water, 4 harvest, 5 chop, 6 mine, 7 carry_idle, 8 carry_walk, 9 eat) và `Dir` (0 down, 1 up, 2 left, 3 right).
4. Tạo GameObject: SpriteRenderer + Animator (gán controller) + `CharacterAnimDriver` + Rigidbody2D (Gravity 0, Freeze Rotation).
5. Thiết lập: PPU 16, Point, Compression None, Sorting theo Y (Custom Axis 0,1,0).

Collider gợi ý: Player/NPC `CapsuleCollider2D` hoặc Box ~10x6 px ở chân; gà/vịt Box ~10x6; bò/cừu Box ~24x12 ở thân dưới. Các script C# chưa chạy thử trong Unity.

## Hạn chế
- Biểu cảm NPC nhỏ (mặt cao khoảng 6 px): chỉ "ngạc nhiên" và "vui" rõ ngay; nên bổ sung bong bóng emote ở Giai đoạn 6.
- Hướng `up` của Player: công cụ vẽ đè lên người, chưa che khuất bởi cơ thể.
- Không có animation tùy chỉnh theo lớp (layer) cho ngoại hình; ngoại hình = preset cả sheet.
- Động vật chưa có animation phụ (ngủ, kêu); bò chỉ vẽ bò sữa (không có bê/bò đực).
- Chưa có bóng đổ dưới nhân vật (để Giai đoạn 6).
