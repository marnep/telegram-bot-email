import imaplib
import email
import re
import requests
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Variáveis de ambiente (Railway -> Variables)
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_code_from_email():
    mail = None
    try:
        logging.info("Conectando ao servidor IMAP...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, timeout=30)
        logging.info("Autenticando no IMAP...")
        mail.login(EMAIL_USER, EMAIL_PASS)
        logging.info("Consultando e-mails não lidos...")
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
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            body = payload.decode("utf-8")
                        except UnicodeDecodeError:
                            body = payload.decode("latin-1", errors="ignore")
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                try:
                    body = payload.decode("utf-8")
                except UnicodeDecodeError:
                    body = payload.decode("latin-1", errors="ignore")

        match = re.search(r"\b\d{6}\b", body)
        return match.group(0) if match else None

    except Exception as e:
        logging.error("Falha ao ler e-mail (%s). Nova tentativa em 15 segundos.", type(e).__name__)
        return None
    finally:
        if mail is not None:
            try:
                mail.shutdown()
            except Exception:
                pass

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        r = requests.post(url, data=data, timeout=(10, 30))
        if r.status_code == 200:
            print("[INFO] Mensagem enviada para o Telegram com sucesso.")
        else:
            print(f"[ERRO] Falha ao enviar para o Telegram: {r.text}")
    except Exception as e:
        logging.error("Falha no envio ao Telegram (%s).", type(e).__name__)

if __name__ == "__main__":
    print("[INFO] Iniciando bot...")
    while True:
        code = get_code_from_email()
        if code:
            send_to_telegram(f"📩 Código recebido: {code}")
        time.sleep(15)  # espera 15 segundos antes de checar de novo
