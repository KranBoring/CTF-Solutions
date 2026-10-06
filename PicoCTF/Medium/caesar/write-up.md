# caesar

#### Category: Crypto - Diff: Medium

#### 1. Overview

* ![image-20261006092851363](images/image-20261006092851363.png)
* Đây là bài kinh điển của mã hóa caesar
* `Mục tiêu`: Giải mã nội dụng của cờ
* `Kỹ thuật`: Brute Force

#### 2. Nền tảng cốt lõi

* Mã hóa caesar [Đọc](https://learncryptography.com/classical-encryption/caesar-cipher)

#### 3. Phân tích

* Khi mở file data.enc lên, ta có thể thấy nội dung của cờ đã bị mã hóa
* ![image-20261006093102769](images/image-20261006093102769.png)
* Dựa vào tên bài, ta có thể biết được rằng đây là mã hóa dịch chuyển kí tự

#### 4. Ý tưởng khai thác 

* Vì bài này chỉ là mã hóa carsar thông thường, nên ta sẽ bruteforce không gian khóa

#### 5. Exploit chain

* Quy trình:

  * Lấy nội dung trong cờ
  * Bruteforce 26 khóa đơn kí tự
  * Chọn ra nội dung phù hợp

* Script: [Đọc](solve.py)

* Kết quả:

* ```wiki
  academy{xmjnndiboczmpwdxjiqaptvumw}
  
  academy{ynkooejcpdanqxeykjrbquwvnx}
  
  academy{zolppfkdqeboryfzlkscrvxwoy}
  
  academy{apmqqglerfcpszgamltdswyxpz}
  
  academy{bqnrrhmfsgdqtahbnmuetxzyqa}
  
  academy{crossingtherubiconvfuyazrb} #############################################################
  
  academy{dspttjohuifsvcjdpowgvzbasc}
  
  academy{etquukpivjgtwdkeqpxhwacbtd}
  
  academy{furvvlqjwkhuxelfrqyixbdcue}
  
  academy{gvswwmrkxlivyfmgsrzjycedvf}
  
  academy{hwtxxnslymjwzgnhtsakzdfewg}
  
  academy{ixuyyotmznkxahoiutblaegfxh}
  
  academy{jyvzzpunaolybipjvucmbfhgyi}
  
  academy{kzwaaqvobpmzcjqkwvdncgihzj}
  
  academy{laxbbrwpcqnadkrlxweodhjiak}
  
  academy{mbyccsxqdrobelsmyxfpeikjbl}
  
  academy{nczddtyrespcfmtnzygqfjlkcm}
  
  academy{odaeeuzsftqdgnuoazhrgkmldn}
  
  academy{pebffvatgurehovpbaishlnmeo}
  
  academy{qfcggwbuhvsfipwqcbjtimonfp}
  
  academy{rgdhhxcviwtgjqxrdckujnpogq}
  
  academy{sheiiydwjxuhkrysedlvkoqphr}
  
  academy{tifjjzexkyvilsztfemwlprqis}
  
  academy{ujgkkafylzwjmtaugfnxmqsrjt}
  
  academy{vkhllbgzmaxknubvhgoynrtsku}
  
  academy{wlimmchanbylovcwihpzosutlv}
  ```

* #### Flag: academy{crossingtherubiconvfuyazrb}

