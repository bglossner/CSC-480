from Games import *
from BoardTest import getBoardValue
from mcts import mcts
try:
    from tictactoe import TicTacToeGame
except ModuleNotFoundError:
    TicTacToeGame = None


def doPlayerPlay(game: Game, eval) -> None:
    moves = game.getValidMoves()
    print("Possible moves:")
    for i, move in enumerate(moves):
        print("  {}) {}".format(i+1, move))

    move = ""
    
    while True:
        choice = input('> ')
        try:
            if choice == 'q':
                exit(0)
            choice = int(choice)
            if choice > 0 and choice <= len(moves):
                move = moves[choice-1]
                break
            print("Enter a number between 1 and {}".format(len(moves)))
        except ValueError:
            print("Enter an integer")
    
    game.doMove(move)

def doAIPlay(game: Game) -> None:
    player = game.getPlayer()
    startkey = game.getBoardKey()
    move = mcts(game, player, 300)
    assert game.getBoardKey() == startkey
    print("MCTS plays {}".format(move))
    game.doMove(move)


print("Game options:")
print("  1) Checkers")
print("  2) Othello")
print("  3) C4Pop10")
if TicTacToeGame is not None:
    print("  4) Tic Tac Toe")

while True:
    response = input('> ')
    if response == '1':
        game = CheckersGame()
        break
    elif response == '2':
        game = OthelloGame()
        break
    elif response == '3':
        game = C4Pop10Game()
        break
    elif TicTacToeGame is not None and response == '4':
        game = TicTacToeGame()
        break
    if TicTacToeGame is None:
        print("Choices are '1', '2', '3'")
    else:
        print("Choices are '1', '2', '3', '4'")

no_player = False

print("Play as black or white? (n for no player)")
while True:
    response = input('(b/w/n)> ')
    if response == "b":
        print("\n\n")
        print(game.showBoard())
        doPlayerPlay(game, eval)
        break
    elif response == "w":
        break
    elif response == "n":
        no_player = True
        break
    else:
        print("Enter 'b' or 'w'")

while True:
    print("\n\n")
    print(game.showBoard())
    doAIPlay(game)
    if game.getWinner() is not None:
        break
    if not no_player:
        print("\n\n")
        print(game.showBoard())
        doPlayerPlay(game, eval)
        if game.getWinner() is not None:
            break

print("\n\n")
print(game.showBoard())

print("{} wins!".format(game.getWinner()))