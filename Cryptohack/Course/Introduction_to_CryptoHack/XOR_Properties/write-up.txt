Bài này cung cấp cho ta 4 đoạn hex string và cách chúng tạo ra:
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf

Và đề cung cấp hint như sau:
Commutative: A ⊕ B = B ⊕ A
Associative: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
Identity: A ⊕ 0 = A
Self-Inverse: A ⊕ A = 0

*Commutative means that the order of the XOR operations is not important

Cách giải:
Khi xor 2 chuỗi bit giống nhau thì kết quả trả về sẽ là 0, và khi 0 xor với chuỗi bit thì trả về đúng chuỗi bit đó và mục tiêu của chúng ta là khôi phục lại flag.
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
Vì FLAG đã xor với 3 key khác nhau, nên ta cần cả 3 key để xor đảo ngược lại ra FLAG
Giải thích:
FLAG ^ KEY1 ^ KEY3 ^ KEY2 ^ (KEY1 ^ KEY2 ^ KEY3) = FLAG ^ (KEY1 ^ KEY1) ^ (KEY2 ^ KEY2) ^ (KEY3 ^ KEY3) = FLAG ^ 0 ^ 0 ^ 0 = FLAG
Script: solve.py
#Flag:crypto{x0r_i5_ass0c1at1v3}

