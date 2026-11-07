# Rắn Săn Mồi - Snake Master (Python)

Trò chơi Rắn Săn Mồi cổ điển với giao diện đồ họa Pygame hiện đại, mượt mà ở tốc độ 60 FPS và hỗ trợ hiển thị Tiếng Việt đầy đủ.

### Đặc điểm & Luật chơi:
- **Kích thước bàn chơi:** Lưới 24x20 ô (mỗi ô 26px) cùng thanh hiển thị thông số phía trên.
- **3 Cấp độ khó:** Tùy chọn tốc độ di chuyển linh hoạt trước khi vào ván:
  - **Chậm:** ~7 ô/giây (140ms/bước)
  - **Vừa:** ~12 ô/giây (85ms/bước)
  - **Nhanh:** ~18 ô/giây (55ms/bước)
- **Điều khiển mượt mà:** Hỗ trợ bộ đệm lệnh bấm phím (Input Queue), giúp chuyển hướng nhanh liên tiếp mà không bị khựng phím hay lỗi tự cắn vào cổ.
- **Tính điểm & Luật va chạm:** Mỗi mồi ăn được cộng **10 điểm**. Trò chơi kết thúc khi rắn đâm vào tường biên hoặc tự cắn vào thân.
- **Bảng xếp hạng riêng biệt:** Tự động lưu trữ Top 5 điểm cao nhất cho từng cấp độ khó vào file `snake_leaderboard.json`.
- **Hiển thị trực quan:** Mồi ăn có hiệu ứng phát sáng (glow), đầu rắn có mắt xoay theo hướng di chuyển.

### Phím điều khiển:
- **Tại Menu chính:** Nhấn phím `1`, `2`, `3` (hoặc click chuột) để chọn độ khó. Nhấn `SPACE` hoặc `ENTER` để bắt đầu.
- **Trong khi chơi:** Dùng các phím mũi tên (`↑`, `↓`, `←`, `→`) hoặc cụm phím `W`, `A`, `S`, `D` để điều hướng. Nhấn `ESC` để quay về Menu chính.
- **Khi Game Over:** Nhấn `SPACE` để chơi lại ngay hoặc `ESC` để về Menu chính.

---

### Hướng dẫn cài đặt & chạy:

1. Đảm bảo máy đã cài **Python 3.10+** (hỗ trợ tốt nhất các bản Python mới nhất).
2. Mở terminal / command prompt tại thư mục project:
```bash
py -m pip install pygame-ce
```
3. Khởi chạy game:
```bash
python mainSnake.py
```
