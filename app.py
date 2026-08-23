import email
import imaplib
import os
import threading
import time
from flask import Flask
from whatsapp_api_client_python import API

app = Flask(__name__)

# কনফিগারেশন
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "knuhighschool1994@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

ID_INSTANCE = os.environ.get("ID_INSTANCE")
API_TOKEN_INSTANCE = os.environ.get("API_TOKEN_INSTANCE")
GROUP_CHAT_ID = "120363356722963349@g.us"

greenAPI = API.GreenAPI(ID_INSTANCE, API_TOKEN_INSTANCE)


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
            response_api = greenAPI.sending.sendMessage(GROUP_CHAT_ID, message)
            if response_api.code == 200:
              print("WhatsApp message sent successfully via Flask app!")

      mail.logout()
    except Exception as e:
      print(f"Error in background loop: {e}")

    # প্রতি ১ মিনিট (৬০ সেকেন্ড) পর পর চেক করবে
    time.sleep(60)


# ব্যাকগ্রাউন্ডে লুপটি রান করানোর জন্য থ্রেড শুরু করা
threading.Thread(target=check_email_loop, daemon=True).start()


@app.route("/")
def home():
  return "KNU High School Email-to-WhatsApp Bot is Running LIVE!"


if __name__ == "__main__":
  app.run()