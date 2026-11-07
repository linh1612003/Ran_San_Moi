# Game Cờ Caro 2 Người (Python)

Trò chơi Cờ Caro 2 người chơi với giao diện đồ họa Pygame mượt mà.

### Đặc điểm & Luật chơi:
- **Kích thước bàn cờ:** 20x20 ô (rộng rãi, chuẩn bàn cờ thi đấu thực tế).
- **Luật phân định thắng bại:** Đạt đủ 5 quân liên tiếp (ngang, dọc, chéo).
- **Luật chặn 2 đầu:** Nếu chuỗi 5 quân bị đối thủ **chặn cả 2 đầu mút** thì **không tính là thắng**.
- **Tính điểm & Tỉ số:** Hiển thị tỉ số trận đấu giữa Player X và Player O qua từng ván.
- **Nút "Ván mới":** Bắt đầu ván mới mà vẫn giữ nguyên tỉ số tổng.
- **Hiển thị trực quan:** Viền vàng đánh dấu nước cờ gần nhất, highlight màu xanh lá chuỗi 5 quân chiến thắng.

---

### Hướng dẫn cài đặt & chạy:

1. Đảm bảo máy đã cài **Python 3.10+** (hỗ trợ tốt nhất các bản Python mới nhất).
2. Mở terminal / command prompt tại thư mục project:
```bash
pip install -r requirements.txt
```
3. Khởi chạy game:
```bash
python main.py
```
