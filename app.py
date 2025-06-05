from flask import Flask, render_template, request
from Crypto.Cipher import DES3
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher.DES3 import adjust_key_parity
import base64
import binascii


def encode_data(data: bytes, fmt: str) -> str:
    if fmt == 'hex':
        return data.hex()
    return base64.b64encode(data).decode('utf-8')


def decode_data(data_str: str, fmt: str) -> bytes:
    if fmt == 'hex':
        return bytes.fromhex(data_str)
    return base64.b64decode(data_str)

app = Flask(__name__)

def generate_3des_key():
    while True:
        key = get_random_bytes(24)
        try:
            key = adjust_key_parity(key)
            DES3.new(key, DES3.MODE_ECB)
            return key
        except ValueError:
            continue

# Encrypt plaintext using 3DES in CBC mode with step tracking
def encrypt_3des_with_steps(plaintext, out_format: str = 'base64'):
    key = generate_3des_key()
    iv = get_random_bytes(8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded_text = pad(plaintext.encode('utf-8'), DES3.block_size)
    ciphertext = cipher.encrypt(padded_text)

    steps = []
    blocks = [padded_text[i:i+8] for i in range(0, len(padded_text), 8)]
    prev = iv

    for block in blocks:
        step = {}
        xor_input = bytes(a ^ b for a, b in zip(block, prev))
        step['xor_input'] = encode_data(xor_input, out_format)

        c1 = DES.new(key[:8], DES.MODE_ECB).encrypt(xor_input)
        step['des1'] = encode_data(c1, out_format)

        c2 = DES.new(key[8:16], DES.MODE_ECB).decrypt(c1)
        step['des2'] = encode_data(c2, out_format)

        c3 = DES.new(key[16:24], DES.MODE_ECB).encrypt(c2)
        step['des3'] = encode_data(c3, out_format)

        prev = c3
        steps.append(step)

    return {
        'ciphertext': encode_data(ciphertext, out_format),
        'key': encode_data(key, out_format),
        'iv': encode_data(iv, out_format),
        'steps': steps
    }

# Decrypt ciphertext using 3DES in CBC mode
def decrypt_3des(ciphertext_str, key_str, iv_str, in_format: str = 'base64'):
    key = decode_data(key_str, in_format)
    iv = decode_data(iv_str, in_format)
    ciphertext = decode_data(ciphertext_str, in_format)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_padded, DES3.block_size).decode('utf-8')
    return plaintext

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'encrypt':
            plaintext = request.form.get('plaintext')
            out_fmt = request.form.get('enc_format', 'base64')
            result = encrypt_3des_with_steps(plaintext, out_fmt)
            result['mode'] = 'encrypt'
            result['input'] = plaintext
            result['fmt'] = out_fmt
        elif action == 'decrypt':
            ciphertext = request.form.get('ciphertext')
            key = request.form.get('key')
            iv = request.form.get('iv')
            in_fmt = request.form.get('dec_format', 'base64')
            try:
                plaintext = decrypt_3des(ciphertext, key, iv, in_fmt)
                result = {
                    'mode': 'decrypt',
                    'input': ciphertext,
                    'key': key,
                    'iv': iv,
                    'plaintext': plaintext,
                    'fmt': in_fmt
                }
            except Exception as e:
                result = {'error': str(e)}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
