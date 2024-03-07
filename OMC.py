import datetime
from cryptography.fernet import Fernet
import os
import subprocess
import time
import shutil

key = b'T1NySQTocKZ2Fd03Hmw1HJKf7mjYuFiR-l8bndWeylg='
cipher_suite = Fernet(key)
key_enc = "key.enc"

# 儲存新到期加密日
def save_activation_date(expiration_date):
    encrypted_date = cipher_suite.encrypt(expiration_date.strftime("%Y-%m-%d %H:%M:%S").encode())
    with open(key_enc, "wb") as file:
        file.write(encrypted_date)

# 讀取到期加密日
def get_activation_date():
    if os.path.exists(key_enc):
        with open(key_enc, "rb") as file:
            encrypted_date = file.read()
            decrypted_date = cipher_suite.decrypt(encrypted_date)
            expiration_date = datetime.datetime.strptime(decrypted_date.decode(), "%Y-%m-%d %H:%M:%S")
            return expiration_date
    else:
        pw = str(input('Press Enter.'))
        if (pw == 'jasper100'):
            with open(r'date.txt', 'r') as file:
                date_str = file.readline().strip()
                expiration_date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                print('Update expiration date:', expiration_date)
            save_activation_date(expiration_date)
        else:
            expiration_date = datetime.datetime(2001,1,1)
            print('No key.enc file.')
        
        return expiration_date
    
def find_exe():
    exe_path = 'C:/Users/name/AppData/Local/Temp/'
    username = os.getlogin()
    exe_path = exe_path.replace('name', username)

    for root, dirs, files in os.walk(exe_path):
        for dir_name in dirs:
            if dir_name.startswith('_MEI'):
                mei_folder = os.path.join(root, dir_name)  # 找到 _MEI 資料夾

                try: 
                    # 刪除其他 _MEI 資料夾（除了目前程式開啟的暫存檔案）
                    if mei_folder != os.path.join(root, '_MEI'):
                        shutil.rmtree(mei_folder)
                except:
                    print('Checking...')
                # 複製 Data.db 到 _MEI 資料夾
                current_path = os.getcwd()  # 取得目前程式 NMS_main 的路徑
                shutil.copy(os.path.join(current_path, 'Data.db'), mei_folder)

                # 設定 exe_path 到 _MEI 資料夾中的 NMS.exe 檔案
                exe_path = os.path.join(mei_folder, 'NMS.exe')

                # 檢查 NMS.exe 是否存在於 _MEI 資料夾中
                if os.path.exists(exe_path):
                    return exe_path

    return None

def restore_db():
    exe_path = 'C:\\Users\\name\\AppData\\Local\\Temp\\'
    username = os.getlogin()
    exe_path = exe_path.replace('name', username)
    
    for root, dirs, files in os.walk(exe_path):
        for dir_name in dirs:
            if dir_name.startswith('_MEI'):
                current_path = os.getcwd() # 得到NMS_main執行位置
                source_path = os.path.join(root, dir_name, 'Data.db') # 將Data.db複製回去
                shutil.copy(source_path, current_path)
                print('Finished rewrite.')

def main():
    expiration_date = get_activation_date() # 獲取日期
    exe_path = find_exe()
    try:
        remaining_time = expiration_date - datetime.datetime.now()
        print(f"Your license is valid until: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if remaining_time.total_seconds() <= 0:
            print("License expired. Please contact support.")
            time.sleep(5)
        else:
            process = subprocess.Popen([exe_path])
        
            while True:
                remaining_time = expiration_date - datetime.datetime.now()
                if remaining_time.total_seconds() <= 0:
                    process.terminate()
                    print("License expired. Please contact support.")
                    time.sleep(5)
                    break
                
                if process.poll() is not None: # 檢查NMS.exe是否關閉
                    restore_db()
                    time.sleep(5)
                    break
                
                elif remaining_time.total_seconds() <= 3600:  # 低於一小時
                    remaining_minutes = int(remaining_time.total_seconds() // 60)
                    if remaining_minutes % 10 == 0: # 10分鐘提醒一次
                        print(f"Remaining time: {remaining_minutes} min(s)")
                    
                time.sleep(5) # 5秒檢查一次
            
    except FileNotFoundError:
        print(f"Error: The specified executable file '{exe_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()