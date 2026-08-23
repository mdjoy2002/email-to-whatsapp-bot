import email
import imaplib
import os
from whatsapp_api_client_python import API

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "knuhighschool1994@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

ID_INSTANCE = os.environ.get("ID_INSTANCE")
API_TOKEN_INSTANCE = os.environ.get("API_TOKEN_INSTANCE")
GROUP_CHAT_ID = "120363356722963349@g.us"

greenAPI = API.GreenAPI(ID_INSTANCE, API_TOKEN_INSTANCE)


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
          response = greenAPI.sending.sendMessage(GROUP_CHAT_ID, message)
          if response.code == 200:
            print("WhatsApp message sent to group successfully!")

    mail.logout()
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  check_email_and_send()