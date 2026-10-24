# AIX PLANET — Mod Cộng Đồng

[Tiếng Anh (English)](README.md) | **Tiếng Việt**

Nơi cộng đồng đóng góp mod cho **AIX PLANET** — trò chơi mô phỏng hệ sinh thái
tiến hóa nhiều người chơi, vận hành liên tục, do **AIXLAB** phát triển. Hàng
nghìn bầy sinh vật tiến hóa, di cư, lai giống và tuyệt chủng trên một hành
tinh sống tick mỗi 90 giây — và mod cho phép bạn bẻ cong thời tiết, sinh thái
và hình thái của nó.

> Engine của game là mã nguồn đóng, nằm trong một repository riêng tư.
> **Repo này là bề mặt mod công khai**: toàn bộ hợp đồng Lua Mod API, các
> định dạng mod dữ liệu, mod mẫu chạy được, công cụ kiểm tra, và các mod cộng
> đồng được đưa vào game. Bạn không bao giờ cần mã nguồn engine để làm mod —
> mod là các thư mục tự chứa, thả vào là chạy.

## Giới thiệu về game

**AIX PLANET** là một mô phỏng tiến hóa vĩ mô nhiều người chơi, thế giới
không bao giờ dừng: mỗi **90 giây** là một tick, mùa màng luân chuyển, các
loài trỗi dậy và tuyệt chủng dù có ai đang xem hay không.

- **Một hành tinh sống** — 81.358 ô lục giác (Uber H3) trải khắp các lục địa
  và đại dương, với đới sinh thái theo vĩ độ từ lãnh nguyên Bắc cực tới sa
  mạc xích đạo. Một năm dài 120 tick (Xuân 20 · Hạ 40 · Thu 20 · Đông 40) và
  một thế hệ dài 480 tick.
- **Sáu thế lực** — phe người chơi **Solaris Vanguard** (PLAYER_1), bốn đế
  chế lãnh chúa AI (Frostborn Syndicate, Verdant Swarm, Dune Ravagers,
  Abyssal Armada), và hệ sinh thái hoang dã **SYSTEM_AI** chuyên gieo và tái
  gieo sự sống cho hành tinh.
- **Sinh vật có gene thật** — mỗi bầy mang bộ DNA 4 trục (chịu nhiệt, cơ
  động, trao đổi chất, hình thái chiến đấu), theo một trong bốn học thuyết
  (ZERG bầy đàn, PREDATOR săn mồi, TURTLE sinh tồn, NOMAD khai phá), và leo
  qua **5 giai đoạn tiến hóa** chấm theo đỉnh thế hệ (Stage 2 tại 2.500 ·
  Stage 3 tại 10.000 · Stage 4 tại 15.000 · Stage 5 tại 100.000 cá thể).
- **Sinh thái biết phản kháng** — bầy lớn ăn trên dấu chân đa ô (tối đa 19
  ô), sinh sản theo cửa sổ mùa của từng dòng họ, các loài khác nhau có thể
  **lai giống**, hàng xóm lâu năm có thể **cộng sinh**, dịch bệnh lan theo
  từng ô, sa mạc lấn dần, và một AI kể chuyện (storyteller) liên tục ném hạn
  hán, mùa hoa nở và khủng hoảng vào biên niên sử.
- **Người chơi dẫn dắt, thế giới ghi nhớ** — ra lệnh trực tiếp (di chuyển,
  tách đàn, hợp nhất, đột biến, di cư tầm xa), để Governor (phi công tự
  động) canh giữ bầy khi bạn offline, và đọc bản tóm tắt *"khi bạn vắng
  mặt"* đầy đủ lúc quay lại. Cây phả hệ, hầm di sản gene, biên niên sử từng
  phe và bảng vinh danh tuần/tháng ghi lại tất cả.
- **Vinh danh thay chiến thắng** — không có màn hình "thắng game". Các
  vương triều giành vinh dự, thành tựu và quyền đặt tên; phe giữ vị trí #1
  sinh khối **3 ngày liên tiếp** sẽ mở khóa một lần phát động thảm họa sinh
  thái của riêng mình (FAMINE nạn đói, FREEZE băng giá, DEFOREST phá rừng —
  hoặc PLAGUE dịch bệnh gieo thẳng vào các ô đông nhất của đối thủ).
