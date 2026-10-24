# Đóng Góp Mod Cho AIX PLANET

(Bản tiếng Anh: [CONTRIBUTING.md](CONTRIBUTING.md))

Cảm ơn bạn đã xây dựng cho hành tinh này. Repo này là bề mặt công khai duy
nhất của một game mã nguồn đóng, nên các quy tắc dưới đây giữ cho mod an
toàn, nguyên bản và sẵn sàng đưa vào game.

## Quy trình gửi mod

1. **Fork** repo này và tạo mod của bạn:
   - Mod Lua: thư mục mới `mods/<mod_id>/` gồm `manifest.json` + `main.lua`.
   - Hình thái trực quan: một file JSON trong `mods/visuals/`.
   - Kịch bản thời tiết: một file JSON trong `mods/weather/`.
2. **Kiểm tra** trước khi gửi:
   `python tools/validate_mod.py mods/<mod_id>` (hoặc truyền đường dẫn file
   JSON). Mô tả PR phải kèm kết quả chạy validator.
3. **Mở Pull Request** theo mẫu gửi mod. Mỗi PR một mod.

## Chuẩn duyệt

- **Chỉ tác phẩm gốc.** Tự viết code và dữ liệu của bạn. Không sao chép code
  từ game hay dự án khác (kể cả dự án GPL). Học *ý tưởng thiết kế* từ game
  khác thì được — hãy ghi rõ trong PR; sao chép code thì không.
- **Tự chứa.** Một mod là thư mục của nó (cộng thư mục `assets/` tùy chọn).
  Không thứ gì bên ngoài thư mục được phép là điều kiện để mod chạy, và xóa
  thư mục là gỡ mod hoàn toàn.
- **An toàn theo cấu trúc.** Mod Lua chạy trong sandbox đã cọ sạch (không
  `os`, `io`, `debug`, không hệ thống file hay mạng). Mod lỗi bị cô lập và
  ghi nhận; mod không được phép dựa vào việc gây lỗi hay chặn tick.
- **Cân bằng là một cuộc trao đổi.** Chỉ thị thời tiết và ghi cấu hình tác
  động lên một thế giới chung, liên tục. Hiệu ứng cực đoan vẫn được hoan
  nghênh dưới dạng ý tưởng — hãy kỳ vọng đội ngũ bảo trì cùng bạn tinh
  chỉnh con số thay vì bác bỏ ý tưởng.
- **Hợp đồng API.** Nhắm `api_version: "1"` (xem [MODDING.md](MODDING.md)).
  Manifest khai `api_version` mới hơn mức engine hỗ trợ sẽ bị đánh dấu,
  không được nạp.

## Bản quyền đóng góp

- Bạn giữ bản quyền mod của mình.
- Khi mở Pull Request, bạn cấp phép mod của mình theo **Giấy phép MIT**
  (inbound = outbound), và trao cho AIXLAB quyền đưa mod đã duyệt vào AIX
  PLANET, kèm ghi danh tên `author` của bạn trong manifest và danh sách mod
  trong game.
- Chỉ gửi tác phẩm mà bạn có quyền cấp phép theo cách này.

## Sau khi được merge

Mod đạt chuẩn được đồng bộ từ repo này vào bản dựng game và nạp nóng
(`POST /api/mods/reload`, phía quản trị). Nếu một mod đã phát hành cần bị
rút vì cân bằng hay an toàn, nó sẽ bị vô hiệu qua manifest — ghi nhận tác
giả của bạn vẫn nằm trong lịch sử của repo này.
