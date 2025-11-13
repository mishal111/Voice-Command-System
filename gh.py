import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

now = datetime.datetime.now()

content=''

def extract_news(url):
    print("Extracting Hacker News....")
    cnt=''
    cnt+=('<b>HN Top Stories:</b>\n'+"<br>"+'-'*50+'<br>')
    response=requests.get(url)
    content=response.content
    soup=BeautifulSoup(content,"html.parser")
    stories=soup.find_all("span",class_='titleline')
    for i,story in enumerate(stories,start=1):
        title_tag=story.find('a')
        if title_tag:
            title=title_tag.text
            link=title_tag['href']
            cnt+=f"{i}.<a href='{link}'>{title}</a><br>"
    return cnt

cnt=extract_news("https://news.ycombinator.com/")
content+=cnt
content+=("<br>------<br>")
content+=("<br><br>End of Message")

print(content)
#Composs and Send the email
print("Composing the email...")

SERVER = "smtp.gmail.com"
PORT = 587
FROM = 'hiccupshelby@gmail.com'
TO = "mishalsafeek@gmail.com"
PASS = 'flaz bpla mvtd rvdm '

msg = MIMEMultipart()

msg['Subject'] = "Top Stories HN [Automated Email]" + " "+str(now.day)+'-'+str(now.month)+'-'+str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content,'html'))

print("Iniating Server...")

server= smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM,TO,msg.as_string())

print("Email Sent")
server.quit()