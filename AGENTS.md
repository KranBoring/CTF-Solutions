# Quy trình làm việc cho CTF-Solutions

Các quy tắc này áp dụng cho toàn repository. Giữ nguyên cấu trúc, tên bài, URL challenge, nội dung write-up và thứ tự ưu tiên hiện có; chỉ thay phần người dùng yêu cầu. Đọc file này trước khi chạy skill hoặc script đồng bộ. Không dùng script cũ nếu nó không thực hiện đủ các quy tắc dưới đây.

## Lệnh người dùng: `Cập nhập wu`

Mặc định lệnh này đồng bộ toàn bộ repository. Nếu người dùng chỉ rõ nền tảng, thư mục hay bài tập thì giới hạn đúng phạm vi đó. Thực hiện tuần tự các bước sau.

### 1. Phát hiện write-up đã hoàn thành

Với mỗi `write-up.md` trong phạm vi:

1. Nếu file không tồn tại, ghi nhận là thiếu; không tự tạo khi đang đồng bộ trạng thái.
2. Đọc UTF-8. Lỗi đọc/giải mã là lỗi cần báo, không được xem là file rỗng.
3. Bỏ BOM đầu file, khoảng trắng, dòng trống, dòng chỉ có Markdown heading (ví dụ `# Tên bài`), và comment HTML `<!-- ... -->`.
4. Coi các dòng chỉ chứa placeholder sau là rỗng: `TODO`, `TBD`, `Chưa có write-up`, `Coming soon`, `Write-up coming soon` (so sánh không phân biệt hoa thường; cho phép dấu `:` hoặc dấu chấm cuối dòng).
5. File là **có nội dung** nếu sau các bước trên còn ít nhất một ký tự không phải khoảng trắng. Văn bản, lệnh, code, ảnh/link Markdown đều là nội dung. Không đánh giá chất lượng lời giải ở bước đồng bộ.

### 2. Đọc bảng README đúng cấu trúc

Với mỗi README có bảng challenge:

1. Tìm dòng header của bảng chứa cột tên challenge (header chuẩn hóa thành `challenge`, `name`, `exercise`, hoặc `bài`) và cột trạng thái write-up (`writeup`, `solution`, hoặc `writeupstatus`). Dòng phân cách Markdown gồm dấu `-`, `:` và `|` không phải bài.
2. Tách từng dòng bảng theo dấu `|` **không được escape**; `\|` trong nội dung ô không phải dấu phân cột. Dùng chỉ số cột từ header, không giả định bảng luôn có hai cột.
3. Nếu có cột `ID`, `#`, `No`, `Number` hoặc `Challenge ID`, đó là cột định danh riêng, không phải tên challenge. Cột `Challenge`/`Name` mới là tên. Nếu header không phân biệt được cột tên hoặc trạng thái, dừng cập nhật bảng đó và báo cần làm rõ cấu trúc.
4. Tên challenge là nhãn hiển thị của Markdown link trong ô tên; nếu không có link, dùng toàn bộ nội dung ô sau khi bỏ code ticks, HTML tags và khoảng trắng đầu/cuối. Không lấy URL challenge làm nhãn tên.
5. Giữ nguyên toàn bộ ô khác, nhất là URL challenge, ID, thứ tự bài và tên hiển thị.

### 3. Ánh xạ tên challenge với thư mục

Tạo danh sách candidate từ các thư mục trong cây con của README danh mục. Một candidate là thư mục chứa trực tiếp `write-up.md`; candidate có thể ở nhiều cấp thư mục. Không dùng thư mục `.git`, `skill-ctf-writeup-sync` hoặc thư mục không thuộc danh mục đang xử lý. Với mỗi dòng, áp dụng các bước sau theo thứ tự và chỉ nhận kết quả nếu có đúng một candidate:

