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

pokebase = {}


def show(update: Update, context: CallbackContext):
    if not weakness or not strength or not nullify:
        read_type_chart()

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
            update.message.reply_html(show_weakness(weakness_c, strength_c, nullify_c, text[1].lower()))
            update.message.reply_html(show_resistence(weakness_c, strength_c, nullify_c, text[1].lower()))
        else:
            if ((text[0] == "/dr1" and (text[1].lower() == "buio" or text[1].lower() == "acciaio"
                                         or text[1].lower() == "folletto")) or (
                    text[0] == "/dr2" and text[1].lower() == "folletto")):
                update.message.reply_text("Tipo non valido per questa Generazione. "
                                          "(Usa /help per vedere quale comando usare)")
            else:
                update.message.reply_text("Tipo non valido")
    elif num_types == 2:
        if weakness_c.__contains__(text[1].lower()) and weakness_c.__contains__(text[2].lower()):
            update.message.reply_html(show_weakness(weakness_c, strength_c, nullify_c, text[1].lower(), text[2].lower()))
            update.message.reply_html(show_resistence(weakness_c, strength_c, nullify_c, text[1].lower(), text[2].lower()))
        else:
            if ((text[0] == "/dr1" and (text[1].lower() == "buio" or text[1].lower() == "acciaio"
                                       or text[1].lower() == "folletto" or text[2].lower() == "buio" or
                                        text[2].lower() == "acciaio" or text[2].lower() == "folletto"))
                    or (text[0] == "/dr2" and (text[1].lower() == "folletto" or text[2].lower() == "folletto"))):
                update.message.reply_text("Uno o entrambi i tipi non sono validi per questa Generazione. "
                                          "(Usa /help per vedere quale comando usare)")
            else:
                update.message.reply_text("Uno o entrambi i tipi non sono validi")
    else:
        update.message.reply_text("Il comando deve essere seguito da minimo uno e massimo due tipi")


def show_weakness(*args):
    tot = "<u><b>DEBOLEZZE:</b></u>\n"
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
    tot = "<u><b>RESISTENZE:</b></u>\n"
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
    if not pokebase:
        read_pokebase()

    text = update.message.text.split()

    if len(text) == 1:
        update.message.reply_text("Il comando deve essere seguito dal nome del Pokémon.")
    else:
        if pokebase.__contains__(text[1].lower()):
            update.message.reply_html(show_pokemon(text[1].lower()))

            if pokebase.__contains__(text[1].lower() + "(alola)"):
                update.message.reply_html(show_pokemon(text[1].lower() + "(alola)"))
            if pokebase.__contains__(text[1].lower() + "(galar)"):
                update.message.reply_html(show_pokemon(text[1].lower() + "(galar)"))
            if pokebase.__contains__(text[1].lower() + "(hisui)"):
                update.message.reply_html(show_pokemon(text[1].lower() + "(hisui)"))

            if pokebase.__contains__(text[1].lower() + "(pre-8g)"):
                update.message.reply_html("<u>PER GENERAZIONI PRECEDENTI LA 8</u>\n\n" + show_pokemon(text[1].lower() + "(pre-8g)"))
            if pokebase.__contains__(text[1].lower() + "(pre-6g)"):
                update.message.reply_html("<u>PER GENERAZIONI PRECEDENTI LA 6</u>\n\n" + show_pokemon(text[1].lower() + "(pre-6g)"))
            if pokebase.__contains__(text[1].lower() + "(pre-5g)"):
                update.message.reply_html("<u>PER GENERAZIONI PRECEDENTI LA 5</u>\n\n" + show_pokemon(text[1].lower() + "(pre-5g)"))
            if pokebase.__contains__(text[1].lower() + "(pre-4g)"):
                update.message.reply_html("<u>PER GENERAZIONI PRECEDENTI LA 4</u>\n\n" + show_pokemon(text[1].lower() + "(pre-4g)"))
            if pokebase.__contains__(text[1].lower() + "(pre-3g)"):
                update.message.reply_html("<u>PER GENERAZIONI PRECEDENTI LA 3</u>\n\n" + show_pokemon(text[1].lower() + "(pre-3g)"))
            if pokebase.__contains__(text[1].lower() + "(pre-2g)"):
                update.message.reply_html("<u>PER GENERAZIONI PRECEDENTI LA 2</u>\n\n" + show_pokemon(text[1].lower() + "(pre-2g)"))
        else:
            update.message.reply_text("Pokémon non esistente o non ancora presente nel nostro Pokédex (WIP :D)")


