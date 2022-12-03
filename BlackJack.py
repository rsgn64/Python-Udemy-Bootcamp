import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    def __str__(self):
        return '{} of {}'.format(self.rank, self.suit)

class Deck():
    def __init__(self):
        # Note this only happens once upon creation of a new Deck
        self.all_cards = [] 
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.all_cards.append(Card(suit,rank))
                
    def shuffle(self):
        # Note this doesn't return anything
        random.shuffle(self.all_cards)
        
    def deal_one(self):
        # Note we remove one card from the list of all_cards
        return self.all_cards.pop()

class Player():
    def __init__(self, money):
        self.money = money
    def deposit(self, amount):
        self.money += amount
    def withdraw(self, amount):
        if amount > self.money:
            print("You don't have enough money.")
            return False
        else:
            self.money -= amount
            return True

class Hand():
    def __init__(self, cards): #cards is a list compossed of current deck
        #initial blackjack hand deal of two cards
        self.cards = [cards.deal_one(), cards.deal_one()]
    def add_card(self, name, cards):
        added_card = cards.deal_one()
        self.cards.append(added_card)
        print("{} was added to {} hand.".format(added_card, name))
    def hand_value(self):
        total = 0
        num_aces = 0
        for card in self.cards:
            if card.value == 11:
                num_aces += 1
            total += card.value
        if total > 21 and total <= (21 + 10*num_aces) and num_aces > 0: #If there's aces
               total -= 10*num_aces
               return total
        else:
            return total

game_on = True
print('Welcome to BlackJack! Type in "exit" anytime to quit.')
while True:
    monies = input('How much money have you brought to the table? : ')
    if monies.lower() == 'exit':
        print('Exiting Game.')
        game_on = False
        break
    try:
        monies = int(monies)
        break
    except:
        print('Please bet an integer.')

new_player = Player(monies)

while game_on == True:
    the_deck = Deck()
    the_deck.shuffle()
    player_hand = Hand(the_deck)
    dealer_hand = Hand(the_deck)
    
    bet = 0
    bet_accepted = False
    while bet_accepted == False:
        bet = input('You have ${}, place a bet greater than zero: '.format(new_player.money))
        if bet.lower() == 'exit':
            print('Exiting Game.')
            game_on = False
            break
        try:
            bet = int(bet)
            bet_accepted = new_player.withdraw(bet)
        except:
            print('Please bet an integer.')

    while game_on == True:
        stext = 'Your hand of value {} consists of: '.format(player_hand.hand_value())
        for card in player_hand.cards:
            stext += '{} | '.format(card)
        print(stext)
        stext = 'The dealers hand of value {} consists of: '.format(dealer_hand.hand_value())
        for card in dealer_hand.cards:
            stext += '{} | '.format(card)
        print(stext)
        
        #If either hand is 21 off the hop, round over
        if player_hand.hand_value() == 21 and dealer_hand.hand_value():
            print('A double BlackJack tie! No winner!')
            new_player.deposit(bet)
            break
        elif player_hand.hand_value() == 21: #in blackjack getting 21 is instant-win 
            print('BlackJack! You got 21 off the initial draw and win!')
            new_player.deposit(bet*2)
            break
        elif dealer_hand.hand_value() == 21: #in blackjack getting 21 is instant-win 
            print('BlackJack! Dealer got 21 off the initial draw and you lose!')
            break

        hit_or_stay = ''
        while not (hit_or_stay == 'hit' or hit_or_stay == 'stay' or hit_or_stay == 'exit'):
            hit_or_stay = input('Do you want to hit or stay? (hit/stay): ').lower()

        if hit_or_stay == 'exit':
            print('Exiting Game.')
            game_on = False
            break
        elif hit_or_stay == 'hit': #on hit check for win or bust
            player_hand.add_card('your', the_deck)
            if player_hand.hand_value() == 21: #in blackjack getting 21 is instant-win 
                print('BlackJack! You got 21 and win!')
                new_player.deposit(bet*2)
                break
            elif player_hand.hand_value() > 21:
                print('Bust! You went over 21!')
                break
        elif hit_or_stay == 'stay' and dealer_hand.hand_value() >= 17: #on stay if dealer has more and can't hit (>=17) check for dealer win.
            if dealer_hand.hand_value() >= player_hand.hand_value():
                print('Dealer wins with {} against your {}.'.format(dealer_hand.hand_value(), player_hand.hand_value()))
                break

        #If dealer is below 17, they hit as per rules
        if dealer_hand.hand_value() < 17:
            dealer_hand.add_card("the Dealer's" , the_deck)
            if dealer_hand.hand_value() == 21: #in blackjack getting 21 is instant-win 
                print('BlackJack! Dealer got 21 and you lose!')
                break
            elif dealer_hand.hand_value() > 21:
                print('Dealer Bust! You win!')
                new_player.deposit(bet*2)
                break
        
        #if dealer is 17 or more they do no actions, so check if player has more
        #There's an instance here where dealer can be at 17 while player just got to 18 and technically would win. Instead, they'll need to type 'Stay'
        if (player_hand.hand_value() > dealer_hand.hand_value()) and dealer_hand.hand_value() >= 17:
            print("Your total of {} beats the Dealer's total of {}. You win!".format(player_hand.hand_value(), dealer_hand.hand_value()))
            new_player.deposit(bet*2)
            break
        elif player_hand.hand_value() == dealer_hand.hand_value() and hit_or_stay == 'stay':
            print('The tie goes to the dealer!')
            break


    if new_player.money <= 0 and game_on == True:
        print('You ran out of money! Game over.')
        game_on = False