async def responder_mensagem(update: Update, context: CallbackContext):
    print(f"Recebi: {update.message.text}")  # Debug
    await update.message.reply_text("Estou aqui!")