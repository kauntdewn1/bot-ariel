async def responder_mensagem(update: Update, context: CallbackContext):
    print(f"Mensagem recebida: {update.message.text}")  # Adiciona log no terminal

    await update.message.reply_text("Estou aqui!")
