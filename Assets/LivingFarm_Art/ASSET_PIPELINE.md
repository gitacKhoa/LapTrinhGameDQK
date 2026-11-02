# Living Farm — Asset Pipeline (tổng hợp Giai đoạn 1–6)

Bộ asset pixel art 2D cho Unity 6000.3, **sinh hoàn toàn bằng code** (Python + Pillow) từ bảng màu 43 màu. Project đã được kiểm tra trên Unity 6000.3.27f2. Không dùng asset, font hay mô hình bên ngoài.
Chạy lại toàn bộ: `python3 build_all.py` (sinh asset → QA → đóng gói `LivingFarm_Assets.zip`).

## 1. Chuẩn đồ họa (đã chốt, không đổi)
Tile 16x16 · PPU 16 · top-down 3/4 · reference resolution 480x270 · viền tối 1 px · ánh sáng trên-trái · không anti-aliasing · bảng màu 43 màu (`00_Standards/LivingFarm.hex|.gpl`).
Ngoại lệ có chủ ý: `Shadows/` dùng alpha 96 (bóng đổ mềm); khung người chơi **48x48** (thay vì 16x32) để chứa cán công cụ khi vung, pivot (0.5, 0.125).

## 2. Cấu trúc thư mục
| Thư mục | Nội dung |
|---|---|
| `00_Standards/` | Bảng màu, tài liệu quy chuẩn |
| `01_Environment/` | Tile đất/đường, nước và hàng rào 16-mask, vật thể (cây, đá, bụi, hoa, cầu, cổng...) |
| `02_Crops_Items/` | 7 cây x 6 trạng thái, 32 vật phẩm/công cụ, CSV + ScriptableObject |
| `03_Characters/` | 4 người chơi (preset), 6 NPC (+6 biểu cảm) |
| `04_Animals/` | Gà, vịt, bò, cừu (idle, walk, eat) |
| `05_Buildings/` | 4 công trình, rương, 3 máy chế biến, bàn chế tạo, 3 máy tưới, footprint/collider |
| `06_UI/` | 39 sprite UI (9-slice), 32 icon |
| `07_Effects/` | Hiệu ứng, thời tiết, bong bóng emote, bóng đổ |
| `Assets/Editor/`, `Assets/Scripts/` | Script Unity đã tích hợp: Slicer, AnimBuilder, DataImporter, UISetup, TexturePostprocessor và các runtime data/animation scripts |
| `QA/`, `QA_REPORT.md` | Ảnh sáng/tối tổng hợp và báo cáo kiểm thử |
| `LivingFarm_Assets/` (ngoài thư mục này) | **Chỉ ảnh**, gọn để kéo vào Unity |

## 3. Quy tắc đặt tên
`<nhóm>_<đối tượng>_<biến thể/anim>_<hướng>_<NN>`: `env_grass_a`, `crop_tomato_ready`, `item_seed_corn`, `tool_axe`, `player_a_walk_down_02`, `npc_baker_expr_happy`, `animal_cow_eat_left_01`, `bld_house`, `machine_oven_work_a`, `ui_btn_green_hover`, `icon_coin`, `fx_water_03`, `emote_heart`. Chữ thường, snake_case, frame 2 chữ số, hướng `down/up/left/right` (right = lật gương của left).
Mỗi sheet có file `*.names.txt` (dòng đầu `#cell=WxH pivot=...`).

## 4. Quy trình đưa vào Unity
1. Tạo project 2D (URP), cài **2D Pixel Perfect**, **2D Tilemap Extras**, **2D Sprite**.
2. Trong project hiện tại, ảnh đã nằm ở `Assets/Art/`, CSV ở `Assets/Data/Source/`, và script chuẩn ở `Assets/Editor/` + `Assets/Scripts/`. Các bản C# trùng lặp của từng giai đoạn được lưu ngoài `Assets` trong `LivingFarm_Art_LegacyScripts/`; không chép chúng trở lại `Assets`, nếu không Unity sẽ báo định nghĩa class trùng.
3. `LivingFarmTexturePostprocessor` tự đặt PPU 16, Point, Uncompressed, tắt mipmap cho mọi texture dưới `Assets/Art/`.
4. Chọn từng sheet → **Assets > Living Farm > Slice Sheet (names.txt)**; chọn sheet nhân vật/động vật → **Build Animator From Sheet**; **Tools > Living Farm > Setup UI Sprites** và **Create Data Assets From CSV**.
5. Camera: Pixel Perfect Camera (Assets PPU 16, Reference 480x270, Upscale Render Texture). Graphics > Transparency Sort Mode = Custom Axis (0,1,0). Canvas UI: Scale With Screen Size 480x270.
6. Tilemap: thứ tự layer Water → Ground → Soil → Fence → Objects; Rule Tile cho nước/hàng rào (16 mask, xem `01_Environment/README_Environment.md`); Tilemap Collider 2D + Composite cho Water và Fence.

