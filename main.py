MAX_ITEMS = 6
START_BATTERY = 70
BATTERY_DRAIN = 10

# barvy
RESET = "\033[0m"
GREY = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

TITLE_ART = [
    " _  __  ___   _  _  ___   ___  _  _    _   ",
    "| |/ / / _ \\ | \\| || __| / __|| \\| |  /_\\  ",
    "| ' < | (_) || .` || _| | (__ | .` | / _ \\ ",
    "|_|\\_\\ \\___/ |_|\\_||___| \\___||_|\\_|/_/ \\_\\",
    "",
    "      ___________________________________",
    "     |  [] [] [] [] [] [] [] [] [] []  |",
    "     |_________________________________|",
    "======(o)==(o)===============(o)==(o)======",
]

DESCRIPTIONS = {
    "Nástupiště": "Konečná. Nad kolejí bzučí nouzová světla. "
                  "Odsud vedou cesty do všech koutů stanice.",
    "Vestibul": "Prázdný vestibul s turnikety. Hlavní východ zavírá ocelová roleta. "
                "Vedle ní je velké červené tlačítko.",
    "Stará dílna": "Stará dílna údržbářů. Ponk, regály a všude zaprášené nářadí.",
    "Zatopený úsek": "Koleje mizí pod černou vodou. Voda je divně teplá.",
    "Servisní chodba": "Úzká chodba plná trubek. Odněkud je slyšet šustění.",
    "Dispečink": "Pulty plné tlačítek a velká elektrická skříň. "
                 "Jedna pojistka v ní chybí.",
    "Zavalený tunel": "Tunel končí stěnou suti. Nahoře u stropu je mezera. "
                      "V podlaze je zarezlý poklop.",
}

# popisy, které platí, až jde proud
POWER_DESCRIPTIONS = {
    "Vestibul": "Prázdný vestibul s turnikety. Hlavní východ zavírá ocelová roleta. "
                "Tlačítko vedle ní svítí zeleně.",
    "Dispečink": "Pulty blikají a elektrická skříň tiše bzučí. "
                 "Všechny pojistky jsou na místě.",
}

# kam se dá jít z nástupiště
PLACES = ["Vestibul", "Stará dílna", "Zatopený úsek", "Servisní chodba",
          "Dispečink", "Zavalený tunel"]

# tady je tma, stojí to baterku
DARK_PLACES = ["Stará dílna", "Zatopený úsek", "Servisní chodba", "Dispečink",
               "Zavalený tunel"]

# stav hry
game = {
    "room": "Nástupiště",
    "battery": START_BATTERY,
    "power": False,
    "ending": "",
    "message": "",
}

# věci, které hráč nese
inventory = []

# co kde leží
room_items = {
    "Nástupiště": [],
    "Vestibul": ["páčidlo"],
    "Stará dílna": ["lano", "brodicí kalhoty"],
    "Zatopený úsek": ["pojistka", "hák"],
    "Servisní chodba": ["drát", "karta"],
    "Dispečink": [],
    "Zavalený tunel": [],
}


def clear_screen():
    print("\033[H\033[2J\033[3J", end="")


def choose(actions):
    # vypíše akce a vrátí tu, kterou hráč vybral
    print()
    print("Co uděláš?")
    valid = []
    for i in range(len(actions)):
        number = str(i + 1)
        print("  " + CYAN + number + ")" + RESET + " " + actions[i])
        valid.append(number)

    answer = input("> ").strip()
    while answer not in valid:
        print(RED + "Napiš číslo od 1 do " + str(len(actions)) + "." + RESET)
        answer = input("> ").strip()
    return actions[int(answer) - 1]


def current_goal():
    if game["power"]:
        return "Proud jde! Jdi do vestibulu a zmáčkni tlačítko u rolety."
    if "pojistka" not in inventory and "opravená pojistka" not in inventory:
        if "brodicí kalhoty" in inventory:
            return "Najdi pojistku v zatopeném úseku."
        return "Najdi pojistku v zatopeném úseku. Na vodu potřebuješ brodicí kalhoty."
    if "pojistka" in inventory and "drát" not in inventory:
        return "Pojistka je spálená. Drát najdeš v servisní chodbě."
    if "pojistka" in inventory and "drát" in inventory:
        return "Spoj drát a pojistku."
    if "karta" not in inventory:
        return "Dispečink je zamčený. Kartu najdeš v servisní chodbě."
    return "Jdi do dispečinku a vlož opravenou pojistku do skříně."


