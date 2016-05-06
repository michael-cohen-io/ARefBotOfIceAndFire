import anapioficeandfire

class CharacterResponse:

    def __init__(self, raw_text):
        self.query = raw_text.replace('ARefBotOfIceAndFire! Character ', '', 1)
        self.api = anapioficeandfire.API()

    def get_relative(self, url):
        url_tokens = url.split('/')
        id = int(url_tokens[-1])
        relative = self.api.get_character(id=id)
        return relative.name

    def get_allegiance(self, url):
        url_tokens = url.split('/')
        id = int(url_tokens[-1])
        house = self.api.get_house(id=id)
        return house.name

    def get_book(self, url):
        url_tokens = url.split('/')
        id = int(url_tokens[-1])
        book = self.api.get_book(id=id)
        return book.name


    def get_character(self, character):
        response = ''
        reddit_eol = '    \n'

        #NAME
        response += '## **' + character.name + '**' + reddit_eol

        #TITLES
        if character.titles:
            response += '### '
            i = 0
            while i != len(character.titles)-1:
                response += character.titles[i] + ', '
                i += 1
            response += character.titles[i] + reddit_eol

        #ALIASES
        if character.aliases:
            response += '### '
            i = 0
            while i != len(character.aliases)-1:
                response += character.aliases[i] + ', '
                i += 1
            response += character.aliases[i] + reddit_eol

        #LIFE
        if character.born:
            response += 'Born: ' + character.born + reddit_eol

        if character.died:
            response += 'Died: ' + character.died + reddit_eol

        #RELATIVES
        if character.father:
            response += 'Father: ' + self.get_relative(character.father) + reddit_eol

        if character.mother:
            response += 'Mother: ' + self.get_relative(character.mother) + reddit_eol

        if character.spouse:
            response += 'Spouse: ' + self.get_relative(character.spouse) + reddit_eol

        #ALLEGIANCES
        if character.allegiances:
            response += 'Allegiances: '
            for house in character.allegiances:
                response += self.get_allegiance(house) + ', '
            response = response[:-2] + reddit_eol

        #BOOKS
        if character.books:
            response += 'Appears in: '
            for book in character.books:
                response += self.get_book(book) + ', '
            response = response[:-2] + reddit_eol

        #PLAYEDBY
        if character.playedBy:
            response += 'Played by: '
            actors = character.playedBy
            i = 0
            while i != len(actors)-1:
                response += actors[i] + ', '
                i += 1
            response += actors[i]

        return response

    def create_response(self):
        response = ''
        characters = self.api.get_characters(name=self.query)
        print('Length: ' + str(len(characters)))
        for c in characters:
            response += self.get_character(c)
            response += '\n***\n'

        response += 'Provided by [/u/ARefBotOfIceAndFire](https://www.reddit.com/user/arefbotoficeandfire) v1.0'
        return response
