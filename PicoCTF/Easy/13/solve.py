import codecs

ciphertext = "npnqrzl{abg_gbb_onq_bs_n_ceboyrz}"
flag = codecs.decode(ciphertext, "rot_13")
print(flag)