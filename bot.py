import imaplib
import email
import re
import requests
import os
import time

# Variáveis de ambiente (Railway -> Variables)
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_code_from_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        status, data = mail.search(None, "UNSEEN")
        mail_ids = data[0].split()

        if not mail_ids:
            print("[INFO] Nenhum e-mail novo encontrado.")
            return None

        status, msg_data = mail.fetch(mail_ids[-1], "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        match = re.search(r"\b\d{6}\b", body)
        return match.group(0) if match else None

    except Exception as e:
        print(f"[ERRO] Falha ao ler e-mail: {e}")
        return None

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            print("[INFO] Mensagem enviada para o Telegram.")
        else:
            print(f"[ERRO] Falha ao enviar mensagem. Código: {r.status_code}")
    except Exception as e:
        print(f"[ERRO] Falha na requisição ao Telegram: {e}")

if __name__ == "__main__":
    while True:
        code = get_code_from_email()
        if code:
            send_to_telegram(f"📩 Código recebido: {code}")
        time.sleep(30)
