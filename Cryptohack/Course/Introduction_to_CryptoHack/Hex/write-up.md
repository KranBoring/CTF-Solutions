# Hex

Bài cung cấp 1 đoạn cờ bị chuyển sang mã hex string
Trong python có hàm bytes.fromhex("<hex string>") nhận vào 1 chuỗi hex string đổi sang bytes thì quá trình chuyển đổi của nó như sau:
B1: Tách mỗi 2 kí tự có trong hex string (Nếu như hàm nhận vào 1 đoạn hex string lẻ thì sẽ bị lỗi)
B2: mỗi 1 kí tự hex sẽ chiếm 4 bit nên 2 kí tự hex sẽ chiếm 1 bytes bộ nhớ, khi in ra, ram sẽ đẩy giá trị bytes đó lên và đổi sang demical 
B3: Đổi sang mã chữ ASCII để in ra terminal
-> Và ta thu được cờ!

#### Flag:crypto{You_will_be_working_with_hex_strings_a_lot}

