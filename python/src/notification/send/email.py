import smtplib, os, json
from email.message import EmailMessage

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GAMIL_ADDRESS")
        sender_password = os.environ.get("GAMIL_PASSWORD")
        receiver_address = message["username"]

        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is ready")
        msg["Subject"] = "Download MP3"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        session = smtplib.SMTP("smtp.gmail.com")
        session.starttls()
        session.login(msg, sender_address, sender_password)
        session.send_message(msg)
        session.quit()
        print("mail sent")
    except Exception as err:
        print(err)
        return err