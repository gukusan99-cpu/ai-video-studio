# Thử nghiệm chọn giọng đọc (13/11/2026)

Cách đo: tạo cùng 8 câu khó của tập Chi Lăng (tên riêng, số năm, câu dài) bằng từng giọng, rồi cho máy nhận dạng giọng nói tiếng Việt
(Vosk, offline) "nghe" lại. WER = tỷ lệ từ máy nghe sai → thấp hơn = rõ chữ hơn. (Mô hình nhỏ có sai số nền ~20%.)

| Giọng | WER | Tốc độ |
|---|---|---|
| **NamMinh, rate −10%, pitch −4Hz (CHỌN)** | **23.7%** | 3.84 từ/s |
| NamMinh, rate −4% | 26.0% | 4.09 từ/s |
| NamMinh, rate −8% | 28.2% | 3.92 từ/s |
| HoaiMy (nữ), rate −4% | 28.2% | 3.97 từ/s |
| Piper vais1000 (offline) | 50.4% | 4.51 từ/s |

Kết luận: giọng nam NamMinh chậm & trầm nhẹ rõ nhất và hợp phong cách kể chuyện lịch sử (các kênh tóm tắt lịch sử thường dùng giọng nam,
nhịp vừa phải, ~3.5–4 từ/giây). Piper chỉ dùng khi không có mạng.

Muốn giọng "người thật" hơn nữa (miễn phí có giới hạn / trả phí): Vbee, FPT.AI, Zalo AI, ElevenLabs – cần tài khoản & API key của bạn;
khi có key, thêm engine mới vào `make.py → tts_line`. Tốt nhất về lâu dài: tự thu giọng thật.

## Vòng 2 (13/11/2026)
| Giọng | WER |
|---|---|
| **NamMinh −10%, −4Hz (giữ nguyên)** | **23.7%** |
| NamMinh −14%, −7Hz (trầm/chậm hơn nữa) | 25.2% |
| Giọng "Multilingual" của Microsoft (Andrew, Brian, William, Rémy, Florian…) | không dùng được – dịch vụ miễn phí không trả âm thanh tiếng Việt |

Tham khảo kênh: các bài tổng hợp khen kênh "Sử Lược" vì giọng nam "hay, dễ nghe, đan xen chút hùng hồn"; EZ Sử không công bố người lồng tiếng.
→ Giữ NamMinh chậm & trầm nhẹ; câu dồn dập (nhiều tên riêng) thêm ngắt nghỉ bằng dấu phẩy trong `say` và chậm riêng bằng `"rate": "-16%"`.
