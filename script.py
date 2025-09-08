import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def aes_128_cbc_decrypt(ciphertext_b64, key_text):
    ciphertext = base64.b64decode(ciphertext_b64)
    
    key = key_text.encode('utf-8')
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes for AES-128")
    
    iv = bytes([0]*16)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return decrypted.decode('utf-8')


headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://ereader2.studora.se/reader/',
    'User-Agent': '', # Generate random UA
    'sec-ch-ua': '', # Generate random sec UA
    'sec-ch-ua-mobile': '?0',

}
def serialize_page(page_number):
    return f"{page_number:04d}"

# Assuming 1000 pages is the maximum
for i in range(1, 1000):
    # Censored book-id
    response = requests.get(f'https://ereader2.studora.se/********/html5/********/OPS/images/page{serialize_page(i)}.svgz', headers=headers)
    if response.status_code != 200:
        print(f"Last page {i} reached. Quitting.")
        break

    key = dump_key("book id here") # I will not be sharing information on how to extract encryption keys
    
    output = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    """

    # We have to do this as after decryption <?xml is completely broken, so just replace it :-)
    output += "<?xml version='1.0'" + aes_128_cbc_decrypt(response.text, key)[20:] + "\n\n"

    output += """
    </body>
    </html>"""

    with open(f"page_{i}.html", "w", encoding="utf-8") as file:
        file.write(output)
        print(f"Decrypted page {i}!")

print("Done")
