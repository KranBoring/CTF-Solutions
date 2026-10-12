# Lo-Hi Card Game

#### Cryptohack - Challenges: Misc

#### 1. Overview

* Đây là 1 bài Crypto/Misc và nằm trong mục `PRNGs`. Đây là 1 dạng bài crack bộ sinh số giả ngẫu nhiên để lấy được cờ. Ý tưởng triển khai bài này, cũng như cách bài này để lộ ra vấn đề bảo mật khá là hay =)))). Đây là bài thứ 2 mình giải liên quan đến bộ sinh số giả ngẫu nhiên sau bài `nLCG`. Các bạn có thể xem tại mục `Event -> 2026 -> Wannagame recruit 2026`. Và đây cũng là task bài tập mà anh `Nhan_Laptop` đã giao cho k25 (mình k26 nhưng mình muốn làm task k25 :v)
* `Mục tiêu`: Trong vòng 200 round, đánh thắng nhà cái và có tổng tiền nhận về lớn hơn 130 đô là nhân được cờ
* `Lỗ hỗng`: Các lá bài được rút một cách giả ngẫu nhiên
* `Kỹ thuật`: Đại số tuyến tinh trên trường module để khôi phục lại các thành phần sinh số

#### 2. Nền tảng cốt lõi

* Các bạn cần nắm được các lý thuyết số cơ bản như module, nghịch đảo module.
* Có kiến thức về giải hệ phương trình (Cơ bản là Đại số tuyến tính)
* Kiến thức cơ bản về `LCG`: [Đọc](https://en.wikipedia.org/wiki/Linear_congruential_generator)
* Luật chơi cơ bản của High Low card game: [Đọc](https://www.quora.com/What-are-the-rules-of-the-High-Low-card-game)

#### 3. Phân tích lỗ hỗng

* Khi netcat đến server. Server sẽ phát cho chúng ta 20 đô tiền gốc, 1 lá bài , và bắt chúng ta dự đoán xem, lá bài tiếp theo có giá trị cao hay thấp hơn lá cờ mình đang giữ.
* Nếu bạn đoán đúng, bạn nhận 1 đô
* Nếu bạn đoán sai, bạn pay 2 đô
* Sau mỗi round, lá bài tiếp theo sẽ trở thành là bài hiện tại của chúng ta, và ta tiếp tục dự đoán lá bài bí ẩn tiếp theo.
* Tiếp theo là về source code. Ta có thể thấy được ngay ở class đầu tiên của chương trình được khai báo là `RNG`
* ```Python
  class RNG:
      mul = random.getrandbits(60)
      inc = random.getrandbits(60)
      mod = 2**61 - 1  # 9th mersenne prime

      def __init__(self, seed):
          self.state = seed

      def next(self):
          self.state = (self.state * self.mul + self.inc) % self.mod
          return self.state
  ```
* Thay vì sử dụng các hàm random sẵn có trong thư viên `secret` hay `Crypto.Random`thì server lại chọn cách tính toán ra số tiếp theo dựa trên số hiện tại bằng thuật toán sinh số giả ngẫu nhiên `LCG`
* Sau khi sinh ra 1 số giả ngẫu nhiên, số đó được đưa vào hàm `rebase` ở class `Game` và được lưu vào biến `deals`chứa list các số được tính từ số giả ngẫu nhiên đó. List số đó tính được bằng cách đổi số từ hệ 10 sang hệ 52.
* Ở mỗi lượt rút bài bí ẩn. Index của lá cờ bí ẩn sẽ lấy ra bằng hàm `pop()`trên list số `deals`. Khi `deals`rỗng, tạo ra số giả ngẫu nhiên mới và lặp lại quá trình trên.

#### 4. Ý tưởng khai thác

* Đã hiểu được quá trình các lá bài bí ẩn được chọn như nào, bây giờ ta cần phải khôi phục làm bộ sinh số giả ngẫu nhiên đang hiện có của server.
* Các tham số cho 1 bộ sinh số giả ngẫu nhiên là:
  * `seed`: Hạt giống của quá trình sinh số (Chưa biết)
  * `mul`: Hệ số nhân (Chưa biết)
  * `inc`: Số hạng (Chưa biết)
  * `mod`: Số mod (Đã biết)
* Trong 4 mục trên, ta cần biết nhất là hệ số `mul` và `inc`. `Seed`có lẽ là không cần bởi vì chỉ cần ta biết được trạng thái `state thứ i`thì dựa vào `mul,inc,mod`, ta có thể dự đoán và tính được `state thứ i + 1`
* Để có thể khôi phục được `mul`và `inc`, ta giả sử số giả ngẫu nhiên sinh ra đâu tiên là `x1`, tiếp nối là `x2,x3`
* Khi đó để tính được `mul`, ta đặt `d2,d3` là các delta của `x1,x2` và `x2,x3`
* ![1791821654738](image/write-up/1791821654738.png)
* Khi đã có được `mul`, ta dễ dàng tính được `inc`
* ![1791821769496](image/write-up/1791821769496.png)
* Vì vậy, để có thể khôi phục được bộ sinh số, ta cần phải được 3 trạng thái liên tiếp của bộ sinh.
* Để có thể tính được `x1,x2` và `x3`, ta sẽ feed lên server nhiều nhất là 33 round `(số giả ngẫu nhiên dài 60 bit khi đổi từ hệ 2 sang hệ 52 sẽ có độ dài khoảng 11)`, thu lại các lá bài, sau đó khôi phục lại vị trí của nó trong `desk`, rồi đưa các giá trị ví trí lá bài đó vào đúng thứ tự biểu diễn giống với list `deals` rồi chuyển list đó tự hệ 52 sang lại hệ 10 là ta thu được trạng thái của số giả ngẫu nhiên, với mỗi 11 số liên tiếp là ta thu được 11 trạng thái
* Ta sẽ thử choice ngẫu nhiên cho đến khi đến được tối đa là vòng 33, nếu ít hơn vì tiền hết thì ta sẽ bắt đầu lại cho đến khi thu được 3 số `x1,x2,x3`
* Sau đó là quá trình khôi phục `mul,inc`. Rồi từ round 34 trở đi, ta sẽ tính toán trạng thãi `x4`, rồi sinh ra lại list `deals`để dự đoán lá bài tiếp theo của server và lặp lại cho đến khi nhận cờ

#### 5. Exploit chain

* Quy trình:
  * Feed 33 round đầu
  * Khôi phục lại trạng thái `x1,x2,x3`
  * Tính toán `mul, inc`
  * Trở thành thần bài, không có đối thủ nào có thể đánh bại khi mà mọi lá bài tiếp theo đều năm trong tầm tay =)))))))))
* Script: [Đọc](solve.py)
* Kết quả:
* ```
  You pulled a 21! Here's a flag: crypto{shuffl3_tr4ck1n6_i5_1t_l3g4l?}
  So tran thang:172
  So tran thua:28
  Ty le thang:0.86
  Than bai🔥🔥🔥🔥🔥
  ```
* ```
  crypto{shuffl3_tr4ck1n6_i5_1t_l3g4l?}
  ```
