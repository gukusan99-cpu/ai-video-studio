# Kinh thánh kênh (Channel Bible) – TÍ XUYÊN SỬ

## Định vị
- **Tên kênh:** Tí Xuyên Sử · **Khẩu hiệu:** "Mỗi ngày 1 phút – đi xuyên lịch sử Việt"
- **Khán giả:** học sinh 10–15 tuổi, phụ huynh và người lớn yêu lịch sử (KHÔNG đặt "dành cho trẻ em", vì đối tượng chính là người xem phổ thông).
- **Lời hứa:** mỗi tập trả lời 1 câu hỏi "Vì sao…?" về một sự kiện có thật, kể bằng hoạt hình vui nhộn, đúng sử.
- **Vì sao chọn chủ đề này:** lịch sử là nhóm nội dung "dùng được lâu" (ít lỗi thời), giáo dục nên quảng cáo khá; có nhân vật cố định làm thương hiệu → khác biệt và không bị coi là nội dung AI hàng loạt; tiếng Việt ít đối thủ làm hoạt hình chỉn chu.

## Nhân vật (KHOÁ – không thay đổi giữa các tập)
**Tèo** – cậu bé 9 tuổi dẫn chuyện (biểu cảm mặc định `blank` = mặt đơ mắt trố; thêm think/sleepy/smug/shock/scared/happy/angry/sad/cry), lém lỉnh, hay cà khịa tỉnh bơ, hay hỏi "Vì sao?" (vẽ bằng `peg(who="teo")`, studio/cast.py)
- Đầu to tròn, **tai vểnh**, tóc bát úp đen có mái răng cưa + 1 lọn xoăn trên đỉnh, tàn nhang, má hồng, **răng thỏ sứt**, mắt ốc nhồi
- Áo bà ba màu chàm `#2F4D8F`, 3 cúc trắng, quần soóc xanh đen, khăn quàng đỏ `#D62F3A` thắt nút
- **Đồng hồ thời gian** vàng `#F4C430` đeo trước ngực – phát sáng khi xuyên không
**Tí** – chú **châu chấu** xanh lá `#7CC242`, mắt to lờ đờ, râu dài, luôn ngồi trên vai trái Tèo (phía bên phải khung hình),
không nói, chỉ biểu cảm (smug/shock/happy/deadpan/scared); có thể đứng riêng bằng `chauchau(x, y, s, expr)`. Kênh vẫn tên "Tí Xuyên Sử".

Bộ tư thế có sẵn: `stand, wave, point, cheer, think, hold, shock, run` · Biểu cảm: `happy, excited, determined, worried, surprised`.
(Xem `channel/character_sheet.png`.)

Khi dùng ảnh AI bên ngoài (Gemini, Bing…), luôn dán **mô tả khoá** này vào đầu prompt:
> A 9-year-old Vietnamese boy named Tèo, cylinder peg-doll body with no arms, oil-paint texture, thick dark-brown outlines, oversized round head, big sticking-out ears, black bowl haircut with jagged bangs and one curl on top, deadpan blank stare (big empty white eyes with tiny dot pupils, flat mouth), freckles, two buck teeth, rosy cheeks, indigo áo bà ba shirt with three white buttons, red scarf, dark navy shorts, a glowing golden pocket watch on his chest, a small bright-green grasshopper with big sleepy eyes and long antennae (named Tí) on his left shoulder.

## Phong cách hình ảnh
Vector phẳng, viền nâu đậm `#2B1B12`, màu ấm, nền núi đá vôi/sông nước Việt Nam. Không máu me; chiến tranh thể hiện bằng thuyền vỡ, cờ, nước bắn.

## Công thức 1 tập (45–60s, 6–9 cảnh)
1. **Hook (0–3s):** câu "Nếu bạn là…", "Vì sao…", "Đừng bao giờ…" + hình gây tò mò.
2. **Tí xuất hiện (3–8s):** "Chào bạn, mình là Tí…" + địa điểm, năm.
3. **Bối cảnh / mâu thuẫn (8–20s)**
4. **Bí mật / mưu kế (20–35s)**
5. **Cao trào (35–45s)**
6. **Kết quả + "Điều thú vị" (45–55s)**
7. **CTA hỏi người xem (cuối):** "Bạn muốn Tèo và Tí đến… tiếp theo? Bình luận nhé!"

## Lịch đăng & mở rộng
- 4–5 Shorts/tuần, 18:30–20:30. Mỗi 8 tập → gộp thành 1 video dài 8–10 phút ("Tí Xuyên Sử – Tập tổng hợp") để tích giờ xem.
- Sau ~30 tập: lồng tiếng tiếng Anh cho cùng hình ảnh (kênh "Time Kid Ti") để có RPM cao hơn.

## Kiếm tiền (thực tế)
- Quảng cáo YouTube (sau 1.000 sub + 10 triệu lượt xem Shorts/90 ngày, hoặc 4.000 giờ xem video dài).
- Bán sản phẩm phụ: bộ tranh tô màu / sticker Tèo & châu chấu Tí, sách tóm tắt lịch sử (affiliate Shopee/Tiki sách sử).
- Tài trợ từ nhà sách, ứng dụng học tập khi kênh đạt 20–50k sub.
