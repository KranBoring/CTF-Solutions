from CTF_Crypto_Attack.Hash.length_extension_attack import new
import requests
url = "http://w01.ctf.chronos-security.ro:36762/api/command"
data = {"message_hex":"73746174696f6e3d454153544c494e4b2d313126636d643d5354415455532674733d31373638363539393338266e6f6e63653d3731373163383236","sig":"7162d694436136a7dbae03fbbd948b9dd3cfd3fa8f840a76d61f959bcc9c19aa"}
message_bytes = bytes.fromhex(data['message_hex'])
sig = data['sig']
cmd_to_add = b"&cmd=DISPATCH"
for key_len in range(8, 33):
    sha = new('sha256')
    payload_message, payload_sig = sha.extension(key_len, message_bytes, cmd_to_add, sig)
    payload = {'message_hex': payload_message.hex(),'sig': payload_sig}
    print(f"Key_length = {key_len}\n{payload_message}\n{payload_sig}")
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        print(res.text)
        break