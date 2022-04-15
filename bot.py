import copy

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
            'terra': ['veleno', 'roccia', 'folletto'],
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
            'spettro': ['normale', 'lotta'],
            'drago': [],
            'buio': ['psico'],
            'acciaio': ['veleno'],
            'folletto': ['drago']}


def show(update: Update, context: CallbackContext) -> None:
    types = update.message.text.split()
    num_types = len(types) - 1

    weakness_c = copy.deepcopy(weakness)
    resistence_c = copy.deepcopy(resistence)
    nullify_c = copy.deepcopy(nullify)

    if types[0] == "/dr2" or types[0] == "/dr1":
        weakness_c.pop("folletto", None)
        resistence_c.pop("folletto", None)
        nullify_c.pop("folletto", None)

        for type, weak in weakness_c.items():
            if weak.__contains__("folletto"):
                count = 0
                for w in weak:
                    if w == "folletto":
                        weakness_c[type].pop(count)
                        break
                    else:
                        count += 1

        for type, res in resistence_c.items():
            if res.__contains__("folletto"):
                count = 0
                for r in res:
                    if r == "folletto":
                        resistence_c[type].pop(count)
                        break
                    else:
                        count += 1

        for type, nul in nullify_c.items():
            if nul.__contains__("folletto"):
                count = 0
                for n in nul:
                    if n == "folletto":
                        nullify_c[type].pop(count)
                        break
                    else:
                        count += 1

        if types[0] == "/dr2":
            resistence_c["acciaio"].append("buio")
            resistence_c["acciaio"].append("spettro")
        elif types[0] == "/dr1":
            weakness_c.pop("acciaio", None)
            resistence_c.pop("acciaio", None)
            nullify_c.pop("acciaio", None)
            weakness_c.pop("buio", None)
            resistence_c.pop("buio", None)
            nullify_c.pop("buio", None)

            for type, weak in weakness_c.items():
                if weak.__contains__("acciaio"):
                    count = 0
                    for w in weak:
                        if w == "acciaio":
                            weakness_c[type].pop(count)
                            break
                        else:
                            count += 1

            for type, res in resistence_c.items():
                if res.__contains__("acciaio"):
                    count = 0
                    for r in res:
                        if r == "acciaio":
                            resistence_c[type].pop(count)
                            break
                        else:
                            count += 1

            for type, nul in nullify_c.items():
                if nul.__contains__("acciaio"):
                    count = 0
                    for n in nul:
                        if n == "acciaio":
                            nullify_c[type].pop(count)
                            break
                        else:
                            count += 1

            for type, weak in weakness_c.items():
                if weak.__contains__("buio"):
                    count = 0
                    for w in weak:
                        if w == "buio":
                            weakness_c[type].pop(count)
                            break
                        else:
                            count += 1

            for type, res in resistence_c.items():
                if res.__contains__("buio"):
                    count = 0
                    for r in res:
                        if r == "buio":
                            resistence_c[type].pop(count)
                            break
                        else:
                            count += 1

            for type, nul in nullify_c.items():
                if nul.__contains__("buio"):
                    count = 0
                    for n in nul:
                        if n == "buio":
                            nullify_c[type].pop(count)
                            break
                        else:
                            count += 1

            count = 0
            for res in resistence_c["fuoco"]:
                if res == "ghiaccio":
                    resistence_c["fuoco"].pop(count)
                    break
                else:
                    count += 1

            count = 0
            for weak in weakness_c["psico"]:
                if weak == "spettro":
                    weakness_c["psico"].pop(count)
                    break
                else:
                    count += 1

            count = 0
            for res in resistence_c["veleno"]:
                if res == "coleottero":
                    resistence_c["veleno"].pop(count)
                    break
                else:
                    count += 1

            weakness_c["veleno"].append("coleottero")
            weakness_c["coleottero"].append("veleno")
            nullify_c["psico"].append("spettro")

    if num_types == 1:
        if weakness_c.__contains__(types[1].lower()):
            update.message.reply_text(show_weakness(weakness_c, resistence_c, nullify_c, types[1].lower()))
            update.message.reply_text(show_resistence(weakness_c, resistence_c, nullify_c, types[1].lower()))
        else:
            if ((types[0] == "/dr1" and (types[1].lower() == "buio" or types[1].lower() == "acciaio"
                                         or types[1].lower() == "folletto")) or (
                    types[0] == "/dr2" and types[1].lower() == "folletto")):
                update.message.reply_text("Tipo non valido per questa Generazione. (Usa /help per vedere quale comando usare)")
            else:
                update.message.reply_text("Tipo non valido")
    elif num_types == 2:
        if weakness_c.__contains__(types[1].lower()) and weakness_c.__contains__(types[2].lower()):
            update.message.reply_text(show_weakness(weakness_c, resistence_c, nullify_c, types[1].lower(), types[2].lower()))
            update.message.reply_text(show_resistence(weakness_c, resistence_c, nullify_c, types[1].lower(), types[2].lower()))
        else:
            if ((types[0] == "/dr1" and (types[1].lower() == "buio" or types[1].lower() == "acciaio"
                                       or types[1].lower() == "folletto" or types[2].lower() == "buio" or
                                        types[2].lower() == "acciaio" or types[2].lower() == "folletto"))
                    or (types[0] == "/dr2" and (types[1].lower() == "folletto" or types[2].lower() == "folletto"))):
                update.message.reply_text("Uno o entrambi i tipi non sono validi per questa Generazione. (Usa /help per vedere quale comando usare)")
            else:
                update.message.reply_text("Uno o entrambi i tipi non sono validi")
    else:
        update.message.reply_text("Il comando deve essere seguito da minimo uno e massimo due tipi")


