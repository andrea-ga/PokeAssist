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

weakness = {}
strength = {}
nullify = {}

pokemon = {"bulbasaur": ["erba veleno", "livello 16", "ivysaur", "erba veleno", "livello 32", "venusaur", "erba veleno"],
           "ivysaur": ["bulbasaur"],
           "venusaur": ["bulbasaur"],

           "charmander": ["fuoco", "livello 16", "charmeleon", "fuoco", "livello 36", "charizard", "fuoco volante"],
           "charmeleon": ["charmander"],
           "charizard": ["charmander"],

           "squirtle": ["acqua", "livello 16", "wartortle", "acqua", "livello 36", "blastoise", "acqua"],
           "wartortle": ["squirtle"],
           "blastoise": ["squirtle"]
}


def show(update: Update, context: CallbackContext):
    if not weakness or not strength or not nullify:
        read_typechart()

    text = update.message.text.split()
    num_types = len(text) - 1

    weakness_c = copy.deepcopy(weakness)
    strength_c = copy.deepcopy(strength)
    nullify_c = copy.deepcopy(nullify)

    if text[0] == "/dr2" or text[0] == "/dr1":
        weakness_c.pop("folletto", None)
        strength_c.pop("folletto", None)
        nullify_c.pop("folletto", None)

        for typ, weak in weakness_c.items():
            if weak.__contains__("folletto"):
                count = 0
                for w in weak:
                    if w == "folletto":
                        weakness_c[typ].pop(count)
                        break
                    else:
                        count += 1

        for typ, res in strength_c.items():
            if res.__contains__("folletto"):
                count = 0
                for r in res:
                    if r == "folletto":
                        strength_c[typ].pop(count)
                        break
                    else:
                        count += 1

        for typ, nul in nullify_c.items():
            if nul.__contains__("folletto"):
                count = 0
                for n in nul:
                    if n == "folletto":
                        nullify_c[typ].pop(count)
                        break
                    else:
                        count += 1

        if text[0] == "/dr2":
            strength_c["acciaio"].append("buio")
            strength_c["acciaio"].append("spettro")
        elif text[0] == "/dr1":
            weakness_c.pop("acciaio", None)
            strength_c.pop("acciaio", None)
            nullify_c.pop("acciaio", None)
            weakness_c.pop("buio", None)
            strength_c.pop("buio", None)
            nullify_c.pop("buio", None)

            for typ, weak in weakness_c.items():
                if weak.__contains__("acciaio"):
                    count = 0
                    for w in weak:
                        if w == "acciaio":
                            weakness_c[typ].pop(count)
                            break
                        else:
                            count += 1

            for typ, res in strength_c.items():
                if res.__contains__("acciaio"):
                    count = 0
                    for r in res:
                        if r == "acciaio":
                            strength_c[typ].pop(count)
                            break
                        else:
                            count += 1

            for typ, nul in nullify_c.items():
                if nul.__contains__("acciaio"):
                    count = 0
                    for n in nul:
                        if n == "acciaio":
                            nullify_c[typ].pop(count)
                            break
                        else:
                            count += 1

            for typ, weak in weakness_c.items():
                if weak.__contains__("buio"):
                    count = 0
                    for w in weak:
                        if w == "buio":
                            weakness_c[typ].pop(count)
                            break
                        else:
                            count += 1

            for typ, res in strength_c.items():
                if res.__contains__("buio"):
                    count = 0
                    for r in res:
                        if r == "buio":
                            strength_c[typ].pop(count)
                            break
                        else:
                            count += 1

            for typ, nul in nullify_c.items():
                if nul.__contains__("buio"):
                    count = 0
                    for n in nul:
                        if n == "buio":
                            nullify_c[typ].pop(count)
                            break
                        else:
                            count += 1

            count = 0
            for res in strength_c["fuoco"]:
                if res == "ghiaccio":
                    strength_c["fuoco"].pop(count)
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
            for res in strength_c["veleno"]:
                if res == "coleottero":
                    strength_c["veleno"].pop(count)
                    break
                else:
                    count += 1

            weakness_c["veleno"].append("coleottero")
            weakness_c["coleottero"].append("veleno")
            nullify_c["psico"].append("spettro")

    if num_types == 1:
        if weakness_c.__contains__(text[1].lower()):
            update.message.reply_text(show_weakness(weakness_c, strength_c, nullify_c, text[1].lower()))
            update.message.reply_text(show_resistence(weakness_c, strength_c, nullify_c, text[1].lower()))
        else:
            if ((text[0] == "/dr1" and (text[1].lower() == "buio" or text[1].lower() == "acciaio"
                                         or text[1].lower() == "folletto")) or (
                    text[0] == "/dr2" and text[1].lower() == "folletto")):
                update.message.reply_text("Tipo non valido per questa Generazione. (Usa /help per vedere quale comando usare)")
            else:
                update.message.reply_text("Tipo non valido")
    elif num_types == 2:
        if weakness_c.__contains__(text[1].lower()) and weakness_c.__contains__(text[2].lower()):
            update.message.reply_text(show_weakness(weakness_c, strength_c, nullify_c, text[1].lower(), text[2].lower()))
            update.message.reply_text(show_resistence(weakness_c, strength_c, nullify_c, text[1].lower(), text[2].lower()))
        else:
            if ((text[0] == "/dr1" and (text[1].lower() == "buio" or text[1].lower() == "acciaio"
                                       or text[1].lower() == "folletto" or text[2].lower() == "buio" or
                                        text[2].lower() == "acciaio" or text[2].lower() == "folletto"))
                    or (text[0] == "/dr2" and (text[1].lower() == "folletto" or text[2].lower() == "folletto"))):
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


