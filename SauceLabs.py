from selenium import webdriver
import xlrd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_cap = {
    'platform': "Mac OS X 10.9",
    'browserName': "chrome",
    'version': "31" ,
}

file_location = "E:\\Aautomation_software\\Test.xlsx"
workbook = xlrd.open_workbook (file_location)
sheet = workbook.sheet_by_index (0)
data = [[sheet.cell_value (r , c) for r in range (sheet.nrows)] for c in range (sheet.ncols)]

driver = webdriver.Remote(
    command_executor='http://akothari10:6a672b25-b10e-489a-8602-98530f8fd012@ondemand.saucelabs.com:80/wd/hub',
    desired_capabilities=desired_cap)
driver.maximize_window ()
driver.get ("http://www.google.com")

driver.find_element_by_id ("lst-ib").send_keys (data[0][2])
driver.find_element_by_xpath ("//*[@id='tsf']/div[2]/div[3]/center/input[1]").click ()
driver.implicitly_wait (20)
driver.get_screenshot_as_file ("Google.png")

sender_email_id = "tapputest@gmail.com"
receiver_email_id = "abhay@concret.io"

# instance of MIMEMultipart
msg: MIMEMultipart = MIMEMultipart ()

# storing the senders email address
msg['From'] = sender_email_id

# storing the receivers email address
msg['To'] = receiver_email_id

# storing the subject
msg['Subject'] = "Hello, this is auto-generated mail from python"

# string to store the body of the mail
msg_body = "Hello PFA"

# attach the body with the msg instance
msg.attach (MIMEText (msg_body , 'plain'))

# open the file to be sent
filename = "Test.png"
attachment = open ("./Google.png" , "rb")

# instance of MIMEBase and named as p
p: MIMEBase = MIMEBase ('application' , 'octet-stream')

# To change the payload into encoded form
p.set_payload ((attachment).read ())

# encode into base64
encoders.encode_base64 (p)
p.add_header ('Content-Disposition' , "attachment;filename=%s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach (p)

# creates SMTP session
server = smtplib.SMTP ('smtp.gmail.com' , 587)

# start TLS for security
server.starttls ()

# Authentication
password = "Mintu1@&"
server.login (sender_email_id , password)

# Converts the Multipart msg into a string
text = msg.as_string ()

# sending the mail
server.sendmail (sender_email_id , receiver_email_id , text)

# terminating the session
server.quit ()

driver.quit ()