def delsubstring(s):
    ns = s
    pos = s.find("(pre")

    if pos != -1:
        ns = s[:pos]

    return ns


def show_pokemon(poke):
    mex = "INFO SU <b>" + delsubstring(poke).upper() + "</b>\t" \
                                                       "\t\t\t\^-^/ :\n"
    pos = 0
    num_tab = 1

    if pokebase[poke][0] == "-e":
        if pokebase.__contains__(pokebase[poke][1]):
            mex += "<u>" + delsubstring(pokebase[poke][1]) + "</u> "
            for i in pokebase[pokebase[poke][1]]:
                if i == "-e":
                    continue

                if i == "-a":
                    num_tab -= 1
                    for n in range(num_tab):
                        mex += "\t\t"

                    mex += "<i>------ oppure ------</i>\n"
                    continue

                if i == "-o":
                    num_tab -= 1
                    for n in range(num_tab):
                        mex += "\t\t"

                    mex += "<i>------ inoltre ------</i>\n"
                    continue

                if pos == 0:
                    mex += "[" + i + "]\n"
                    pos = 1
                elif pos == 1:
                    for n in range(num_tab):
                        mex += "\t\t"

                    mex += "<i>**** " + i.replace("-", " ") + " ****</i>\n"
                    pos = 2
                elif pos == 2:
                    for n in range(num_tab):
                        mex += "\t\t"

                    if i == poke:
                        mex += "<b><u>" + delsubstring(i) + "</u></b> "
                    else:
                        mex += "<u>" + delsubstring(i) + "</u> "
                    pos = 0
                    num_tab += 1
        else:
            mex += "WIP"
    else:
        mex += "<b><u>" + delsubstring(poke) + "</u></b> "
        for i in pokebase[poke]:
            if i == "-e":
                continue

            if i == "-a":
                num_tab -= 1
                for n in range(num_tab):
                    mex += "\t\t"

                mex += "<i>------ oppure ------</i>\n"
                continue

            if i == "-o":
                num_tab -= 1
                for n in range(num_tab):
                    mex += "\t\t"

                mex += "<i>------ inoltre ------</i>\n"
                continue

            if pos == 0:
                mex += "[" + i + "]\n"
                pos = 1
            elif pos == 1:
                for n in range(num_tab):
                    mex += "\t\t"

                mex += "<i>**** " + i.replace("-", " ") + " ****</i>\n"
                pos = 2
            elif pos == 2:
                for n in range(num_tab):
                    mex += "\t\t"

                mex += "<u>" + delsubstring(i) + "</u> "
                pos = 0
                num_tab += 1

    return mex


def show_pokebase(update: Update, context: CallbackContext):
    if not pokebase:
        read_pokebase()

    mex = "<b><u>GENERAZIONE 1</u></b>\n"
    number = 1

    for p in pokebase:
        if p[0] == "-":
            gen = p[1]
            update.message.reply_html(mex)
            mex = "<b><u>" + "GENERAZIONE " + f"{gen}" + "</u></b>\n"
            continue

        if p.find("(pre") == -1 and p.find("(alola)") == -1 and p.find("(galar)") == -1 and p.find("(hisui)") == -1:
            mex += f"{number}. " + p + " "
            number += 1

            if pokebase[p][0] != "-e":
                mex += "[" + pokebase[p][0] + "]\n"
                continue
            else:
                s = ""

                if pokebase.__contains__(pokebase[p][1]):
                    s = pokebase[p][1]
                else:
                    if pokebase.__contains__(p + "(pre-2g)"):
                        p += "(pre-2g)"
                        if pokebase[p][0] != "-e":
                            mex += "[" + pokebase[p][0] + "]\n"
                            continue
                        else:
                            s = pokebase[p][1]
                    elif pokebase.__contains__(p + "(pre-3g)"):
                        p += "(pre-3g)"
                        if pokebase[p][0] != "-e":
                            mex += "[" + pokebase[p][0] + "]\n"
                            continue
                        else:
                            s = pokebase[p][1]
                    elif pokebase.__contains__(p + "(pre-4g)"):
                        p += "(pre-4g)"
                        if pokebase[p][0] != "-e":
                            mex += "[" + pokebase[p][0] + "]\n"
                            continue
                        else:
                            s = pokebase[p][1]
                    elif pokebase.__contains__(p + "(pre-5g)"):
                        p += "(pre-5g)"
                        if pokebase[p][0] != "-e":
                            mex += "[" + pokebase[p][0] + "]\n"
                            continue
                        else:
                            s = pokebase[p][1]
                    elif pokebase.__contains__(p + "(pre-6g)"):
                        p += "(pre-6g)"
                        if pokebase[p][0] != "-e":
                            mex += "[" + pokebase[p][0] + "]\n"
                            continue
                        else:
                            s = pokebase[p][1]
                    elif pokebase.__contains__(p + "(pre-8g)"):
                        p += "(pre-8g)"
                        if pokebase[p][0] != "-e":
                            mex += "[" + pokebase[p][0] + "]\n"
                            continue
                        else:
                            s = pokebase[p][1]

                count = 0
                for t in pokebase[s]:
                    if t == p:
                        mex += "[" + pokebase[s][count + 1] + "]\n"
                        break
                    else:
                        count += 1

        #print(mex) #per il debug

    update.message.reply_html(mex)