def info(update: Update, context: CallbackContext):
    text = update.message.text.split()

    if len(text) == 1:
        update.message.reply_text("Il comando deve essere seguito dal nome del Pokémon.")
    else:
        if pokemon.__contains__(text[1].lower()):
            update.message.reply_text(show_pokemon(text[1].lower()))
        else:
            update.message.reply_text("Pokémon non esistente o non ancora presente nel nostro Pokédex (WIP :D)")


def show_pokemon(poke):
    mex = "INFO SU " + poke.upper() + "   \^-^/ :\n"
    count = 0

    if len(pokemon[poke]) == 1:
        mex += pokemon[poke][0] + " "
        for i in pokemon[pokemon[poke][0]]:
            if count == 0 or count == 3 or count == 6:
                mex += "[" + i + "]\n"
            elif count == 1 or count == 4:
                mex += "**** " + i + " ****\n"
            else:
                mex += i + " "

            count += 1
    else:
        mex += poke + " "
        for i in pokemon[poke]:
            if count == 0 or count == 3 or count == 6:
                mex += "[" + i + "]\n"
            elif count == 1 or count == 4:
                mex += "**** " + i + " ****\n"
            else:
                mex += i + " "

            count += 1

    return mex


def start(update: Update, context: CallbackContext):
    if not weakness or not strength or not nullify:
        read_typechart()

    update.message.reply_text("Benvenut*! Il bot mostra Debolezze e Resistenze dei tipi Pokémon.\n"
                              "Digita il comando /dr seguito dal primo tipo "
                              "ed eventualmente secondo tipo.\n"
                              "Esempi:\n/dr fuoco\n"
                              "/dr folletto spettro\n\n"
                              "(/dr fa riferimento ai giochi dalla 6 Generazione in poi.\n"
                              "Utilizza /dr1 per i giochi di 1 Generazione.\n"
                              "Utilizza /dr2 per i giochi della 2-5 Generazione.)\n\n"
                              "Il comando /info è in WIP. Ha la funzione di Pokédex \^-^/\n"
                              "Esempi:\n/info bulbasaur\n"
                              "/info charizard")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Digita il comando /dr seguito dal primo tipo "
                              "ed eventualmente secondo tipo.\n"
                              "Esempi:\n/dr fuoco\n"
                              "/dr folletto spettro\n\n"
                              "(/dr fa riferimento ai giochi dalla 6 Generazione in poi.\n"
                              "Utilizza /dr1 per i giochi di 1 Generazione.\n"
                              "Utilizza /dr2 per i giochi della 2-5 Generazione.)\n\n"
                              "Il comando /info è in WIP. Ha la funzione di Pokédex \^-^/\n"
                              "Esempi:\n/info bulbasaur\n"
                              "/info charizard")


def read_typechart():
    f = open("typeChart.txt", "r")
    count = 0

    for li in f:
        line = li.split()

        if len(line) == 0:
            count += 1
        else:
            if count == 0:
                index = 0
                weakness[line[0]] = []
                for t in line:
                    if index != 0:
                        weakness[line[0]].append(line[index])

                    index += 1
            elif count == 1:
                index = 0
                strength[line[0]] = []
                for t in line:
                    if index != 0:
                        strength[line[0]].append(line[index])

                    index += 1
            elif count == 2:
                index = 0
                nullify[line[0]] = []
                for t in line:
                    if index != 0:
                        nullify[line[0]].append(line[index])

                    index += 1

    f.close()


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("dr", show))
    dispatcher.add_handler(CommandHandler("dr1", show))
    dispatcher.add_handler(CommandHandler("dr2", show))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(CommandHandler("info", info))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    #updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
