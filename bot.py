import os
import requests
import time
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

TOKEN = os.getenv('TELEGRAM_TOKEN')  # Token do BotTelegram
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')  # O teu chat ID para o bot só responder a ti

API_URL = "https://public-api.birdeye.so/public/coins?network=solana"

current_token = None

def get_chat_id(update: Update):
    return update.effective_chat.id

def start(update: Update, context: CallbackContext):
    chat_id = get_chat_id(update)
    if str(chat_id) != CHAT_ID:
        update.message.reply_text("Acesso negado.")
        return
    update.message.reply_text(
        "Olá! Sou o 2xntos CRYPTO BOT. Vou ajudar a monitorar memecoins em tendência.\n"
        "Use /status para ver o token atual em análise.\n"
        "Use /comprar para comprar o token em tendência.\n"
        "Use /vender para vender a posição.\n"
        "Use /parar para cancelar a operação."
    )

def fetch_top_token():
    resp = requests.get(API_URL)
    data = resp.json()
    coins = data.get('coins', [])
    if not coins:
        return None
    top = max(coins, key=lambda x: x.get('priceChange', 0))
    return top['address'], top['name'], top.get('priceChange', 0)

def status(update: Update, context: CallbackContext):
    global current_token
    if current_token:
        update.message.reply_text(
            f"Token atual: {current_token[1]} ({current_token[0]})\n"
            f"Variação: {current_token[2]:.2f}%"
        )
    else:
        update.message.reply_text("Ainda não há token em análise.")

def comprar(update: Update, context: CallbackContext):
    global current_token
    if not current_token:
        update.message.reply_text("Não há token para comprar no momento.")
        return
    update.message.reply_text(
        f"Compra confirmada para o token {current_token[1]} ({current_token[0]}).\n"
        "Execução da ordem em breve..."
    )
    update.message.reply_text("Ordem de compra executada (simulada).")

def vender(update: Update, context: CallbackContext):
    global current_token
    if not current_token:
        update.message.reply_text("Não há posição para vender no momento.")
        return
    update.message.reply_text(
        f"Venda confirmada para o token {current_token[1]} ({current_token[0]}).\n"
        "Execução da ordem em breve..."
    )
    update.message.reply_text("Ordem de venda executada (simulada).")

def parar(update: Update, context: CallbackContext):
    global current_token
    current_token = None
    update.message.reply_text("Operação cancelada.")

def main():
    global current_token
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("comprar", comprar))
    dp.add_handler(CommandHandler("vender", vender))
    dp.add_handler(CommandHandler("parar", parar))

    updater.start_polling()

    while True:
        try:
            token_info = fetch_top_token()
            if token_info:
                current_token = token_info
            time.sleep(60)
        except Exception as e:
            print("Erro no loop principal:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()
