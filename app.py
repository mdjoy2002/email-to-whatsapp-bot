import email
import imaplib
import threading
import time
from flask import Flask
import requests

app = Flask(__name__)

# কনফিগারেশন
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "knuhighschool1994@gmail.com"
EMAIL_PASSWORD = "yxzicyuqakfryenx"

ID_INSTANCE = "710762264"
API_TOKEN_INSTANCE = "cb0e59e38acb4385b4fc75f121c7f3bf1425d70fb2314ae08a"
GROUP_CHAT_ID = "120363356722963349@g.us"


def send_whatsapp_message(message_text):
  url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
  payload = {"chatId": GROUP_CHAT_ID, "message": message_text}
  try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
      print("WhatsApp message sent successfully via HTTP!")
    else:
      print(f"Failed to send WhatsApp message. Status: {response.status_code}")
  except Exception as e:
    print(f"API Request Error: {e}")


def check_email_loop():
  while True:
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
            send_whatsapp_message(message)

      mail.logout()
    except Exception as e:
      print(f"Error in background loop: {e}")

    # প্রতি ১ মিনিট পর পর চেক করবে
    time.sleep(60)


# ব্যাকগ্রাউন্ডে লুপটি চালু করা
threading.Thread(target=check_email_loop, daemon=True).start()


@app.route("/")
def home():
  return "KNU High School Email-to-WhatsApp Bot is Running LIVE!"


if __name__ == "__main__":
  app.run()