1. **Đích write-up đã có trong ô trạng thái:** nếu ô trạng thái chứa link tương đối tới `write-up.md`, resolve từ thư mục của README. Chỉ nhận nếu file tồn tại, nằm trong repository và thuộc cây challenge đang xét. Link này là bằng chứng ánh xạ mạnh nhất; nếu trỏ ra ngoài phạm vi hoặc file mất, báo lỗi và không tự thay đích.
2. **Tên chuẩn hóa chính xác:** lấy tên challenge; chuẩn hóa cả tên này và tên thư mục bằng: Unicode NFKD → bỏ dấu kết hợp → lowercase invariant → bỏ mọi ký tự không phải chữ hoặc số. Giữ nguyên chữ số. Vì khoảng trắng, `_`, `-`, dấu chấm, dấu nháy và dấu câu đều bị bỏ, `Modular Exponentiation`, `Modular_Exponentiation` và `MODULAR-EXPONENTIATION` cùng thành `modularexponentiation`.
3. **URL challenge khớp tên thư mục:** chỉ khi bước 2 không có candidate, lấy riêng path segment cuối của URL ở ô tên challenge, URL-decode đúng một lần, bỏ phần query/fragment; chuẩn hóa segment theo cùng quy tắc. Chỉ nhận khi khớp chính xác đúng một candidate. Không dùng host, ID số hoặc một phần slug làm bằng chứng độc lập.
4. **Alias được xác nhận:** chỉ dùng alias đã được người dùng xác nhận hoặc file tùy chọn ở repository root `challenge-aliases.csv` mà người dùng chấp thuận. CSV phải có header `readme,challenge_id,challenge,directory`; `readme` là đường dẫn README danh mục từ root, `directory` là đường dẫn thư mục challenge từ root. Nếu `challenge_id` có giá trị, chỉ khớp đúng ID trong cột ID; nếu để trống, khớp tên challenge sau chuẩn hóa. Thư mục đích phải nằm trong danh mục đó và có `write-up.md`. Nhiều alias khớp hoặc file CSV sai header là lỗi cần báo, không tự chọn. Không suy diễn alias chỉ vì tên “trông giống nhau”.
5. Nếu các bước cho ra nhiều candidate, không chọn candidate đầu tiên, không chọn theo thứ tự alphabet và không dùng fuzzy matching để tự sửa. Ghi README, tên/ID bài và các candidate tương đối rồi bỏ qua dòng đó.
6. Nếu không có candidate, giữ nguyên trạng thái và ghi nhận không ánh xạ được. Không tạo thư mục hoặc write-up trong lệnh `Cập nhập wu`.

Không gộp hai dòng challenge khác ID chỉ vì tên chuẩn hóa giống nhau. Nếu một bảng có ID và tên trùng, dùng ID/URL để phân biệt; nếu không thể phân biệt bằng bằng chứng hiện có, hỏi người dùng.

### 4. Cập nhật duy nhất ô write-up

Sau khi ánh xạ chắc chắn:

- Nếu file đích có nội dung theo quy tắc bước 1, thay **chỉ ô write-up** bằng `[Đọc write-up](<đường-dẫn-tương-đối>)`.
- Nếu file đích rỗng/thiếu, đặt trạng thái `Chưa có write-up`, trừ khi ô hiện tại có một liên kết ngoài hợp lệ hoặc trạng thái đặc biệt cần giữ; không xóa liên kết ngoài khi không có bằng chứng thay thế.
- Tạo link Markdown tương đối từ README đến `write-up.md`, dùng dấu `/`; encode ký tự dành riêng trong path nếu cần. Trước khi ghi link, resolve link như GitHub Markdown và kiểm tra file đích tồn tại.
- Không thay URL challenge ở ô tên, ID, cột khác, dấu câu hoặc nhãn tên. Khi ghi lại row, giữ nguyên từng ô ngoài ô write-up và giữ đúng thứ tự cột.
- Chỉ tự chuyển `Chưa có write-up` thành link khi file đã được phân loại có nội dung. Không sửa nội dung `write-up.md` trong quy trình đồng bộ.

### 5. CryptoHack: Course và Challenges

