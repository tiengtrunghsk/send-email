import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os

# 1. Đọc danh sách email từ file Excel
excel_file = "users_export_20261016.xlsx"
df = pd.read_excel(excel_file)
users = df[['email', 'name']].dropna(subset=['email']).to_dict('records')

# 2. Lấy thông tin tài khoản từ biến môi trường GitHub Secrets
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("❌ Chưa cấu hình SENDER_EMAIL hoặc SENDER_PASSWORD trong GitHub Secrets!")

# 3. Tiêu đề và nội dung email
SUBJECT = "[THÔNG BÁO] Chuyển đổi tên miền chính thức - Tự Học Tiếng Trung"

BODY_TEMPLATE = """Chào {name},

Xin thông báo đến bạn:
Tên miền cũ (hoctiengtrung.ddns.net) sẽ chính thức DỪNG HOẠT ĐỘNG sau ngày 15/11/2026.

Website đã chính thức chuyển sang tên miền quốc tế mới:
👉 https://tuhoctiengtrung.org

Vui lòng cập nhật lại bookmark/dấu trang của bạn để không bị gián đoạn trong quá trình truy cập và học tập.

Trân trọng,
Đội ngũ Tự Học Tiếng Trung
"""

# 4. Tiến hành gửi email
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("✅ Đã kết nối thành công tới SMTP Server.")

    count = 0
    for user in users:
        recipient_email = str(user['email']).strip()
        recipient_name = str(user['name']).strip() if pd.notna(user['name']) else "bạn"

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = SUBJECT

        body = BODY_TEMPLATE.format(name=recipient_name)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        count += 1
        print(f"[{count}/{len(users)}] Đã gửi thành công tới: {recipient_email}")

        time.sleep(1) # Nghỉ 1 giây tránh spam

    print("\n🎉 Hoàn tất gửi email cho toàn bộ danh sách!")

except Exception as e:
    print(f"❌ Có lỗi xảy ra: {e}")
finally:
    server.quit()
