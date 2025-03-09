from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import responder_mensagem
("TELEGRAM_BOT_TOKEN")

app = Application.builder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", responder_mensagem))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensagem))

app.run_polling()