def show_weakness(*args):
    tot = "DEBOLEZZE:\n"
    #print(*args)

    amount = {}

    for weak in args[0][args[3]]:
        amount[weak] = 2
        if len(args) == 5:
            if args[2][args[4]].__contains__(weak):
                amount[weak] = 0
            elif args[1][args[4]].__contains__(weak):
                amount[weak] = 1
            elif args[0][args[4]].__contains__(weak):
                amount[weak] = 4

    if len(args) == 5:
        for weak in args[0][args[4]]:
            if amount.__contains__(weak):
                continue

            amount[weak] = 2
            if len(args) == 5:
                if args[2][args[3]].__contains__(weak):
                    amount[weak] = 0
                elif args[1][args[3]].__contains__(weak):
                    amount[weak] = 1

    for am in amount:
        if amount[am] > 1:
            tot += f"{am} x{amount[am]}\n"

    return tot


def show_resistence(*args):
    tot = "RESISTENZE:\n"
    #print(*args)

    amount = {}

    for nu in args[2][args[3]]:
        amount[nu] = 0

    if len(args) == 5:
        for nu in args[2][args[4]]:
            amount[nu] = 0

    for res in args[1][args[3]]:
        if amount.__contains__(res):
            continue

        amount[res] = 0.5
        if len(args) == 5:
            if args[0][args[4]].__contains__(res):
                amount[res] = 1
            elif args[1][args[4]].__contains__(res):
                amount[res] = 0.25

    if len(args) == 5:
        for res in args[1][args[4]]:
            if amount.__contains__(res):
                continue

            amount[res] = 0.5
            if len(args) == 5:
                if args[0][args[3]].__contains__(res):
                    amount[res] = 1

    for am in amount:
        if amount[am] < 1:
            tot += f"{am} x{amount[am]}\n"

    return tot


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Benvenut*! Il bot mostra Debolezze e Resistenze dei tipi Pokémon.\n"
                              "Digita il comando /dr seguito dal primo tipo "
                              "ed eventualmente secondo tipo.\n"
                              "Esempi:\n/dr fuoco\n"
                              "/dr folletto spettro\n\n"
                              "(/dr fa riferimento ai giochi dalla 6 Generazione in poi.\n"
                              "Utilizza /dr1 per i giochi di 1 Generazione.\n"
                              "Utilizza /dr2 per i giochi della 2-5 Generazione.)")


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Digita il comando /dr seguito dal primo tipo "
                              "ed eventualmente secondo tipo.\n"
                              "Esempi:\n/dr fuoco\n"
                              "/dr folletto spettro\n\n"
                              "(/dr fa riferimento ai giochi dalla 6 Generazione in poi.\n"
                              "Utilizza /dr1 per i giochi di 1 Generazione.\n"
                              "Utilizza /dr2 per i giochi della 2-5 Generazione.)")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("dr", show))
    dispatcher.add_handler(CommandHandler("dr1", show))
    dispatcher.add_handler(CommandHandler("dr2", show))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    #updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
