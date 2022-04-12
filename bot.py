from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import os

PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

weakness = {'fuoco': ['acqua', 'roccia', 'terra'],
            'acqua': ['erba', 'elettro'],
            'normale': ['lotta'],
            'elettro': ['terra'],
            'erba': ['fuoco', 'ghiaccio', 'veleno', 'volante', 'coleottero'],
            'ghiaccio': ['fuoco', 'lotta', 'roccia', 'acciaio'],
            'lotta': ['volante', 'psico', 'folletto'],
            'veleno': ['terra', 'psico'],
            'terra': ['acqua', 'erba', 'ghiaccio'],
            'volante': ['elettro', 'ghiaccio', 'roccia'],
            'psico': ['coleottero', 'spettro', 'buio'],
            'coleottero': ['fuoco', 'volante', 'roccia'],
            'roccia': ['acqua', 'erba', 'lotta', 'terra', 'acciaio'],
            'spettro': ['spettro', 'buio'],
            'drago': ['ghiaccio', 'drago', 'folletto'],
            'buio': ['lotta', 'coleottero', 'folletto'],
            'acciaio': ['fuoco', 'lotta', 'terra'],
            'folletto': ['veleno', 'acciaio']}
resistence = {'fuoco': ['fuoco', 'erba', 'ghiaccio', 'coleottero', 'acciaio', 'folletto'],
            'acqua': ['fuoco', 'acqua', 'ghiaccio', 'acciaio'],
            'normale': [],
            'elettro': ['elettro', 'volante', 'acciaio'],
            'erba': ['acqua', 'elettro', 'erba', 'terra'],
            'ghiaccio': ['ghiaccio'],
            'lotta': ['coleottero', 'roccia', 'buio'],
            'veleno': ['erba', 'lotta', 'veleno', 'coleottero'],
            'terra': ['veleno', 'roccia'],
            'volante': ['erba', 'lotta', 'coleottero'],
            'psico': ['lotta', 'psico'],
            'coleottero': ['erba', 'lotta', 'terra'],
            'roccia': ['normale', 'fuoco', 'veleno', 'volante'],
            'spettro': ['veleno', 'coleottero'],
            'drago': ['fuoco', 'acqua', 'elettro', 'erba'],
            'buio': ['spettro', 'buio'],
            'acciaio': ['normale', 'erba', 'ghiaccio', 'volante', 'psico', 'coleottero', 'roccia', 'drago', 'acciaio', 'folletto'],
            'folletto': ['lotta', 'coleottero', 'buio']}
nullify = {'fuoco': [],
            'acqua': [],
            'normale': ['spettro'],
            'elettro': [],
            'erba': [],
            'ghiaccio': [],
            'lotta': [],
            'veleno': [],
            'terra': ['elettro'],
            'volante': ['terra'],
            'psico': [],
            'coleottero': [],
            'roccia': [],
            'spettro': ['normale'],
            'drago': [],
            'buio': ['psico'],
            'acciaio': [],
            'folletto': ['drago']}


def show(update: Update, context: CallbackContext) -> None:
    types = update.message.text.split()
    num_types = len(types) - 1

    if num_types == 1:
        if weakness.__contains__(types[1]):
            update.message.reply_text(show_weakness(types[1]))
            update.message.reply_text(show_resistence(types[1]))
        else:
            update.message.reply_text("Tipo non valido")
    elif num_types == 2:
        if weakness.__contains__(types[1]) and weakness.__contains__(types[2]):
            update.message.reply_text(show_weakness(types[1], types[2]))
            update.message.reply_text(show_resistence(types[1], types[2]))
        else:
            update.message.reply_text("Uno o entrambi i tipi non sono validi")
    else:
        update.message.reply_text("Selezionare minimo uno e massimo due tipi")


def show_weakness(*args):
    tot = "DEBOLEZZE:\n"
    #print(*args)

    amount = {}

    for weak in weakness[args[0]]:
        amount[weak] = 2
        if len(args) == 2:
            if nullify[args[1]].__contains__(weak):
                amount[weak] = 0
            elif resistence[args[1]].__contains__(weak):
                amount[weak] = 1
            elif weakness[args[1]].__contains__(weak):
                amount[weak] = 4

    if len(args) == 2:
        for weak in weakness[args[1]]:
            if amount.__contains__(weak):
                continue

            amount[weak] = 2
            if len(args) == 2:
                if nullify[args[0]].__contains__(weak):
                    amount[weak] = 0
                elif resistence[args[0]].__contains__(weak):
                    amount[weak] = 1

    for am in amount:
        if amount[am] > 1:
            tot += f"{am} x{amount[am]}\n"

    return tot


def show_resistence(*args):
    tot = "RESISTENZE:\n"
    #print(*args)

    amount = {}

    for nu in nullify[args[0]]:
        amount[nu] = 0

    if len(args) == 2:
        for nu in nullify[args[1]]:
            amount[nu] = 0

    for res in resistence[args[0]]:
        if amount.__contains__(res):
            continue

        amount[res] = 0.5
        if len(args) == 2:
            if weakness[args[1]].__contains__(res):
                amount[res] = 1
            elif resistence[args[1]].__contains__(res):
                amount[res] = 0.25

    if len(args) == 2:
        for res in resistence[args[1]]:
            if amount.__contains__(res):
                continue

            amount[res] = 0.5
            if len(args) == 2:
                if weakness[args[0]].__contains__(res):
                    amount[res] = 1

    for am in amount:
        if amount[am] < 1:
            tot += f"{am} x{amount[am]}\n"

    return tot


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Benvenut*! Il bot mostra Debolezze e Resistenze dei tipi Pokémon.\n"
                              "Digita il comando /dr seguito dal primo tipo "
                              "ed eventualmente secondo tipo.\n"
                              "Es:\n/dr fuoco\n"
                              "/dr folletto spettro")


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Digita il comando /dr seguito dal primo tipo "
                              "ed eventualmente secondo tipo.\n"
                              "Es:\n/dr fuoco\n"
                              "/dr folletto spettro")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("dr", show))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    #updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
