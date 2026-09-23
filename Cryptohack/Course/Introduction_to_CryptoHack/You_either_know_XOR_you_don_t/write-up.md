# You either know, XOR you don't 

Baì này cung cấp 1 đoạn hex string và ... ko còn gì nữa
Đề yêu cầu chúng ta giải mã đoạn hex string và không có key
Hint: Remember the flag format and how it might help you in this challenge!

Theo như chúng ta được biết:
Khi ta xor plaintext với key sẽ tạo ra ciphertext
plaintext ^ key = ciphertext
Nhưng chúng ta hiện tại chỉ có ciphertext và hint nói rằng có thể plaintext giống với flag format của web, vì vậy trước hết chúng ta cần có cái nhìn về key đã, nếu chúng ta đảo ngược phép xor lại
plaintext ^ ciphertext = key !!!
Format của cờ là crypto{...}, vì vậy chúng ta biết 7 kí tự đầu của plaintext và kí tự cuối cùng của plaintext.
Khi xor phần plaintext đầu với 14 kí tự hex đầu của ciphertext và phần plaintext cuối với 2 kí tự hex cuối cùng của ciphertext ta thu được 2 phần key
"myXORke" và "y"
Ta tinh ý sẽ phát hiện ra ngay là khi ghép cả 2 phần lại với nhau, ta sẽ thu được 1 key hoàn chỉnh là "myXORkey"
Và bây giờ chỉ là ta xor ciphertext với key để thu được flag
Script:solve.py

#### Flag:crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}
