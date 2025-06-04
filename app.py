from flask import Flask, render_template, request
from Crypto.Cipher import DES3
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher.DES3 import adjust_key_parity
import base64

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
def encrypt_3des_with_steps(plaintext):
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
        step['xor_input'] = base64.b64encode(xor_input).decode('utf-8')

        c1 = DES.new(key[:8], DES.MODE_ECB).encrypt(xor_input)
        step['des1'] = base64.b64encode(c1).decode('utf-8')

        c2 = DES.new(key[8:16], DES.MODE_ECB).decrypt(c1)
        step['des2'] = base64.b64encode(c2).decode('utf-8')

        c3 = DES.new(key[16:24], DES.MODE_ECB).encrypt(c2)
        step['des3'] = base64.b64encode(c3).decode('utf-8')

        prev = c3
        steps.append(step)

    return {
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'key': base64.b64encode(key).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8'),
        'steps': steps
    }

# Decrypt ciphertext using 3DES in CBC mode
def decrypt_3des(ciphertext_b64, key_b64, iv_b64):
    # Fail early if the provided data isn't valid base64
    key = base64.b64decode(key_b64, validate=True)
    iv = base64.b64decode(iv_b64, validate=True)
    ciphertext = base64.b64decode(ciphertext_b64, validate=True)

    if len(key) not in (16, 24):
        raise ValueError('Invalid key length')
    if len(iv) != 8:
        raise ValueError('Invalid IV length')

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
            result = encrypt_3des_with_steps(plaintext)
            result['mode'] = 'encrypt'
            result['input'] = plaintext
        elif action == 'decrypt':
            ciphertext = request.form.get('ciphertext')
            key = request.form.get('key')
            iv = request.form.get('iv')
            try:
                plaintext = decrypt_3des(ciphertext, key, iv)
                result = {
                    'mode': 'decrypt',
                    'input': ciphertext,
                    'key': key,
                    'iv': iv,
                    'plaintext': plaintext
                }
            except Exception as e:
                result = {'error': str(e)}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
