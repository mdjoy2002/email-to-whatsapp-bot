import email
import imaplib
import os
import requests

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "knuhighschool1994@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD") or "yxzicyuqakfryenx"

ID_INSTANCE = os.environ.get("ID_INSTANCE") or "7107622664"
API_TOKEN_INSTANCE = (
    os.environ.get("API_TOKEN_INSTANCE")
    or "cb0e59e38acb4385b4fc75f121c7f3bf1425d70fb2314ae08a"
)
GROUP_CHAT_ID = "120363356722963349@g.us"


def check_email_and_send():
  try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    status, response = mail.search(None, "UNSEEN")
    if status == "OK":
      for num in response[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        if status == "OK":
          msg = email.message_from_bytes(data[0][1])
          subject = msg["Subject"]
          sender = msg["From"]

          message = f"📢 New Email Arrived!\nFrom: {sender}\nSubject: {subject}"

          # সরাসরি HTTP রিকোয়েস্ট (কোনো লাইব্রেরির ঝামেলা নেই)
          url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
          payload = {"chatId": GROUP_CHAT_ID, "message": message}
          res = requests.post(url, json=payload)

          if res.status_code == 200:
            print("WhatsApp message sent successfully!")
          else:
            print(f"Failed to send. Status: {res.status_code}")

    mail.logout()
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  check_email_and_send()