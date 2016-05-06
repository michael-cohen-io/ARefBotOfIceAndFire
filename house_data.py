import anapioficeandfire

class HouseResponse:

    def __init__(self, raw_text):
        self.query = raw_text.replace('ARefBotOfIceAndFire! House ', '', 1)
        self.api = anapioficeandfire.API()


    def get_character(self, url):
        url_tokens = url.split('/')
        id = int(url_tokens[-1])
        character = self.api.get_character(id=id)
        return character.name

    def get_relative_house(self, url):
        url_tokens = url.split('/')
        id = int(url_tokens[-1])
        house = self.api.get_character(id=id)
        return house.name

    def get_house(self, house):
        response = ''
        reddit_eol = '    \n'

        #NAME
        response += '## **' + house.name + '**' + reddit_eol

        #WORDS
        if house.words:
            response += '### ' + house.words + reddit_eol

        #Kingdom
        if house.region:
            response += 'Kingdom: ' + house.region + reddit_eol

        #COA
        if house.coatOfArms:
            response += 'Coat of arms: ' + house.coatOfArms + reddit_eol

        #TITLES
        if house.titles:
            response += 'Title(s): '
            i = 0
            while i != len(house.titles)-1:
                response += house.titles[i] + ', '
                i += 1
            response += house.titles[i] + reddit_eol

        #SEATS
        if house.seats:
            response += 'Seat(s): '
            i = 0
            while i != len(house.seats)-1:
                response += house.seats[i] + ', '
                i += 1
            response += house.seats[i] + reddit_eol


        if house.currentLord:
            response += 'Current Lord: ' + self.get_character(house.currentLord)

        if house.heir:
            response += 'Heir: ' + self.get_character(house.heir) + reddit_eol

        if house.overlord:
            response += 'Sworn To: ' + self.get_relative_house(house.overlord) + reddit_eol

        if house.founded:
            response += 'Founded: ' + house.founded + reddit_eol

        if house.founder:
            response += 'Founder: ' + house.founder + reddit_eol

        if house.diedOut:
            response += 'Died Out: ' + house.diedOut + reddit_eol

        if house.ancestralWeapons:
            response += 'Weapon(s): '
            i = 0
            while i != len(house.ancestralWeapons)-1:
                response += house.ancestralWeapons[i] + ', '
                i += 1
            response += house.ancestralWeapons[i] + reddit_eol

        if house.cadetBranches:
            response += 'Cadet Branche(s): '
            i = 0
            while i != len(house.cadetBranches)-1:
                response += get_relative_house(house.cadetBranches[i])
                i += 1
            response += get_relative_house(house.cadetBranches[i]) + reddit_eol

        return response

    def create_response(self):
        response = ''
        print('Query: ' + self.query)
        houses = self.api.get_houses(name=self.query)
        print ('Length: ' + str(len(houses)))
        for h in houses:
            response += self.get_house(h)
            response += '\n***\n'

        response += 'Provided by [/u/ARefBotOfIceAndFire](https://www.reddit.com/user/arefbotoficeandfire) v1.0'
        return response
