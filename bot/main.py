import logging
import os
import re
from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, filters, CallbackContext
from bot.bot import registrar_handlers  # Importa os handlers do bot.py

# 🔹 Pegando o token do ambiente (Railway ou local)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: O token do bot não foi encontrado!")

# 🔹 Criando o aplicativo do bot
app = Application.builder().token(TOKEN).build()

# 🔹 Função para rodar o bot
def iniciar_bot():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Bot Iniciado e aguardando mensagens...")

    # 🔹 Registrando os handlers do `bot.py`
    registrar_handlers(app)

    # 🔹 Rodando o bot
    app.run_polling()

# 🔹 Apenas executa o bot se o arquivo for rodado diretamente
if __name__ == "__main__":
    iniciar_bot()
