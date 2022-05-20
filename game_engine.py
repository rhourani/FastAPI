#TODO run the logic here

from random import randrange
import uuid

from fastapi import HTTPException, Response, status
from game_dto import CreatGame, Game, Status, UpdateGame, Winner

class GameEngine:
    
    my_games = []

    def find_game(self, game_id):
        for game in self.my_games:
            if game['id'] == game_id:
                return game

    def find_index_game(self, game_id):
        for i, game in enumerate(self.my_games):
            if game['id'] == game_id:
                return i

    def get_game_service(self):
        return self.my_games

    def get_game_by_id_service(self, game_id):
        game = self.find_game(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"game with id: {game_id} was not found")
        return game

    def create_game_service(self, created_game: CreatGame):
        userHasAMove = False
        userMoveIndex = 0
        userIsCrosses = False

        chBoard = [] 

        for ch in created_game.board:
            chBoard.append(ch)

        for i, ch in enumerate(chBoard):
            if ch != '-':
                userHasAMove = True
                if ch == 'x' or ch == 'X':
                    userIsCrosses = True
                else:
                    userIsCrosses = False
                userMoveIndex = i
        
        locationIndex = 0
        if userHasAMove == False:
            locationIndex = randrange(9)
        else: 
            locationIndex = randrange(9)
            while locationIndex == userMoveIndex:  
                locationIndex = randrange(9)
                if locationIndex != userMoveIndex: 
                    break
            
        if userIsCrosses:
            chBoard[locationIndex] = 'O'
        else:
            chBoard[locationIndex] = 'X'

        tempBoarStr = ''
        tempBoarStr = tempBoarStr.join(chBoard)
        game_id= str(uuid.uuid4())

        new_game = Game()

        new_game.id = game_id
        new_game.board = tempBoarStr
        new_game.status = Status.RUNNING.name
        new_game.user_is_crosses = userIsCrosses

        game_dict = new_game.dict()
        
        self.my_games.append(game_dict)
        return {"location": "http://127.0.0.1:8000/api/v1/games/" + game_id}

    def update_game_service(self, game_id, updated_game : UpdateGame):
        index = self.find_index_game(game_id)
        if index == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        game = Game()
        game = self.my_games[index]
        return self.game_engine( game, updated_game.board)

    def delete_game_service(self, game_id):
        index = self.find_index_game(game_id)
        if index == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)

        self.my_games.pop(index)

        return Response(status_code = status.HTTP_204_NO_CONTENT)
  
    def is_game_draw(self, chBoard):
        tempBoarStr = ''
        tempBoarStr = tempBoarStr.join(chBoard)
        return '-' not in tempBoarStr

    def is_game_won(self, chBoard):
        if self.check_winning(chBoard, 0, 1, 2):
            return {"is_win": True, "winner_name": chBoard[0]}
        if self.check_winning(chBoard, 3, 4, 5):
            return {"is_win": True, "winner_name": chBoard[3]}
        if self.check_winning(chBoard, 6, 7, 8):
            return {"is_win": True, "winner_name": chBoard[6]}
        if self.check_winning(chBoard, 0, 3, 6):
            return {"is_win": True, "winner_name": chBoard[0]}
        if self.check_winning(chBoard, 1, 4, 7):
            return {"is_win": True, "winner_name": chBoard[1]}
        if self.check_winning(chBoard, 2, 5, 8):
            return {"is_win": True, "winner_name": chBoard[2]}
        if self.check_winning(chBoard, 0, 4, 8):
            return {"is_win": True, "winner_name": chBoard[0]}
        if self.check_winning(chBoard, 2, 4, 6):
            return {"is_win": True, "winner_name": chBoard[2]}
        return {"is_win": False}

    def check_winning(self, chBoard, pos1, pos2, pos3):
        if chBoard[pos1] == '-': return False
        return chBoard[pos1] == chBoard[pos2] and chBoard[pos2] == chBoard[pos3]

    def compare_changes_in_old_and_new_board(self, new_board, old_board):
        moves = 0
        for i, ch in enumerate(new_board):
            if new_board[i] == old_board[i]:
                continue
            else:
                if old_board[i] == '-':
                    moves +=1
        return moves == 1

    def game_status(self, winner_name):
        return Status.X_WON.name if winner_name == 'X' or winner_name == 'x' else Status.O_WON.name
        
    def game_engine(self, game : Game, new_board1):
        if new_board1 == None:
         return self.update_game_obj_response(True, "No such game with the uuid: " + game.Id + " provided", None)
        
        #make sure game's rules are followed correctly
        new_board = []
        for ch in new_board1:
            new_board.append(ch)

        old_board = "".join(game['board'])
        if not self.compare_changes_in_old_and_new_board(new_board, old_board):
            return self.update_game_obj_response(True, 
    "You inserted a mark in non empty position or more than one mark!", Game())
        #check if the user won the game
        winner = Winner()
        winner = self.is_game_won(new_board)
        
        if winner['is_win']:
            game['board'] = "".join(new_board)
            game['status'] = self.game_status(winner['winner_name'])
            self.update_game_obj(game)
            return self.update_game_obj_response(False, "Game is Won!", game)
        #pc turn
        if (self.is_game_draw(new_board)):
            game['board'] = "".join(new_board)
            game['status'] = Status.DRAW.name
            self.update_game_obj(game)
            return self.update_game_obj_response(False, "Game is Draw!", game)
        #PC make a move
        index = randrange(9)
        while new_board[index] != '-':  
            index = randrange(9)
            if new_board[index] == '-': 
                break
        new_board[index] = 'O' if game['user_is_crosses'] == True else 'X'
        #validate if PC won
        winner = self.is_game_won(new_board)
        if winner['is_win']:
            game['board'] = "".join(new_board)
            game['status'] = self.game_status(winner['winner_name'])
            self.update_game_obj(game)
            return self.update_game_obj_response(False, "Game is Won!", game)
            
        game['board'] = "".join(new_board)
        game['status'] = Status.RUNNING.name
        self.update_game_obj(game)
        return self.update_game_obj_response(False, "User Turn", game)

    def update_game_obj_response(self, is_error, error_message, game : Game):
        return {"message": error_message,
            "isError": is_error,
            "TicTacToeGameDTO": game}

    def update_game_obj(self, game: Game):
        new_game = Game()

        new_game.id = game['id']
        new_game.board = game['board']
        new_game.status = game['status']
        new_game.user_is_crosses = game['user_is_crosses']

        game_dict = new_game.dict()

        index = self.find_index_game(game['id'])
        self.my_games[index] = game_dict
        