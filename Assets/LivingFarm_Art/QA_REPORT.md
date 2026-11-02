# Báo cáo QA — Living Farm

- File PNG quét: **202**
- Sheet có names.txt: **29**, ô sprite có tên: **1063**
- Lỗi: **0** · Cảnh báo: **0**
- Màu bảng màu đã dùng: **43/43**

## Lỗi

Không có.

## Cảnh báo

Không có.

## Kiểm tra đã chạy

1. Mọi PNG (trừ Shadows) chỉ dùng 43 màu trong bảng màu, pixel alpha 0 hoặc 255.
2. Kích thước sheet chia hết cho ô; số tên ≤ số ô; không trùng tên; ô có tên không rỗng; ô không tên rỗng.
3. Sprite (nhân vật/vật thể/máy/vật phẩm/emote) không có nội dung sáng màu chạm viền ô (nguy cơ bị cắt). Hiệu ứng hạt `fx_*` được loại trừ vì hạt bay ra mép là chủ ý; cầu/cổng/hàng rào chủ ý liền mạch giữa các ô.
4. Chân nhân vật/động vật giữa các frame của cùng animation lệch ≤ 2 px (bỏ qua animation có công cụ).
5. Vật phẩm/vật thể/icon có đủ tương phản trên nền sáng (`CR1`) và tối (`OL0`).
6. `QA/contact_light_dark.png`: ảnh tổng hợp để kiểm tra mắt.
