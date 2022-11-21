import random

def display_game(state=[]):
    #create a board with a list input where 0 = Blank, 1 = x, and 2 = o
    state_text = [' ']*9
    for ctr, state_num in enumerate(state):
        if state_num == 1:
            state_text[ctr] = 'x'
        elif state_num == 2:
            state_text[ctr] = 'o'

    print(state_text[6] + ' | ' + state_text[7] + ' | ' + state_text[8] + '   Choices: ' + ('7' if state_text[6] == ' ' else ' ') + ' | ' + ('8' if state_text[7] == ' ' else ' ') + ' | ' + ('9' if state_text[8] == ' ' else ' '))
    print('---------            ---------')
    print(state_text[3] + ' | ' + state_text[4] + ' | ' + state_text[5] + '            ' + ('4' if state_text[3] == ' ' else ' ') + ' | ' + ('5' if state_text[4] == ' ' else ' ') + ' | ' + ('6' if state_text[5] == ' ' else ' '))
    print('---------            ---------')
    print(state_text[0] + ' | ' + state_text[1] + ' | ' + state_text[2] + '            ' + ('1' if state_text[0] == ' ' else ' ') + ' | ' + ('2' if state_text[1] == ' ' else ' ') + ' | ' + ('3' if state_text[2] == ' ' else ' '))

def player_choice(state):
    choice = 'Invalid'
    allowed_choices = []
    for ctr, value in enumerate(state):
        if value == 0:
            allowed_choices.append(str(ctr + 1))
    while choice not in allowed_choices:
        choice = input('Choose placement #:')
        if choice.lower() == 'exit':
            return -1
        elif choice not in allowed_choices:
            print('Invalid input, try again!')
    return int(choice)

def computer_turn(game_state, player_xo):
    #Applly the player's input choice to the board state
    new_game_state = game_state

    #Computer sucks and goes randomly
    if 0 in new_game_state: #check first if computer can even go
        computer_xo = 1
        if player_xo == 1:
            computer_xo = 2

        available_choices = []
        for ctr, value in enumerate(new_game_state):
            if value == 0:
                available_choices.append(ctr + 1)
        random_choice = random.choice(available_choices)
        new_game_state[random_choice-1] = computer_xo

    return new_game_state

def check_for_win(game_state, player_xo):
    winner = -1
    computer_xo = 1
    if player_xo == 1:
        computer_xo = 2
    #Winning states; 1 is a like-placement
    win_conditions = [[1,1,1,0,0,0,0,0,0],\
                      [0,0,0,1,1,1,0,0,0],\
                      [0,0,0,0,0,0,1,1,1],\
                      [1,0,0,1,0,0,1,0,0],\
                      [0,1,0,0,1,0,0,1,0],\
                      [0,0,1,0,0,1,0,0,1],\
                      [0,0,1,0,1,0,1,0,0],\
                      [1,0,0,0,1,0,0,0,1]]
    #Turn each player's board state into a 0, 1 list to check against
    player_x_board = [0]*9
    player_o_board = [0]*9
    for ctr, each in enumerate(game_state):
        if each == 1:
            player_x_board[ctr] = 1
        elif each == 2:
            player_o_board[ctr] = 1

    #Compare and return winning player
    #Perform the Dot product on each board with each win condition
    for each in win_conditions:
        if [i*j for (i, j) in zip(player_x_board, each)] == each:
            winner = 1
        elif [i*j for (i, j) in zip(player_o_board, each)] == each:
            winner = 2

    #Check tie and wins:
    if winner == -1 and 0 not in game_state:
        print('It was a tie!')
    elif winner == player_xo:
        print('Horray, you win!')
    elif winner == computer_xo:
        print('Damn, you suck and lost.')

    return winner

#Main
game_on = True
player_xo = ''
play_again = ''
game_state = [0]*9
print('Welcome to tic-tac-toe!')

while player_xo.upper() != 'X' and player_xo.upper() != 'O':
    player_xo = input('Do you want to be X or O?: ')
    if player_xo.upper() != 'X' and player_xo.upper() != 'O':
        print('Invalid choice, please try again.')

print('You are now ' + player_xo.upper() + ' and your opponent is ' + ('O' if player_xo.upper() == 'X' else 'X') + '.')
print("Type 'exit' anytime to quit. Let's play!\n")

if player_xo.upper() == 'X':
    player_xo = 1
else:
    player_xo = 2

while game_on:
    display_game(game_state)
    player_pick = player_choice(game_state)
    if player_pick == -1:
        print('Exiting game, thanks for playing.')
        game_on = False
    else:
        game_state[player_pick-1] = player_xo #update board with player choice
        win_status = check_for_win(game_state, player_xo)
        if win_status == -1: #if no win, computer takes turn
            game_state = computer_turn(game_state, player_xo)
            win_status = check_for_win(game_state, player_xo)
        if win_status != -1:
            display_game(game_state)
            while play_again.lower() != 'y' and  play_again.lower() != 'n':
                play_again = input('Would you like to play again? (y/n): ')
                if play_again.lower() != 'y' and  play_again.lower() != 'n':
                    print('Invalid input, try again.')
            if play_again.lower() == 'y':
                game_state = [0]*9
                play_again = ''
                print('Retarting game. You are still ' + ('X' if player_xo == 1 else 'O') + '.')
            else:
                print('Exiting game, thanks for playing.')
                game_on = False
    