1. Course là nguồn write-up chính cho bài đã có trong Course. Không tạo bản sao write-up trong `Challenges`.
2. Khi tên bài trong Challenges chuẩn hóa trùng duy nhất với một bài trong Course, ghi `Đang nằm ở course [Tên course](<link README course>)` trong ô write-up của Challenges. Giữ nguyên URL challenge và các ô còn lại.
3. Nếu bài Course có write-up rỗng/thiếu, trạng thái Challenges vẫn là `Đang nằm ở course ...` để tránh tạo bản sao; bài đó chưa được tính hoàn thành.
4. Nếu một bài trong Challenges có thư mục/write-up riêng và không có Course write-up tương ứng, áp dụng đồng bộ write-up bình thường.
5. Nếu bài có ở nhiều Course, chỉ tự liên kết khi README/URL/alias xác định duy nhất course. Nếu không, báo các course ứng viên và hỏi người dùng.
6. Khi tính tiến độ cho một dòng `Đang nằm ở course`, resolve link tới README Course, tìm đúng một dòng challenge Course bằng ID nếu có, nếu không thì bằng tên chuẩn hóa; tính hoàn thành khi dòng Course đó trỏ tới write-up nội bộ có nội dung hoặc một write-up ngoài được ghi rõ là đã có. Không tính chỉ vì README Course tồn tại.

### 6. Others-Events khi README event chưa có bảng

Áp dụng cho README bên trong `Others-Events` có thư mục challenge nhưng chưa có bảng challenge:

1. Chỉ xem đây là README event nếu nó có challenge folder ở cây con; bỏ qua README điều hướng chỉ liệt kê năm/event con.
2. Một challenge folder phải có trực tiếp `write-up.md` hoặc `solve.py`. Duyệt đệ quy. Nếu một folder có README con chứa bảng challenge riêng, không kéo các bài của README con lên bảng cha.
3. Mỗi challenge folder chỉ tạo một dòng. Tên mặc định là basename folder; nếu README hiện tại đã có mục/link tới folder đó với tên hiển thị khác thì dùng nhãn sẵn có. Giữ nguyên tên folder và không đổi tên file.
4. Thêm bảng ở cuối README, trước đó một dòng trống:
   `| Challenge | Write-up |`
   `| --- | --- |`
5. Với mỗi folder, link nội bộ tương đối tới write-up nếu file có nội dung; nếu không thì ghi `Chưa có write-up`. Nếu chỉ có `solve.py` mà chưa có `write-up.md`, không tự tạo file trong đồng bộ; báo file write-up thiếu.
6. Duy trì các dòng bảng đã có; không tạo bảng thứ hai nếu README đã có một bảng challenge. Với bảng hiện hữu, cập nhật theo các quy tắc parse/map ở trên.

### 7. Tính lại số hoàn thành ở README cha và README gốc

1. Tổng số của một mục là số data row trong bảng challenge của README được link, sau khi bỏ header và separator. Bảng nhiều cột vẫn đếm một row là một bài; ID không làm tăng số bài.
2. Bài đã hoàn thành nếu ô write-up là một trong các trường hợp: (a) link nội bộ tới `write-up.md` có nội dung; (b) link write-up ngoài được giữ rõ ràng trong ô trạng thái; (c) trạng thái Course được resolve theo bước 5. Không tính `Chưa có write-up`, file rỗng, file chỉ có heading/placeholder, link hỏng hoặc dòng chưa ánh xạ chắc chắn.
3. Với mỗi link README có hậu tố tiến độ `(x/y)`, tính lại từ bảng challenge đích và thay đúng hai số trong hậu tố; không sửa link path hoặc nhãn.
4. Áp dụng việc tính lại đệ quy cho README cha có các link con mang hậu tố tiến độ, rồi kiểm tra README gốc. Không tự thêm số cho link cha chưa dùng định dạng này, trừ khi người dùng yêu cầu.
5. Giữ nguyên thứ tự độ khó và cấu trúc danh sách lồng nhau. `Others-Events` luôn là nền tảng cuối trong README gốc.

### 8. Kiểm tra sau đồng bộ

Trước khi kết thúc, kiểm tra và báo rõ các trường hợp không giải quyết được:

