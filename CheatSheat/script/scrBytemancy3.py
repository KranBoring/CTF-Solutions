from pwn import *
#main
io = remote("green-hill.picoctf.net", 51480)

symbol = {
    b"astral_spark":0x080491c1,
    b"binding_word":0x080491e3,
    b"glyph_conflux":0x0804919a,
    b"ember_sigil":0x08049176,
    b"frame_dummy":0x08049170
}
for i in range(3):
    mess = io.recvuntil(b"procedure '")
    sym = io.recvuntil(b"'",drop=True)
    io.send(p32(symbol[sym]))
io.interactive()
io.close()