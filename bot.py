import email
import imaplib
import os
from whatsapp_api_client_python import API

# --- সিক্রেট ও এনভায়রনমেন্ট ভেরিয়েবল থেকে কনফিগারেশন লোড করা ---
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "knuhighschool1994@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# --- Green API কনফিগারেশন ---
ID_INSTANCE = os.environ.get("ID_INSTANCE")
API_TOKEN_INSTANCE = os.environ.get("API_TOKEN_INSTANCE")

# খন্দকার নাসের উদ্দিন মাধ্যমিক বিদ্যালয় (KNU High school 1994) এর গ্রুপ চ্যাট আইডি
GROUP_CHAT_ID = "120363356722963349@g.us"

# Green API ক্লায়েন্ট ইনিশিয়ালাইজ করা
greenAPI = API.GreenAPI(ID_INSTANCE, API_TOKEN_INSTANCE)


def check_email_and_send():
  try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    # শুধু নতুন বা অপঠিত মেইলগুলো খুঁজবে
    status, response = mail.search(None, "UNSEEN")

    if status == "OK":
      for num in response[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        if status == "OK":
          msg = email.message_from_bytes(data[0][1])
          subject = msg["Subject"]
          sender = msg["From"]

          # গ্রুপে পাঠানোর জন্য মেসেজ ফরম্যাট
          message = f"📢 New Email Arrived!\nFrom: {sender}\nSubject: {subject}"

          print("Sending message to KNU High school WhatsApp Group...")

          # Green API দিয়ে সরাসরি গ্রুপে মেসেজ পাঠানো
          response = greenAPI.sending.sendMessage(GROUP_CHAT_ID, message)

          if response.code == 200:
            print("WhatsApp message sent to group successfully!")
          else:
            print(f"Failed to send message. Response code: {response.code}")

    mail.logout()
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  print("Checking emails via GitHub Actions for KNU High School Bot...")
  check_email_and_send()