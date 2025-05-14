class Buyer:

    def __init__(self, n, m):
        self.money = n
        self.fish = m

    def buy_fish(self):
        if self.money >= 1 and self.fish >= 0.5:
            self.money -= 1
            self.fish -= 0.5
            self.fish += 1
            return True
        else:
            return False

    def info(self):
        print("money: " + str(self.money) + "fish: " + str(self.fish))


def how_many_kg(n: int, m: int, k: int):
    buyer = Buyer(n, m)

    for _ in range(k):
        buyer.buy_fish()
        buyer.info()


def how_many_kg_str(inp: str):
    params = inp.split()
    n = int(params[0])
    m = int(params[1])
    k = int(params[2])

    how_many_kg(n, m, k)


i = input("Money fish attempts? (separate with spaces")
how_many_kg_str(i)
