import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
# Thông tin email
    email = 'lequangmy5522@gmail.com'
    password = 'rnsb psuk cqll higq'
    email_sent = 'tranquang2005kg@gmail.com'

    # Tạo email MIME
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email_sent
    msg['Subject'] = '⚠️ CẢNH BÁO BUỒN NGỦ KHI LÁI XE'

    body = 'Người lái xe đang gặp tình trạng nguy hiểm do buồn ngủ. Vui lòng kiểm tra ngay!'
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Gửi email
    with smtplib.SMTP('smtp.gmail.com', 587) as session:
        session.starttls()  # bảo mật
        session.login(email, password)
        session.sendmail(email, email_sent, msg.as_string())