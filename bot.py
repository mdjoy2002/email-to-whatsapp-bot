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

          # '📢 New Email Arrived!' লেখাটি বাদ দেওয়া হয়েছে
          text_message = f"From: {sender}\nSubject: {subject}"
          url_text = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
          requests.post(
              url_text, json={"chatId": GROUP_CHAT_ID, "message": text_message}
          )

          # মেইলের ভেতর এটাচমেন্ট চেক করা (PDF, Word, Excel)
          for part in msg.walk():
            if part.get_content_maintype() == "multipart":
              continue
            if part.get("Content-Disposition") is None:
              continue

            filename = part.get_filename()
            if filename:
              filename_lower = filename.lower()
              allowed_extensions = (
                  ".pdf",
                  ".doc",
                  ".docx",
                  ".xls",
                  ".xlsx",
              )

              if filename_lower.endswith(allowed_extensions):
                filepath = os.path.join(".", filename)
                with open(filepath, "wb") as f:
                  f.write(part.get_payload(decode=True))
                print(f"Downloaded Document: {filename}")

                # Green API-এর মাধ্যমে হোয়াটসঅ্যাপে ফাইল আপলোড করে পাঠানো
                url_file = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendFileByUpload/{API_TOKEN_INSTANCE}"

                with open(filepath, "rb") as f_file:
                  files = {"file": (filename, f_file)}
                  data_payload = {
                      "chatId": GROUP_CHAT_ID,
                      "caption": f"Attached File: {filename}",
                  }
                  res_file = requests.post(
                      url_file, data=data_payload, files=files
                  )

                  if res_file.status_code == 200:
                    print("Document sent to WhatsApp successfully!")
                  else:
                    print(
                        f"Failed to send document. Status:"
                        f" {res_file.status_code}"
                    )

                # কাজ শেষে লোকাল ফোল্ডার থেকে ফাইল ডিলিট করা
                if os.path.exists(filepath):
                  os.remove(filepath)

    mail.logout()
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  check_email_and_send()