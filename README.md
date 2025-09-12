# 📧 Telegram Email Bot

Este projeto lê e-mails do Gmail (via IMAP), extrai códigos de verificação de 6 dígitos e envia automaticamente para um chat do Telegram.

## 🚀 Deploy no Railway

### 1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/telegram-email-bot.git
cd telegram-email-bot
```

### 2. Configure as variáveis de ambiente no Railway:
- `IMAP_SERVER=imap.gmail.com`
- `EMAIL_USER=seu_email@gmail.com`
- `EMAIL_PASS=sua_senha_app`
- `BOT_TOKEN=seu_bot_token`
- `CHAT_ID=seu_chat_id`

### 3. Deploy automático com GitHub Actions
O workflow em `.github/workflows/deploy.yml` garante que cada push na branch **main** será enviado ao Railway.

## 📊 Arquitetura
![Arquitetura](arquitetura.png)
