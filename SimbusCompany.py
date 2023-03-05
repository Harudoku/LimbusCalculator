import tkinter as tk
import random
from tooltip import CreateToolTip

ver = "2.0.2"


def getDefaults():
    lines = open("defaults.cfg", "r").read().split("\n")
    fdict = {}
    for line in lines:
        if not line or line[0] == "#":
            continue
        line = line.split("-")
        if len(line) < 2:
            continue
        if not line[1]:
            continue
        elif line[1][0] == "[":
            try:
                fdict[line[0]] = float(line[1][1:-1])
            except ValueError:
                print(f'Config for {line[0]} doesn\'t interpret as float, continuing with {line[0]} == 0')
        elif line[1][0] == "(":
            fdict[line[0]] = line[1][1:-1]
    return fdict


defaults = getDefaults()


def flip(mod):
    return 1 if random.random() >= .5 - (mod / 100) else 0


def simulate(abase, acoins, acval, asan, bbase, bcoins, bcval, bsan):
    """ Return [win: bool, coins: int, clashes: int] """
    clashCount = 0
    while clashCount < 10000 and acoins > 0 and bcoins > 0:
        acurr, bcurr = abase, bbase
        for x in range(acoins):
            acurr += acval * flip(asan)
        for x in range(bcoins):
            bcurr += bcval * flip(bsan)
        if acurr > bcurr:
            bcoins -= 1
        if bcurr > acurr:
            acoins -= 1
        clashCount += 1
    winner = True if acoins > 0 else False
    coins = acoins
    clashes = clashCount
    return winner, coins, clashes


prompts = (
    (0, "Base power:"), (1, "Coin damage:"), (2, "Coin count:"), (3, "Base power:"), (4, "Coin damage:"),
    (5, "Coin count:"), (6, "Power difference (yours minus theirs):"), (7, "Attack power:"), (8, "Attack power:"),
    (9, "Your sanity:"), (10, "Their sanity:"),
)


