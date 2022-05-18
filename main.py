from http.client import HTTPException
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from game_dto import Game, CreatGame, Status, UpdateGame
from pydantic import BaseModel
import uuid

app = FastAPI()

my_games = []

def find_game(game_id):
    for game in my_games:
        if game['id'] == game_id:
            return game


def find_index_game(game_id):
    for i, game in enumerate(my_games):
        if game['id'] == game_id:
            return i


@app.get("/api/v1/games", status_code=status.HTTP_200_OK)
async def get_games():
    return my_games

@app.post("/api/v1/games", status_code=status.HTTP_201_CREATED)
async def create_game(created_game: CreatGame):
    game_id= str(uuid.uuid4())

    new_game = Game()

    new_game.id = game_id
    new_game.board = created_game.board
    new_game.status = Status.RUNNING

    game_dict = new_game.dict()
    
    my_games.append(game_dict)
    return {"location": "http://127.0.0.1:8000/api/v1/games/" + game_id}

@app.get("/api/v1/games/{game_id}", status_code=status.HTTP_200_OK)
async def get_game_by_id(game_id: str):
    game = find_game(game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"game with id: {game_id} was not found")
    return game

@app.put("/api/v1/games/{game_id}", status_code=status.HTTP_200_OK)
async def update_game(game_id: str, updated_game: UpdateGame):
    index = find_index_game(game_id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)

    updated_new_game = Game()
    updated_new_game.board = updated_game.board
    updated_new_game.id = game_id
    updated_new_game.status = Status.RUNNING

    game_dict = updated_new_game.dict()

    my_games[index] = game_dict

    return {"data": game_dict}


@app.delete("/api/v1/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id):

    index = find_index_game(game_id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)

    my_games.pop(index)

    return Response(status_code = status.HTTP_204_NO_CONTENT)