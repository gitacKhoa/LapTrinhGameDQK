# Living Farm — Giai đoạn 5b: UI

Sinh bằng `gen_ui.py`. **Không có chữ** trong sprite; ảnh `Preview/ui_screens_preview.png` dùng thanh xám giả chữ chỉ để minh họa bố cục (không nằm trong sprite xuất ra).

## File
- `Sprites/` — 39 sprite UI (panel, slot, nút, thanh, đồng hồ...).
- `Icons/` — 32 icon 16x16 lẻ + `icons_16.png` (128x64, 8x4) + `icons_16.names.txt`.
- `Unity/ui_sprites.csv` — kích thước và **border 9-slice** (left, bottom, right, top) từng sprite.
- `Unity/LivingFarmUISetup.cs` — Editor tool đặt import + border tự động.
- `Preview/` — `ui_screens_preview` (HUD, túi đồ, cửa hàng, nhiệm vụ, hội thoại, tạm dừng, tổng kết ngày, chế tạo), `ui_catalogue_x3`, `icons_x4`.

## Danh mục
| Nhóm | Sprite | Cách dùng |
|---|---|---|
| Panel (9-slice, border 6) | `ui_panel_parchment` (cửa sổ sáng), `ui_panel_wood`, `ui_panel_dark` (tooltip, pause, khung thông tin), `ui_dialogue_box` | Image Type: Sliced |
| Nhỏ (9-slice, border 5) | `ui_nameplate`, `ui_hud_plate` (thanh tiền/ngày), `ui_prompt_bubble` | Sliced |
| Ô túi đồ | `ui_slot`, `ui_slot_selected` (20x20, border 3) | Sliced; icon vật phẩm 16x16 đặt giữa |
| Nút (32x16, border 6) | `ui_btn_wood/green/red_{normal,hover,pressed}`, `ui_btn_disabled` | Button + Sprite Swap |
| Thanh tiến trình | `ui_bar_frame`, `ui_bar_v_frame`, `ui_bar_fill_{green,orange,blue,red}`, `ui_bar_mini_*` (tiến trình cây) | Fill: Image Type Filled, Horizontal/Vertical |
| Thời gian | `ui_clock_dial` (32x32) + `ui_clock_hand` (3x13, xoay quanh đầu dưới) | Hand: pivot Bottom Center, xoay theo giờ |
| Khác | `ui_ribbon_red` (tiêu đề, border 10 trái/phải), `ui_divider`, `ui_scroll_track/handle`, `ui_keycap(+_pressed)`, `ui_arrow_down_0/1` (mũi tên "tiếp", 2 frame) | |

Icon (thứ tự trong `icons_16.png`): coin, sun, moon, calendar, cloud, rain, storm, snow, heart, energy, star, star_empty, quest, alert, backpack, bag, gear, pause, play, close, check, plus, minus, arrow_left/right/up/down, lock, home, clock, trash, map.

## Thiết lập Unity
- Chép vào `Assets/Art/UI/{Sprites,Icons}`, `ui_sprites.csv` vào `Assets/Art/UI/`. Chạy **Tools > Living Farm > Setup UI Sprites** (chưa thử trong Unity; nếu lỗi: Single, PPU 16, Point, Uncompressed rồi đặt Border trong Sprite Editor theo CSV).
- Canvas: Scale With Screen Size, **Reference Resolution 480x270**, Match = 0.5, Pixels Per Unit 16. Tắt Preserve Aspect cho ảnh 9-slice.
- Dùng TextMeshPro với font pixel riêng (có giấy phép thương mại) đặt trên các panel; bảng màu chữ gợi ý: tối `SO0 #2c1d1a` trên parchment, sáng `CR1 #fffaf0` trên panel dark, vàng `SU3` cho tiền.
- Màn hình: **Tạm dừng** = `panel_dark` + `btn_wood` (nút Thoát dùng `btn_red`); **Tổng kết ngày** = `ribbon_red` + `panel_parchment` + `slot` + icon `coin`, `star`/`star_empty`; **Nhiệm vụ** = `panel_parchment` + icon `quest` + `bar_mini`; **Hội thoại** = `dialogue_box` + `nameplate` + `arrow_down` (xoay 2 frame 2 fps).

## Hạn chế
- Chưa có font; chữ do TextMeshPro đảm nhiệm.
- Hover/pressed của slot chưa vẽ (dùng `slot_selected` làm hover).
- Chưa có skin sáng/tối khác; chỉ 1 theme gỗ + giấy.
- Con trỏ chuột và biểu tượng bàn phím cụ thể (E, F...) chưa có; `ui_keycap` là phím trống để gắn chữ.
