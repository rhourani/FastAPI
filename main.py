from fastapi import FastAPI, HTTPException,  status
from game_dto import  CreatGame, UpdateGame
from game_engine import GameEngine

app = FastAPI()

@app.get("/api/v1/games", status_code=status.HTTP_200_OK)
async def get_games():
    GameEngineObject = GameEngine()
    return GameEngineObject.get_game_service()

@app.post("/api/v1/games", status_code=status.HTTP_201_CREATED)
async def create_game(created_game: CreatGame):
    GameEngineObject = GameEngine()
    return GameEngineObject.create_game_service(created_game)

@app.get("/api/v1/games/{game_id}", status_code=status.HTTP_200_OK)
async def get_game_by_id(game_id: str):
    GameEngineObject = GameEngine()
    return GameEngineObject.get_game_by_id_service(game_id)
    
@app.put("/api/v1/games/{game_id}", status_code=status.HTTP_200_OK)
async def update_game(game_id: str, updated_game: UpdateGame):
    GameEngineObject = GameEngine()
    response = GameEngineObject.update_game_service(game_id, updated_game)
    if response['isError'] == True:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response['message'])
    else:
        return response['TicTacToeGameDTO']
    
@app.delete("/api/v1/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id):
    GameEngineObject = GameEngine()
    return GameEngineObject.delete_game_service(game_id)

    