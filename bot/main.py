import logging
import os
import re
from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, filters

# CONFIGURAÇÃO DO BOT (Substitua pelo seu token real)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# REGEX PARA DETECÇÃO DE LINKS INDESEJADOS
LINKS_REGEX = re.compile(r"(https?://\S+|www\.\S+|\.\S{2,})")

# MENSAGEM DE BOAS-VINDAS COM BOTÃO INTERATIVO
async def boas_vindas(update: Update, context: CallbackContext) -> None:
    for user in update.message.new_chat_members:
        keyboard = [[InlineKeyboardButton("📜 Regras do Grupo", callback_data="regras")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"🎉 Bem-vindo, {user.first_name}! 🚀\n\n"
            "Clique no botão abaixo para ver as regras:",
            reply_markup=reply_markup
        )

# RESPOSTA AO BOTÃO DE REGRAS
async def botao_clicado(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query and query.data == "regras":
        await query.answer()
        await query.message.reply_text(
            "📜 **Regras do Grupo:**\n"
            "1️⃣ Respeite todos os membros.\n"
            "2️⃣ Não envie links suspeitos.\n"
            "3️⃣ Proibido spam e mensagens ofensivas.\n"
            "4️⃣ Siga as diretrizes da comunidade.\n\n"
            "❗ O não cumprimento pode resultar em banimento."
        )

# VERIFICA SE O USUÁRIO É ADMINISTRADOR
async def is_admin(update: Update) -> bool:
    chat_member = await update.effective_chat.get_member(update.effective_user.id)
    return chat_member.status in ["administrator", "creator"]

# /BAN - Banir um usuário (somente admin)
async def ban(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para banir.")
        return

    try:
        user_id = int(context.args[0])
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text(f"✅ Usuário {user_id} foi banido!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao banir: {e}")

# /MUTE - Silenciar um usuário (somente admin)
async def mute(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para silenciar.")
        return

    try:
        user_id = int(context.args[0])
        await context.bot.restrict_chat_member(
            update.effective_chat.id, user_id, ChatPermissions()
        )
        await update.message.reply_text(f"🔇 Usuário {user_id} foi silenciado!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao silenciar: {e}")

# /UNMUTE - Desmutar um usuário (somente admin)
async def unmute(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para desmutar.")
        return

    try:
        user_id = int(context.args[0])
        await context.bot.restrict_chat_member(
            update.effective_chat.id, user_id, ChatPermissions(can_send_messages=True)
        )
        await update.message.reply_text(f"🔊 Usuário {user_id} foi desmutado!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao desmutar: {e}")

# /WARN - Avisar um usuário (somente admin)
async def warn(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para avisar.")
        return

    try:
        user_id = int(context.args[0])
        await update.message.reply_text(f"⚠️ Aviso enviado para o usuário {user_id}.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao enviar aviso: {e}")

# /START - Iniciar o bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Bot iniciado! Use /help para ver os comandos disponíveis.")

# /REGRAS - Mostrar as regras do chat
async def regras(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "📜 Regras do chat:\n"
        "1️⃣ Respeite todos os membros.\n"
        "2️⃣ Não envie links suspeitos.\n"
        "3️⃣ Proibido spam e mensagens ofensivas.\n"
        "4️⃣ Siga as diretrizes da comunidade.\n\n"
        "❗ O não cumprimento pode resultar em banimento."
    )

# /HELP - Mostrar os comandos disponíveis
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "ℹ️ **Comandos disponíveis:**\n"
        "/start - Iniciar o bot\n"
        "/regras - Mostrar as regras do chat\n"
        "/ban - Banir um usuário (somente admin)\n"
        "/mute - Silenciar um usuário (somente admin)\n"
        "/unmute - Desmutar um usuário (somente admin)\n"
        "/warn - Avisar um usuário (somente admin)\n"
        "/help - Mostrar esta mensagem de ajuda"
    )

# FILTRO DE MENSAGENS (ANTI-SPAM & ANTI-LINKS)
async def verificar_mensagem(update: Update, context: CallbackContext) -> None:
    mensagem = update.message.text.lower()

    if LINKS_REGEX.search(mensagem):
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await update.message.delete()
            await update.message.reply_text(f"🚫 {update.message.from_user.first_name}, links não são permitidos no grupo!")

# INICIAR O BOT
def iniciar_bot():
    logging.basicConfig(level=logging.INFO)
    print("Bot iniciado! Aguardando mensagens...")

    # Criando o aplicativo do bot
    app = Application.builder().token(TOKEN).build()

    # Handlers para comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("regras", regras))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("warn", warn))

    # Handlers para eventos do grupo
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))
    app.add_handler(CallbackQueryHandler(botao_clicado))

    # Handler para mensagens de texto (anti-spam & anti-links)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_mensagem))

    app.run_polling()

if __name__ == "__main__":
    iniciar_bot()