- **Kỷ nguyên thế giới (v10.0)** — mỗi thế hệ hành tinh bước vào một kỷ
  nguyên mới (Phì nhiêu, Băng giá, Dịch bệnh, Săn mồi, Hòa bình hoặc Khắc
  nghiệt), được công bố trước 120 tick, và một dòng predator có thể trỗi
  dậy thành **Apex Ascendant** (Đỉnh Săn Mồi).

*Ảnh chụp thế giới (báo cáo kiểm định đã audit, tick 2829): 3,7 triệu sinh
khối, 962 bầy đang sống, 10 bầy Stage 3 đầu tiên.*

**Mod của bạn chạy ngay trong thế giới này** — cùng một hành tinh liên tục
mà người chơi đang sống, không phải bản sao sandbox.

## Bắt đầu nhanh

1. Sao chép mod mẫu:
   `cp -r mods/example_bloom_festival mods/<id_mod_cua_ban>`
2. Sửa `manifest.json` (`id` duy nhất, tên bạn ở trường `author`) và
   `main.lua` (hook `on_tick(ctx)` trả về các chỉ thị — xem [MODDING.md](MODDING.md)).
3. Kiểm tra tại máy:
   `python tools/validate_mod.py mods/<id_mod_cua_ban>`
4. Mở Pull Request. Quy trình duyệt theo [CONTRIBUTING.vi.md](CONTRIBUTING.vi.md)
   (bản tiếng Anh: [CONTRIBUTING.md](CONTRIBUTING.md)).

## Ba cách làm mod

| Loại | Vị trí | Kỹ năng cần |
|---|---|---|
| **Mod Lua** | `mods/<mod_id>/` gồm `manifest.json` + `main.lua` | Viết script cơ bản — phản ứng theo từng tick, gọi sự kiện thời tiết, ghi cấu hình thế giới, ghi log vào dòng thời gian |
| **Hình thái trực quan** | `mods/visuals/*.json` | Chỉ cần JSON — định nghĩa điều kiện kích hoạt (giai đoạn, địa hình, sĩ số, gene) và hình dạng đặc biệt mà bầy biến thành |
| **Kịch bản thời tiết** | `mods/weather/*.json` | Chỉ cần JSON — định nghĩa ngưỡng mật độ kích hoạt và sự kiện sinh thái được giải phóng |

Hợp đồng đầy đủ: [MODDING.md](MODDING.md) · JSON schema: [`schemas/`](schemas/)

## Mod được vào game như thế nào

1. Bạn mở PR tại repo này.
2. Đội ngũ bảo trì duyệt (tính nguyên bản, cân bằng, an toàn — mod chạy
   trong sandbox, mod lỗi không bao giờ làm sập tick).
3. Mod đạt chuẩn được merge tại đây, đồng bộ vào thư mục `mods/` của bản
   dựng game và nạp nóng. **Tên tác giả của bạn đi theo mod** trong
   `manifest.json` và trong danh sách mod trong game (`GET /api/mods`).

## Cấu trúc repo

```
mods/            Mod cộng đồng (thư mục Lua, script .lua legacy, visuals/, weather/)
schemas/         JSON Schema cho manifest.json và các định dạng mod dữ liệu
tools/           validate_mod.py — công cụ kiểm tra offline (không cần cài game)
MODDING.md       Hợp đồng Lua Mod API (API v1)
CONTRIBUTING.md  Quy trình gửi mod, chuẩn duyệt, điều khoản bản quyền
```

## Giấy phép

Tài liệu, ví dụ và công cụ của repo: MIT (xem [LICENSE](LICENSE)).
Mod đóng góp: tác giả giữ bản quyền và cấp phép mod của mình theo MIT khi
gửi — xem [CONTRIBUTING.vi.md](CONTRIBUTING.vi.md).
