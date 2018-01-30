import sys
from datetime import datetime
import hashlib
import os
import time

from bs4 import BeautifulSoup
import requests

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
import settings as S

class Md5:
    original_md5sum = list()
    new_md5sum = list()


def send_message():
	addr = S.Settings.email
	msg = MIMEMultipart()
	msg['From'] = addr
	msg['To'] = addr
	msg['Subject'] = "Website Updated!"
	 
	body = "The website "+S.Settings.url+" has been updated."
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(addr, S.Settings.password)
	text = msg.as_string()
	server.sendmail(addr, addr, text)
	if S.Settings.push == "True":
		server.sendmail(addr,S.Settings.number, text)
	server.quit()


def write_to_file(i, version, text):
	with open("website_data\website-"+str(i)+version+".txt", "w", encoding="utf-8") as f:
		f.write(text)
	hasher = hashlib.md5()
	with open("website_data\website-"+str(i)+version+".txt", "rb") as f:
		buffer = f.read()
		hasher.update(buffer)

	if version == "" or Md5.original_md5sum[i] == 0:
		Md5.original_md5sum[i] = hasher.hexdigest()
	if version == "_updated" or Md5.new_md5sum[i] == 0:
		Md5.new_md5sum[i] = hasher.hexdigest()


def check_for_update(i):
	request = requests.get(S.Settings.url)
	#assert request.status_code == 200
	html = request.text
	soup = BeautifulSoup(html, "lxml")
	for script in soup(["script", "style"]):
	    script.extract()
	text = soup.get_text()
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines 
		for phrase in line.split(" "))
	text = '\n'.join(chunk for chunk in chunks if chunk)

	if os.path.isfile("website_data\\website-"+str(i)+".txt"):
		write_to_file(i, "_updated", text)
	else:
		write_to_file(i, "", text)
		check_for_update(i)


def get_settings():
	file = open("settings.txt", "r", encoding="utf-8")
	file = file.read()
	file = file.split("\n")
	
	ul = list()
	pl = list()
	
	if ("=" in file[0]):
		t = file[0].split("=")
		t = int(t[len(t)-1])
	for i in range(1,len(file)):
		if (not file[i].strip() == '') and ("=" not in file[i].strip()) and ("," in file[i].strip()):
			s = file[i].split(",")
			ul.append(s[0])
			pl.append(s[1])
	return ul, pl, t


def print_monitoring(i):
	print(str(i+1)+") URL: ", S.Settings.url)
	print("\tOLD: ", Md5.original_md5sum[i])
	print("\tNEW: ", Md5.new_md5sum[i])
	if Md5.original_md5sum[i] != Md5.new_md5sum[i]:
		print("\tWebsite has been updated! " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n")
		send_message()
	else:
		print("\tWebsite hasn't been updated yet... " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n")


def loop(p):
	url_list, push_list, timer = get_settings()
	Md5.original_md5sum = [0]*len(url_list)
	Md5.new_md5sum = [0]*len(url_list)
	S.Settings.timer = timer;
	while True:
		for i in range(0,len(url_list)):
			S.Settings.url = url_list[i]
			S.Settings.push = push_list[i]
			
			check_for_update(i)
			if (p == 1):
				print_monitoring(i)

			Md5.original_md5sum[i] = Md5.new_md5sum[i]	
		time.sleep(S.Settings.timer)


def main(p=0):
    path = os.path.dirname(os.path.realpath(__file__))
    try:
        os.remove(path + "\website*.txt")
    except OSError:
        pass

    loop(p)


if __name__ == "__main__":
    main()