1. Mỗi link `[Đọc write-up](...)` nội bộ mới/cũ trong phạm vi resolve tới file tồn tại; link ngoài được giữ riêng, không coi URL ngoài là đường dẫn file nội bộ.
2. Mỗi dòng có `[Đọc write-up]` có file đích với nội dung theo bước 1; mỗi file nội bộ có nội dung ánh xạ chắc chắn được phản ánh trong đúng bảng.
3. Không còn dòng `Chưa có write-up` có thể ánh xạ duy nhất tới file write-up có nội dung.
4. Tổng số và số hoàn thành trong mọi hậu tố `(x/y)` khớp bảng đích; `x` không lớn hơn `y`.
5. Các URL challenge, ID, tên bài, thứ tự dòng, file write-up có sẵn và các thay đổi không thuộc phạm vi vẫn được giữ nguyên.
6. Báo số bảng/dòng đã cập nhật, số tiến độ đã sửa, và danh sách bài thiếu write-up hoặc mapping mơ hồ. Không tuyên bố đã đồng bộ hoàn toàn nếu còn mapping cần người dùng xác nhận.

## Lệnh người dùng: `Tạo folder web ...`

1. Lấy đúng tên website, thứ tự nền tảng/nhóm/độ khó/category và phạm vi challenge từ yêu cầu, website chính thức hoặc dữ liệu người dùng gửi. Đừng tự đổi thứ tự độ khó. Thêm nền tảng vào README gốc ngay trước `Others-Events`, trừ khi người dùng chỉ định vị trí khác.
2. Lập danh sách challenge có cấu trúc trước khi tạo file: tên hiển thị, ID nếu có, URL chính thức, danh mục, thư mục cha. Nếu website chặn bot, dùng ảnh/danh sách người dùng cung cấp; không đoán các dòng bị khuất. Hỏi người dùng nếu phần thiếu ảnh hưởng danh sách cần tạo.
3. Tạo README điều hướng cho website, nhóm và từng danh mục. Tạo bảng challenge giữ tên/URL chính thức; mỗi bài chưa có lời giải ghi `Chưa có write-up`.
4. Trong đúng thư mục danh mục, gọi `autocreatemyfolder` đúng một lần cho từng challenge chưa tồn tại; truyền nguyên tên challenge cho helper, để helper tự chuẩn hóa tên. Không tự mô phỏng quy tắc chuẩn hóa bằng script khác.
5. Dùng Ubuntu WSL với shell tương tác vì `autocreatemyfolder` là function được nạp từ cấu hình shell. Trước batch, chạy `type autocreatemyfolder`; nếu không tồn tại thì dừng và báo, không thay bằng thao tác tạo file khác.
6. Không ghép trực tiếp tên challenge vào mã shell. Truyền từng tên như một giá trị dữ liệu đã quote an toàn (ví dụ danh sách UTF-8 qua stdin/base64 rồi đọc từng dòng trong bash); bên trong bash chỉ gọi `autocreatemyfolder "$title"`. Đặt working directory rõ ràng và kiểm tra trước khi chạy.
7. Nếu folder bài đã tồn tại, không chạy helper mù quáng và không ghi đè; kiểm tra `solve.py`, `write-up.md` và tích hợp file hiện có. Không xóa hoặc làm trống write-up có nội dung.
8. Sau khi tạo, xác minh mỗi challenge có đúng một folder và có `solve.py` cùng `write-up.md`; xác minh link README, tổng row, thứ tự mục và số liệu tiến độ.

## Quy tắc viết write-up

- Chỉ giải bài khi người dùng yêu cầu. Đọc đề và tài nguyên; không đoán flag hoặc kết quả.
- Viết các bước tái hiện được; giữ `solve.py` đồng bộ nếu được yêu cầu. Dùng ngôn ngữ/phong cách file hiện có. Khi chỉ yêu cầu link hoặc xuống dòng, không viết lại câu chữ.
- Công thức phải tương thích GitHub KaTeX; đặt khối `$$` riêng dòng và tránh lồng cú pháp Markdown không được hỗ trợ trong math mode.

## An toàn thay đổi

- Đọc file và kiểm tra tình trạng trước khi sửa; bảo toàn thay đổi người dùng có sẵn.
- Không xóa/ghi đè nội dung hoặc sửa file ngoài phạm vi. Nếu file đích đã có nội dung, tích hợp thay vì thay mới.
- Không tạo commit trừ khi người dùng yêu cầu rõ.
