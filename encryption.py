from Crypto.Cipher import AES
import os
from dotenv import load_dotenv

# โหลดค่าจาก .env
load_dotenv()

# อ่านค่า KEY และ IV จาก environment variables
SECRET_KEY = os.getenv('SECRET_KEY').encode()
IV = os.getenv('IV').encode()

def encrypt_data(data: bytes) -> bytes:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    
    # Padding
    padding = 16 - (len(data) % 16)
    data += bytes([padding]) * padding
    
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data: bytes) -> bytes:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # ลบ Padding
    padding = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding]
    
    return decrypted_data

def encrypt_mode():
    input_file = input("📁 กรุณาใส่ชื่อไฟล์ที่ต้องการเข้ารหัส: ").strip()
    
    if not os.path.exists(input_file):
        print("❌ ไม่พบไฟล์ที่ต้องการเข้ารหัส")
        return
    
    # เปลี่ยนนามสกุลเป็น .bin
    output_file = os.path.splitext(input_file)[0] + ".bin"
    
    try:
        with open(input_file, "rb") as f:
            file_data = f.read()
        
        encrypted_data = encrypt_data(file_data)
        
        with open(output_file, "wb") as f:
            f.write(encrypted_data)
        
        print(f"✅ ไฟล์ถูกเข้ารหัสแล้ว: {output_file}")
    
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {str(e)}")

def decrypt_mode():
    input_file = input("📁 กรุณาใส่ชื่อไฟล์ที่ต้องการถอดรหัส: ").strip()
    
    if not os.path.exists(input_file):
        print("❌ ไม่พบไฟล์ที่ต้องการถอดรหัส")
        return
    
    # กำหนดชื่อไฟล์ output โดยเติม _decrypted
    output_file = os.path.splitext(input_file)[0] + "_decrypted" + os.path.splitext(input_file)[0][-4:]
    
    try:
        with open(input_file, "rb") as f:
            encrypted_data = f.read()
        
        decrypted_data = decrypt_data(encrypted_data)
        
        with open(output_file, "wb") as f:
            f.write(decrypted_data)
        
        print(f"✅ ไฟล์ถูกถอดรหัสแล้ว: {output_file}")
    
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {str(e)}")

if __name__ == "__main__":
    print("🔐 โปรแกรมเข้ารหัส/ถอดรหัสไฟล์")
    print("1. เข้ารหัสไฟล์ (Encrypt)")
    print("2. ถอดรหัสไฟล์ (Decrypt)")
    
    choice = input("📌 กรุณาเลือก (1 หรือ 2): ").strip()
    
    if choice == "1":
        encrypt_mode()
    elif choice == "2":
        decrypt_mode()
    else:
        print("❌ ตัวเลือกไม่ถูกต้อง")