def show_room():
    room = game["room"]
    clear_screen()
    print(CYAN + "═" * 60)
    print("  " + room.upper())
    print("═" * 60 + RESET)

    if game["power"] and room in POWER_DESCRIPTIONS:
        print(POWER_DESCRIPTIONS[room])
    else:
        print(DESCRIPTIONS[room])

    items = room_items[room]
    if len(items) > 0:
        print("Vidíš tu: " + GREEN + ", ".join(items) + RESET)

    # co se právě stalo
    if game["message"] != "":
        print()
        print(game["message"])
        game["message"] = ""

    print(GREY + "─" * 60 + RESET)
    battery = game["battery"]
    filled = battery // 10
    print("Svítilna: " + YELLOW + "■" * filled + GREY + "□" * (10 - filled) + RESET
          + " " + str(battery) + " %")
    if battery == 0 and not game["power"]:
        print(RED + "Svítilna je vybitá! Až odsud odejdeš, tma tě dostane." + RESET)
    print("Věci (" + str(len(inventory)) + "/" + str(MAX_ITEMS) + "): "
          + GREEN + ", ".join(inventory) + RESET)
    print(YELLOW + "CÍL: " + current_goal() + RESET)


def get_actions():
    # co jde teď udělat
    room = game["room"]
    actions = []

    for item in room_items[room]:
        actions.append("Vzít: " + item)

    if room == "Dispečink" and "opravená pojistka" in inventory:
        actions.append("Vložit pojistku do skříně")
    if room == "Vestibul" and game["power"]:
        actions.append("Zmáčknout tlačítko u rolety")
    if room == "Zavalený tunel" and "kotvička" in inventory:
        actions.append("Vylézt po kotvičce přes suť")
    if room == "Zavalený tunel" and "páčidlo" in inventory:
        actions.append("Vypáčit poklop")

    if "drát" in inventory and "pojistka" in inventory:
        actions.append("Spojit drát a pojistku")
    if "lano" in inventory and "hák" in inventory:
        actions.append("Spojit lano a hák")

    if room == "Nástupiště":
        for place in PLACES:
            actions.append("Jít: " + place)
    else:
        actions.append("Vrátit se na nástupiště")

    actions.append("Ukončit hru")
    return actions


def do_action(action):
    if action == "Vložit pojistku do skříně":
        inventory.remove("opravená pojistka")
        game["power"] = True
        game["message"] = GREEN + "Všude naskočí světla. Proud jde!" + RESET
    elif action == "Zmáčknout tlačítko u rolety":
        game["ending"] = "street"
    elif action == "Vylézt po kotvičce přes suť":
        game["ending"] = "tunnel"
    elif action == "Vypáčit poklop":
        game["ending"] = "train"
    elif action == "Spojit drát a pojistku":
        inventory.remove("drát")
        inventory.remove("pojistka")
        inventory.append("opravená pojistka")
        game["message"] = GREEN + "Máš opravenou pojistku." + RESET
    elif action == "Spojit lano a hák":
        inventory.remove("lano")
        inventory.remove("hák")
        inventory.append("kotvička")
        game["message"] = GREEN + "Máš kotvičku." + RESET
    elif action == "Vrátit se na nástupiště":
        go("Nástupiště")
    elif action == "Ukončit hru":
        if ask_yes_no("Opravdu chceš skončit?"):
            game["ending"] = "quit"
    elif action.startswith("Vzít: "):
        take(action[len("Vzít: "):])
    elif action.startswith("Jít: "):
        go(action[len("Jít: "):])


def ask_yes_no(question):
    answer = input(question + " (a/n) ").strip().lower()
    while answer not in ["a", "n"]:
        print(RED + "Napiš a nebo n." + RESET)
        answer = input(question + " (a/n) ").strip().lower()
    return answer == "a"


