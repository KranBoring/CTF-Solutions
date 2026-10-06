# Flags

#### Category: Crypto - Diff: Medium

#### 1. Overview

* ![image-20261006124217580](images/image-20261006124217580.png)
* Bài này thì chúng ta sẽ giải cờ bằng cờ :dancer:
* `Mục tiêu`: Giải mã bức ảnh `flags`

#### 2. Nền tảng cốt lõi

* International codes of signals flags: [Đọc](https://en.wikipedia.org/wiki/International_maritime_signal_flags)

#### 3. Phân tích/Exploit chain

* Đề cho ta 1 tấm ảnh chứa các cờ khác nhau:

* ![image-20261006124440567](images/image-20261006124440567.png)

* Chúng ta dễ dàng nhận ra 6 cờ đầu là `PICOCTF`, nếu đối chiếu thêm trong dấu `{}` thì chúng ta còn biết thêm `{F????????T?FF}`

* Mình cứ nghĩ những flags có khi được tượng hình cho các chữ cái +)))), mình thử thay lá cờ X bằng chữ X, lá cờ có dạng giống chữ K, nhưng cách này không khả thi thì cờ mình giải ra là 1 đoạn nội dung vô nghĩa

* Khi mình search thử `flags alphabet` thì mình có nhận được cái này:

* ![image-20261006124846128](images/image-20261006124846128.png)

* Mình click vào trang Flagdom để xem thử được bảng này:

* ![image-20261006124855811](images/image-20261006124855811.png)

* Mình nghĩ rằng là bài này đến đây là hết nhưng không, lúc mình đối chiếu với các cờ để giải mã thì mình thiếu 2 lá cờ chưa biết là:

* ![image-20261006125223172](images/image-20261006125223172.png)![image-20261006125237117](images/image-20261006125237117.png)

* Lúc này cờ đang có dạng `PICOCTF{F?LAG?AND?TUFF}` nên mình mạnh dạn đoán cờ đầu tiên là chữ `L` và cờ dấu X là kí tự `_` =))))

* Nhưng cờ vẫn sai, mình có thử thay `_` thành dấu cách, thay thành chữ S vì nó cũng có nghĩa nhưng không thành

* MÌnh thấy mục hiện tại của trang web là ![image-20261006125511687](images/image-20261006125511687.png)

* `International code of signals flags`

* Mình thử tra trang web khác thì nhận được trang wikipedia ở đầu trang =))

* ![image-20261006125607116](images/image-20261006125607116.png)

* Và bùm ![image-20261006125622630](images/image-20261006125622630.png)

* #### Flag: PICOCTF{F1AG5AND5TUFF}