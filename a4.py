import qrcode
import hmac 
import base64
import struct
import hashlib 
import time

# .\venv\Scripts\activate

def get_qr_code():
    label = "user"
    user = "user1@gmail.com"
    key = "JBSWY3DPEHPK3PXP"
    digits = "10"
    period = "30"
    return "otpauth://totp/" + label + ":" + user + "?secret=" + key + "&issuer=" + label + "&digits=" + digits

def countdown(t):
    print("Password is: " + get_TOTP("JBSWY3DPEHPK3PXP"))
    while t:
        secs = t % 30
        timer = '{:02d}'.format( secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        if secs == 0: 
             print("Password is: " + get_TOTP("JBSWY3DPEHPK3PXP"))
    

def generateTOTP(key, time, returnDigits):
    
    
    # https://programtalk.com/python-examples/base64.b32decode/
    # https://datatracker.ietf.org/doc/html/rfc6238?fbclid=IwAR2ZaOsOfbTNaKIU7vHL6N6bDqiOdevq8_EzV3rPZmkmdT4o4ud-QsauAew
    
     codeDigits = base64.b32decode(key)
     
     
     # using the counter 
     # First 8 bytes are for the movingFactor 
     # Compliant with base RFC 4226 (HOTP)
    
     counter = struct.pack('>Q', time)
     
     hash = hmac.new(codeDigits, counter, hashlib.sha1).digest()
     
     
     offset = hash[len(hash) - 1] & 0xf;
     
     # Progress reminder: need to slice the byte to 4 
     binary = (struct.unpack(">L", hash[offset:offset+4])[0] & 0x7fffffff); # format character: unsigned longxxxx
                                                                  
     return str(binary)[-returnDigits:]
    

def get_TOTP(secret):
    intervals_no=int(time.time())//30
    return generateTOTP(secret, intervals_no, 6)

input_data = get_qr_code()
# print("data" + input_data)

# Creating an instance of qrcode
qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
qr.add_data(input_data)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
img.save('qrcode001.png')
print("QR code is generated successfully.")



# Print the TOTP password in a loop 
timer_test = int(time.time())//30
countdown(timer_test)