def take(item):
    if len(inventory) >= MAX_ITEMS:
        game["message"] = RED + "Máš plné ruce. Spoj nějaké věci dohromady." + RESET
        return
    room_items[game["room"]].remove(item)
    inventory.append(item)
    game["message"] = GREEN + "Bereš: " + item + RESET


def go(place):
    if place == "Dispečink" and "karta" not in inventory:
        game["message"] = RED + "Dispečink je zamčený. Potřebuješ kartu." + RESET
        return
    if place == "Zatopený úsek" and "brodicí kalhoty" not in inventory:
        game["message"] = RED + "Voda sahá po prsa. Potřebuješ brodicí kalhoty." + RESET
        return

    # ve tmě se vybíjí baterka
    if place in DARK_PLACES and not game["power"]:
        game["battery"] = game["battery"] - BATTERY_DRAIN

    game["room"] = place

    # vybitá baterka a žádný proud, takže se už nikam nedostaneš
    if game["battery"] == 0 and not game["power"] and place not in DARK_PLACES:
        game["ending"] = "dark"


def show_intro():
    clear_screen()
    for line in TITLE_ART:
        print(YELLOW + line + RESET)
    print(GREY + "           textová adventura v pražském metru")
    print("                Vytvořil Oliver Steiner" + RESET)
    print()
    print("Probouzíš se na lavičce. Poslední vlak už odjel. Stanice je zamčená,")
    print("proud nejde a v tunelech je něco špatně. Musíš se dostat ven,")
    print("dokud ti nedojde světlo.")
    print()
    print("Napiš číslo akce a zmáčkni Enter.")
    print("Každá cesta do tmy vybije svítilnu o " + str(BATTERY_DRAIN) + " %.")
    print("Uneseš jen " + str(MAX_ITEMS) + " věcí. Řádek CÍL ti poradí, co dál.")
    print()
    input(GREY + "Zmáčkni Enter a začni..." + RESET)


def show_ending():
    ending = game["ending"]
    if ending == "quit":
        return

    if ending == "street":
        color = GREEN
        title = "KONEC 1 ze 3 - HLAVNÍ VÝCHOD"
        text = ("Roleta se se skřípěním zvedá a dovnitř se vhrne studený "
                "listopadový vzduch. Ulice je prázdná. Kolem prorachotí noční "
                "tramvaj. Jsi venku.")
    elif ending == "tunnel":
        color = CYAN
        title = "KONEC 2 ze 3 - DALŠÍ STANICE"
        text = ("Vytáhneš se po laně nahoru a jdeš černým tunelem. Na další "
                "stanici potkáš četu údržby. „Odkud jdete?“ Ukážeš zpátky do "
                "tunelu. „Tam nic není,“ řekne potichu ten nejstarší. "
                "„Ten úsek zazdili v devětasedmdesátém.“")
    elif ending == "train":
        color = YELLOW
        title = "KONEC 3 ze 3 - KONEČNÁ"
        text = ("Pod poklopem stojí vlak, který není na žádné mapě. Nastoupíš, "
                "dveře se zavřou a světla zhasínají jedno po druhém... "
                "Probouzíš se na lavičce. Poslední vlak právě odjel.")
    else:
        color = RED
        title = "PROHRA - TMA"
        text = ("Svítilna je vybitá a proud pořád nejde. Nouzová světla "
                "zablikají a zhasnou. Něco ve tmě se pohne a studené prsty "
                "se ti sevřou kolem kotníku.")

    clear_screen()
    print(color + "★" * 60)
    print("  " + title)
    print("★" * 60 + RESET)
    print(text)


# hlavní smyčka hry
# try/except chytí Ctrl+C a Ctrl+D, aby hra nespadla s chybou
try:
    show_intro()
    while game["ending"] == "":
        show_room()
        action = choose(get_actions())
        do_action(action)
    show_ending()
except (KeyboardInterrupt, EOFError):
    print()
    print("Hra ukončena")
print()
print("Díky za hru! Vytvořil Oliver Steiner.")