def start(update: Update, context: CallbackContext):
    if not weakness or not strength or not nullify:
        read_type_chart()

    if not pokebase:
        read_pokebase()

    update.message.reply_html("Benvenut*! Questi sono i comandi del bot:\n"
                              "<u><b>Mostrare Debolezze e Resistenze dei Tipi:</b></u>\n"
                              "<code>/dr tipo1 [tipo2]</code>  <i>Per Generazioni 6+</i>\n"
                              "<code>/dr2 tipo1 [tipo2]</code> <i>Per Generazioni 2-5</i>\n"
                              "<code>/dr1 tipo1 [tipo2]</code> <i>Per Generazione 1</i>\n"
                              "Esempi:\n"
                              "<code>/dr fuoco</code>\n"
                              "<code>/dr folletto spettro</code>\n"
                              "<code>/dr1 coleottero</code>\n"
                              "<u><b>Mostrare Tipi ed Evoluzioni di un Pokémon\n"
                              "(WIP: al momento sono presenti solo le Generazioni 1, 2, 3, 4, 5 e 6):</b></u>\n"
                              "<code>/info nomePokémon</code>\n"
                              "Esempi:\n"
                              "<code>/info bulbasaur</code>\n"
                              "<code>/info charizard</code>\n"
                              "<u><b>Mostrare Nomi e Tipi di tutti i Pokémon\n"
                              "(WIP: al momento sono presenti solo le Generazioni 1, 2, 3, 4, 5 e 6):</b></u>\n"
                              "<code>/all</code>")


def help(update: Update, context: CallbackContext):
    update.message.reply_html("<u><b>Mostrare Debolezze e Resistenze dei Tipi:</b></u>\n"
                              "<code>/dr tipo1 [tipo2]</code>  <i>Per Generazioni 6+</i>\n"
                              "<code>/dr2 tipo1 [tipo2]</code> <i>Per Generazioni 2-5</i>\n"
                              "<code>/dr1 tipo1 [tipo2]</code> <i>Per Generazione 1</i>\n"
                              "Esempi:\n"
                              "<code>/dr fuoco</code>\n"
                              "<code>/dr folletto spettro</code>\n"
                              "<code>/dr1 coleottero</code>\n"
                              "<u><b>Mostrare Tipi ed Evoluzioni di un Pokémon\n"
                              "(WIP: al momento sono presenti solo le Generazioni 1, 2, 3, 4, 5 e 6):</b></u>\n"
                              "<code>/info nomePokémon</code>\n"
                              "Esempi:\n"
                              "<code>/info bulbasaur</code>\n"
                              "<code>/info charizard</code>\n"
                              "<u><b>Mostrare Nomi e Tipi di tutti i Pokémon\n"
                              "(WIP: al momento sono presenti solo le Generazioni 1, 2, 3, 4, 5 e 6):</b></u>\n"
                              "<code>/all</code>")


def read_type_chart():
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


def read_pokebase():
    f = open("pokeBase.txt", "r")

    for li in f:
        line = li.split()
        index = 0
        pokebase[line[0]] = []

        for p in line:
            if index != 0:
                pokebase[line[0]].append(line[index])

            index += 1

    f.close()


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("dr", show))
    dispatcher.add_handler(CommandHandler("dr1", show))
    dispatcher.add_handler(CommandHandler("dr2", show))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("all", show_pokebase))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    #updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
