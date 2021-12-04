from Games import *
from Player import MinimaxPlayer
from ai_battle import AllPlayerBattle
from eval_funcs import *
from minimax import *

class InteractiveMinimaxGame:
    def __init__(self, game, eval_fn, user_playing_as=None, depth_limit=5) -> None:
        self.game = game
        self.eval_fn = eval_fn
        self.depth_limit = depth_limit
        self.user_playing_as = user_playing_as

    def _do_player_play(self):
        InteractiveMinimaxGame.doPlayerPlay(self.game, self.eval_fn, self.depth_limit)

    def _do_minimax_play(self):
        InteractiveMinimaxGame.doMinimaxPlay(self.game, self.eval_fn, self.depth_limit)

    def _get_who_user_will_play(self):
        self.user_playing_as = InteractiveMinimaxGame.get_who_user_will_play()

    def play(self):
        if self.user_playing_as is None:
            self._get_who_user_will_play()
        InteractiveMinimaxGame.run_game(self.game, user_playing_as=self.user_playing_as,
            eval_fn=self.eval_fn, depth_limit=self.depth_limit)

    @staticmethod
    def try_play(game, eval_fn, depth_limit, play_fn):
        print("\n\n")
        print(game.showBoard())
        play_fn(game, eval_fn, depth_limit)

    @staticmethod
    def run_game(game: Game, user_playing_as: str, eval_fn, depth_limit: int):
        if user_playing_as == "b":
            InteractiveMinimaxGame.try_play(game, eval_fn, depth_limit, InteractiveMinimaxGame.doPlayerPlay)

        curr_play = InteractiveMinimaxGame.doMinimaxPlay

        while game.getWinner() is None:
            InteractiveMinimaxGame.try_play(game, eval_fn, depth_limit, curr_play)
            if user_playing_as != "n":
                if curr_play == InteractiveMinimaxGame.doMinimaxPlay:
                    curr_play = InteractiveMinimaxGame.doPlayerPlay
                else:
                    curr_play = InteractiveMinimaxGame.doMinimaxPlay


        print("\n\n")
        print(game.showBoard())

        final_score = eval_fn(game)

        if final_score == 0:
            print("Draw!")
        elif final_score > 0:
            print("Max wins!")
        else:
            print("Min wins!")

    @staticmethod
    def get_who_user_will_play():
        print("Play as black or white? (n for no player)")
        while True:
            response = input('(b/w/n)> ')
            if response in ["w", "b", "n"]:
                return response
            else:
                print("Enter 'b' or 'w'")

    @staticmethod
    def doPlayerPlay(game: Game, eval_fn, depth_limit) -> None:
        moves = game.getValidMoves()
        if len(moves) == 0:
            return
        print("Possible moves:")
        for i, move in enumerate(moves):
            game.doMove(move)
            val = minimax_val(game, eval_fn, float('-inf'), float('inf'), depth_limit)
            game.undoMoves(1)
            print("  {}) {} ({})".format(i+1, move, val))

        move = ""
        
        while True:
            choice = input('> ')
            try:
                if choice == 'q':
                    exit(0)
                elif choice == 'h':
                    print(game.saveBoardState())
                    continue
                choice = int(choice)
                if choice > 0 and choice <= len(moves):
                    move = moves[choice-1]
                    break
                print("Enter a number between 1 and {}".format(len(moves)))
            except ValueError:
                print("Enter an integer")
        
        game.doMove(move)

    @staticmethod
    def doMinimaxPlay(game: Game, eval_fn, depth_limit) -> None:
        move = minimax_best_move(game, eval_fn, depth_limit=depth_limit)
        print("Minimax plays {}".format(move))
        game.doMove(move)


def get_parsed_args(game_options):
    parser = argparse.ArgumentParser(description='Run interactive minimax game as player or watch agents battle.')
    parser.add_argument('--game', '-g', metavar='game', help="Which game. Options: {}".format(
        ', '.join([f'"{game_str}"' for game_str in game_options])
    ), required=True)
    parser.add_argument('--depth-limit', '-d', metavar='depth', type=int, required=False, help="Game depth limit")
    parser.add_argument('--eval-fn', '-e', metavar='fn_name', required=False, help="Evaluation function")

    return parser.parse_args()

def get_default_eval_fn_and_depth(game):
    default_players = AllPlayerBattle.get_default_players(game_class=game)
    default_minimax_player: MinimaxPlayer = next(filter(lambda p: isinstance(p, MinimaxPlayer), default_players), None)
    if default_minimax_player is None:
        raise Exception(f'No default players found for {game}')
    
    return default_minimax_player.get_eval_func(), default_minimax_player.get_depth_limit()

if __name__ == "__main__":
    import sys
    import argparse

    game_options = ['Checkers', 'Othello', 'Connect4', 'C4Pop10']
    if TicTacToeGame is not None:
        game_options.append('Tic Tac Toe')

    game = None
    depth_limit = None
    eval_fn = None

    if len(sys.argv) > 1:
        parsed_args = get_parsed_args(game_options)
        game = AllPlayerBattle.get_game_from_choice(parsed_args.game.lower())
        defaults_for_game = get_default_eval_fn_and_depth(game)
        if parsed_args.depth_limit:
            depth_limit = parsed_args.depth_limit
        else:
            depth_limit = defaults_for_game[1]
        if parsed_args.eval_fn:
            eval_fn = EvalFnGuide.get_eval_fn_from_str(game, parsed_args.eval_fn)
        else:
            eval_fn = defaults_for_game[0]
    else:
        print("Game options:")
        for i, opt in enumerate(game_options):
            print(f"  {i+1}) {opt}")

        while True:
            response = input('> ')
            if response == '1':
                game = CheckersGame
                break
            elif response == '2':
                game = OthelloGame
                break
            elif response == '3':
                game = Connect4
                break
            elif response == '3':
                game = C4Pop10Game
                break
            elif TicTacToeGame is not None and response == '5':
                game = TicTacToeGame
                break
            print("Choices are " + ', '.join([f"'{i+1}'" for i in range(len(game_options))]))

        eval_fn, depth_limit = get_default_eval_fn_and_depth(game)

    assert game is not None
    assert eval_fn is not None
    assert depth_limit is not None

    print(f'\nPlaying {game} with eval_fn {eval_fn} and depth limit {depth_limit}\n')

    game = game()
    InteractiveMinimaxGame(game, eval_fn=eval_fn, depth_limit=depth_limit).play()