class Simulator(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, borderwidth=15)
        self.class_name = "test"

        self.labelYours = tk.Label(self, text="YOUR STATS", font=("Helvetica", 12))
        self.labelTheirs = tk.Label(self, text="THEIR STATS", font=("Helvetica", 12))
        self.labelEmpty = tk.Label(self, text="  ")
        self.labelEmpty2 = tk.Label(self, text="  ")
        self.prompts = {n[0]: tk.Label(self, text=n[1], anchor="e") for n in prompts}
        self.aBase = tk.Entry(self, width=3)
        self.aCVal = tk.Entry(self, width=3)
        self.aCoins = tk.Entry(self, width=3)
        self.bBase = tk.Entry(self, width=3)
        self.bCVal = tk.Entry(self, width=3)
        self.bCoins = tk.Entry(self, width=3)
        self.pDiff = tk.Entry(self, width=3)
        self.pDiff.insert(0, "0")
        self.aPower = tk.Entry(self, width=3)
        self.bPower = tk.Entry(self, width=3)
        self.aSanity = tk.Entry(self, width=3)
        self.aSanity.insert(0, "0")
        self.bSanity = tk.Entry(self, width=3)
        self.bSanity.insert(0, "0")
        # self.prompt12 = tk.Label(self, text="Flip chance % increase per sanity:", anchor="w")
        # self.sanModifier = tk.Entry(self, width=3)
        # self.sanModifier.insert(0, ".45")
        self.submit = tk.Button(self, text="Run 10,000 simulations", command=self.calculate)
        self.output = tk.Label(self, text="\n\n")
        self.toggle1 = tk.Button(self, text="Toggle power mode", command=self.togglePowerMode)
        self.toggle2 = tk.Button(self, text="Toggle sanity mode", command=self.toggleSanityMode)
        self.modePower = "pDiff"
        self.modeSanity = 0
        
        CreateToolTip(self.labelYours, text="Test")

        self.labelYours.grid(column=0, row=0, columnspan=2)
        self.labelEmpty.grid(column=2, row=0)
        self.labelTheirs.grid(column=3, row=0, columnspan=2)
        self.prompts[0].grid(column=0, row=1)
        self.aBase.grid(column=1, row=1)
        self.prompts[1].grid(column=0, row=2)
        self.aCVal.grid(column=1, row=2)
        self.prompts[2].grid(column=0, row=3)
        self.aCoins.grid(column=1, row=3)
        self.prompts[3].grid(column=3, row=1)
        self.bBase.grid(column=4, row=1)
        self.prompts[4].grid(column=3, row=2)
        self.bCVal.grid(column=4, row=2)
        self.prompts[5].grid(column=3, row=3)
        self.bCoins.grid(column=4, row=3)
        self.prompts[6].grid(column=0, row=4, columnspan=4)
        self.pDiff.grid(column=4, row=4)
        self.output.grid(column=0, row=5, columnspan=4)
        self.submit.grid(column=0, row=6, columnspan=6)
        self.toggle1.grid(column=0, row=8)
        self.toggle2.grid(column=3, row=8)

    def toggleSanityMode(self):
        if self.modeSanity == 0:
            self.modeSanity = 1
            self.labelEmpty2.grid(column=0, row=9)
            self.prompts[9].grid(column=0, row=10)
            self.aSanity.grid(column=1, row=10)
            self.prompts[10].grid(column=3, row=10)
            self.bSanity.grid(column=4, row=10)
            # self.prompts[11].grid(column=0, row=11, columnspan=4)
            # self.sanModifier.grid(column=4, row=11)
        else:
            self.modeSanity = 0
            self.prompts[9].grid_forget()
            self.aSanity.grid_forget()
            self.prompts[10].grid_forget()
            self.bSanity.grid_forget()
            # self.prompts[11].grid_forget()
            # self.sanModifier.grid_forget()

    def togglePowerMode(self):
        if self.modePower == "pDiff":
            self.modePower = "aPower"
            self.prompts[6].grid_forget()
            self.pDiff.grid_forget()
            self.prompts[7].grid(column=0, row=4)
            self.aPower.grid(column=1, row=4)
            self.prompts[8].grid(column=3, row=4)
            self.bPower.grid(column=4, row=4)
        else:
            self.modePower = "pDiff"
            self.prompts[7].grid_forget()
            self.aPower.grid_forget()
            self.prompts[8].grid_forget()
            self.bPower.grid_forget()
            self.prompts[6].grid(column=0, row=4, columnspan=4)
            self.pDiff.grid(column=4, row=4)

    def calculate(self):
        try:
            aBase = int(self.aBase.get())
            aCVal = int(self.aCVal.get())
            aCoins = int(self.aCoins.get())
            if aCoins < 1:
                aCoins = 1
            bBase = int(self.bBase.get())
            bCVal = int(self.bCVal.get())
            bCoins = int(self.bCoins.get())
            if bCoins < 1:
                bCoins = 1
            if self.modePower == "pDiff":
                if not self.pDiff.get():
                    pDiff = 0
                else:
                    pDiff = int(int(self.pDiff.get()) / 5)
            else:
                aPower = int(self.aPower.get()) if self.aPower.get() else 0
                bPower = int(self.bPower.get()) if self.bPower.get() else 0
                pDiff = int((aPower - bPower) / 5)
            if pDiff < 0:
                bBase -= pDiff
            else:
                aBase += pDiff
            if self.modeSanity == 0:
                aSan = 0
                bSan = 0
            else:
                # aSan = float(self.sanModifier.get()) * float(self.aSanity.get())
                # bSan = float(self.sanModifier.get()) * float(self.bSanity.get())
                aSan = defaults["Sanity Mod"] * float(self.aSanity.get())
                bSan = defaults["Sanity Mod"] * float(self.bSanity.get())
            wins = 0
            coins = 0
            clashes = 0
            for x in range(10000):
                sim = simulate(aBase, aCoins, aCVal, aSan, bBase, bCoins, bCVal, bSan)
                wins += 1 if sim[0] else 0
                coins += sim[1]
                clashes += sim[2]
            winRate = wins / 100
            if wins:
                avgCoins = coins / wins
            else:
                avgCoins = 0

            result = (
                f'Winrate is around {winRate}%,\nwith an average {round(avgCoins, 2)} coins\nremaining during a win.'
            )
        except ValueError:
            result = "\nPlease, fill all boxes with digits only\n"

        self.output.configure(text=result)


def Main():
    root = tk.Tk(className="Sadness")
    Simulator(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    Main()