| Sprite Atlas | Nội dung | Thiết lập |
|---|---|---|
| `Atlas_Environment` | Tile, vật thể môi trường | Point, Uncompressed, padding 2, Allow Rotation tắt |
| `Atlas_Crops_Items` | Cây, vật phẩm | như trên |
| `Atlas_Characters` | Player, NPC, động vật | như trên (Include in Build) |
| `Atlas_Buildings` | Công trình, máy | như trên |
| `Atlas_UI` | Sprite UI + icon | như trên; để Image 9-slice dùng Tight Packing tắt |
| `Atlas_FX` | Hiệu ứng, emote, bóng | như trên |

Frame rate gợi ý: idle 4 · walk 8 · công cụ 8–10 · animal eat 6 · fx 8–14 · nước 4.

## 5. Kiểm thử (`python3 qa_check.py`)
Kết quả hiện tại: **0 lỗi, 0 cảnh báo**, 29 sheet / 1063 ô sprite có tên, 43/43 màu được dùng.
Đã kiểm tra: chỉ dùng màu trong bảng màu và alpha 0/255 (trừ bóng đổ); kích thước sheet chia hết ô; tên không trùng; ô có tên không rỗng và ngược lại; nội dung không chạm viền ô (nguy cơ cắt); chân nhân vật/động vật không lệch giữa frame; tương phản trên nền sáng và tối.
Lỗi thật đã phát hiện và sửa nhờ QA: cán công cụ của người chơi bị cắt (đổi khung 32x40 → 48x48), mỏ gà/vịt, cán khuấy và ống khói bị cắt ở mép ô.
Cảnh báo còn lại: trứng, gói hạt bắp, icon bản đồ và nhiệm vụ màu kem hơi chìm trên nền sáng (đều có viền tối 1 px).

## 6. Đối chiếu yêu cầu ban đầu
| Hạng mục | Trạng thái |
|---|---|
| Environment (cỏ, đất, cày, tưới, đường, nước, cầu, đá, gốc, bụi, hoa, hàng rào, cổng, biển) | Đủ. Chưa có bộ 47-tile cho hồ tròn và viền đất cày |
| Nhà/chuồng/kho, bàn chế tạo, máy, thùng chứa | Đủ (thùng chứa = rương) |
| Vật thể trang trí | Tối thiểu (bụi, hoa, biển, đá); chưa có bộ decor riêng |
| 7 loại cây x 5 giai đoạn + héo, vật phẩm thu hoạch | Đủ. Giai đoạn `sprout` dùng chung hình |
| Động vật: gà, bò, cừu, vịt; idle/walk/eat 4 hướng | Đủ |
| Player: idle, walk, cuốc, tưới, thu hoạch, chặt, đào, cầm | Đủ; ngoại hình tùy chỉnh = 4 preset |
| NPC: 6 người, idle/walk, 5 biểu cảm | Đủ; chỉ hình ảnh |
| Vật phẩm/công cụ/sản phẩm chế biến | 32 mục (búa, cuốc chim, bánh mì, mứt, phô mai...) |
| Công trình + footprint/collider | Đủ (buildings.csv) |
| UI: thanh công cụ, túi đồ, thông tin, cửa hàng, nhiệm vụ, tiền/thời gian, hội thoại, nút, thanh tiến trình, tạm dừng, tổng kết | Ghép từ sprite 9-slice/icon; mẫu bố cục ở `06_UI/Preview` |
| Effects: nước, đất, thu hoạch, vật phẩm rơi, xu, khói, mưa, ánh sáng/bụi | Đủ. "Vật phẩm rơi" = bóng đổ + pop (chuyển động làm bằng tween); ánh sáng dùng Light 2D |
| ScriptableObject, công cụ cắt sheet, Animator, hướng dẫn Tilemap | Đủ (chưa chạy thử trong Unity) |

## 7. Giới hạn và việc nên làm tiếp
- Các công cụ Slicer, Animator, UI và CSV đã chạy trong Unity; SampleScene đã có Pixel Perfect Camera, Canvas, các lớp Tilemap và collider Water/Fence. Hành vi gameplay/runtime vẫn cần được kiểm thử khi triển khai game.
- Các RuleTile và tile asset đã được tạo; cần tạo/chọn Tile Palette trong Unity để bắt đầu vẽ bản đồ. Tilemap hiện đang trống.
- Nên xem lại bằng mắt ở kích thước game thật: biểu cảm NPC (mặt 6 px), hạt giống và `sprout`, hiệu ứng mưa/lá (rất nhỏ).
- Chưa có: font pixel, âm thanh, bộ 47-tile, biến thể mùa (xuân/hè/thu/đông), công trình ban đêm, nâng cấp công trình, bê/bò đực.
- **Giấy phép:** asset là kết quả code do tôi viết, không lấy từ nguồn ngoài; tuy nhiên trước khi phát hành thương mại, bạn vẫn nên tự xác minh giấy phép của thư viện/công cụ sử dụng (Pillow, Unity, font bạn chọn) và cân nhắc tư vấn pháp lý.
