class Tournament():
    def __init__(self, date, city, shop, winner, pokes, player_list):
        self.date = date
        self.shop = shop
        self.winner = winner

        if len(pokes) == 0:
            self.poke1 = None
            self.poke1_img = None
            self.poke2 = None
            self.poke2_img = None
        else:
            self.poke1 = pokes[0][0]
            self.poke1_img = pokes[0][1]
        
            if len(pokes) == 1:
                self.poke2 = None
                self.poke2_img = None
            else:   
                self.poke2 = pokes[1][0]
                self.poke2_img = pokes[1][1]

        self.city = city
        self.player_list = player_list

        self.pokes = ','.join(sorted([p[0] for p in pokes]))

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def get_city(self):
        return self.city

    def set_city(self, city):
        self.city = city

    def get_shop(self):
        return self.shop

    def set_shop(self, shop):
        self.shop = shop

    def get_winner(self):
        return self.winner

    def set_winner(self, winner):
        self.winner = winner

    def get_poke1(self):
        return self.poke1

    def set_poke1(self, poke1):
        self.poke1 = poke1

    def get_poke1_img(self):
        return self.poke1_img

    def set_poke1_img(self, poke1_img):
        self.poke1_img = poke1_img

    def get_poke2(self):
        return self.poke2

    def set_poke2(self, poke2):
        self.poke2 = poke2

    def get_poke2_img(self):
        return self.poke2_img

    def set_poke2_img(self, poke2_img):
        self.poke2_img = poke2_img

    def get_pokes(self):
        return self.pokes

    def set_pokes(self, pokes):
        self.pokes = pokes

    def get_player_list(self):
        return self.player_list

    def set_player_list(self, player_list):
        self.player_list = player_list
    


class Player():
    def __init__(self, tournament_id, rank, player, pokes, deck_list):
        self.tournament_id = tournament_id
        self.rank = rank
        self.player = player

        if len(pokes) == 0:
            self.poke1 = None
            self.poke1_img = None
            self.poke2 = None
            self.poke2_img = None
        else:
            self.poke1 = pokes[0][0]
            self.poke1_img = pokes[0][1]
        
        if len(pokes) <= 1:
            self.poke2 = None
            self.poke2_img = None
        else:   
            self.poke2 = pokes[1][0]
            self.poke2_img = pokes[1][1]

        self.pokes = ','.join(sorted([p[0] for p in pokes]))

        self.deck_list = deck_list


class Card():
    def __init__(self, name, count, set, number, lang, deck_url, pokes):
        self.name = name
        self.count = count
        self.set = set
        self.number = number
        self.lang = lang
        self.deck_url = deck_url
        self.pokes = pokes