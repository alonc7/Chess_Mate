from fastapi import HTTPException
from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import uuid
from server_models.chessboard import initial_board
from server_models.position import Position
from server_referee.bishop_rules import is_bishop_move_valid
from server_referee.pawn_rules import is_pawn_valid_move
from server_referee.knight_rules import is_knight_valid_move
from server_referee.rook_rules import is_rook_valid_move
from server_referee.queen_rules import is_queen_valid_move
from server_referee.king_rules import is_king_valid_move
import asyncio
# uvicorn main:app --reload
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

games = {}


class Game:
    def __init__(self):
        self.players = []
        self.websockets = set()
        self.chessboard = initial_board
        # Generate a 6-character join code
        self.join_code = str(uuid.uuid4())[:6]


def get_game(game_id: str = None):
    if game_id not in games:
        raise HTMLResponse(status_code=404, detail="Game not found")
    return games[game_id]


@app.post("/create_game")
async def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = Game()  # Create an instance of the Game class
    join_code = str(uuid.uuid4())[:6]  # Generate a join code
    games[game_id].join_code = join_code
    initial_state = {
        "type": "initial_state",
        "payload": {"chessboard": games[game_id].chessboard, "join_code": join_code}
    }
    for ws in games[game_id].websockets:
        await ws.send_text(json.dumps(initial_state))
    return {"game_id": game_id, "join_code": join_code}


@app.post("/join_game/{join_code}")
def join_game(join_code: str):
    for game_id, game in games.items():
        if game.join_code == join_code:
            game.players.append("Player2")
            return {"game_id": game_id, "message": "Player2 joined the game"}
    return {"error": "No game found"}


piece_type_rules: Dict[str, callable] = {
    'bishop': {
        'is_valid_move': is_bishop_move_valid,
    },
    'pawn': {
        'is_valid_move': is_pawn_valid_move,
    },
    'knight': {
        'is_valid_move': is_knight_valid_move,
    },
    'rook': {
        'is_valid_move': is_rook_valid_move,
    },
    'queen': {
        'is_valid_move': is_queen_valid_move,
    },
    'king': {
        'is_valid_move': is_king_valid_move,
    },
}


async def is_valid_move(played_piece: Dict, destination: Position, cloned_board: List[List[Dict]]) -> bool:
    print('destination as recieed to method to is_valid_move=>:',
          destination.x, destination.y)
    possible_moves = played_piece['possibleMoves']
    start_position = Position(
        played_piece['position']['x'], played_piece['position']['y'])
    piece_type = played_piece['type']
    # # print('Chick-Check', destination.to_dict() in possible_moves)
    # print(f"Checking move for piece: {played_piece} to {destination}")

    if piece_type in piece_type_rules:
        # print('check 1 ', destination.to_dict())
        validation_func = piece_type_rules[piece_type]['is_valid_move']
        if destination.to_dict() in possible_moves:
            # print('check 2')
            await asyncio.sleep(0)
            if validation_func(destination, start_position, played_piece['team'], cloned_board):
                print('Valid move: Finished')
                return True
    return False


@app.post("/make_move/{game_id}")
async def make_move(game_id: str, move: Dict):
    try:
        played_piece = move['payload']['playedPiece']
        destination = Position(**move['payload']['destination'])
        cloned_board = move['payload']['clonedBoard']

        is_valid = await is_valid_move(played_piece, destination, cloned_board)
        print('is_valid', is_valid)

        if is_valid:
            # Update the chessboard state in the Game instance
            games[game_id].chessboard = move  # why not move?

        log_message = f"Move is {'valid' if is_valid else 'invalid'}: {played_piece} to {destination}"
        print(log_message)

        return {"isValidMove": is_valid}

    except Exception as e:
        error_message = f"Error processing moves: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def broadcast_game_state(game_id: str):
    updated_state = {
        "type": "chessboard_update",
        "payload": {"chessboard": games[game_id].chessboard}
    }
    for ws in games[game_id].websockets:
        await ws.send_text(json.dumps(updated_state))


@app.get("/get_latest_game_state/{game_id}")
async def get_latest_game_state(game_id: str):
    if game_id in games:
        # Assuming games[game_id].chessboard contains the latest game state
        return {"chessboard": games[game_id].chessboard}
    else:
        raise HTTPException(status_code=404, detail="Game not found")


async def send_current_state_to_player(websocket: WebSocket, game_id: str):
    if game_id in games:
        current_state = {
            "type": "chessboard_update",
            "payload": {"chessboard": games[game_id].chessboard}
        }
        await websocket.send_text(json.dumps(current_state))
    else:
        await websocket.close()


async def send_current_state_to_player(websocket: WebSocket, game_id: str):
    if game_id in games:
        current_state = {
            "type": "chessboard_update",
            "payload": {"chessboard": games[game_id].chessboard}
        }
        await websocket.send_text(json.dumps(current_state))
    else:
        await websocket.close()


# @app.websocket("/ws/{game_id}")
# async def websocket_endpoint(websocket: WebSocket, game_id: str):
#     try:
#         await websocket.accept()

#         if game_id not in games:
#             games[game_id] = Game()
#             initial_state = {"type": "initial_state", "payload": {
#                 "chessboard": games[game_id].chessboard}}
#             await websocket.send_text(json.dumps({"type": "chessboard_update", "payload": {"chessboard": games[game_id].chessboard}}))

#         if game_id in games:
#             games[game_id].websockets.add(websocket)

#             try:
#                 while True:
#                     data = await websocket.receive_text()
#                     moves = json.loads(data)
#                     await make_move(game_id, moves)
#                     for ws in games[game_id].websockets:
#                         await ws.send_text(data)
#             except WebSocketDisconnect:
#                 pass
#             finally:
#                 games[game_id].websockets.remove(websocket)
#         else:
#             await websocket.close()
#     except Exception as e:
#         print(f"Error in WebSocket endpoint: {e}")


@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    try:
        await websocket.accept()

        if game_id not in games:
            games[game_id] = Game()
            initial_state = {
                "type": "initial_state",
                "payload": {"chessboard": games[game_id].chessboard},
            }
            await websocket.send_text(
                json.dumps(
                    {
                        "type": "chessboard_update",
                        "payload": {"chessboard": games[game_id].chessboard},
                    }
                )
            )

        if game_id in games:
            games[game_id].websockets.add(websocket)

            try:
                while True:
                    data = await websocket.receive_text()
                    print('Received message from client:', data)
                    moves = json.loads(data)
                    await make_move(game_id, moves)
                    for ws in games[game_id].websockets:
                        await ws.send_text(data)
            except WebSocketDisconnect:
                pass
            finally:
                games[game_id].websockets.remove(websocket)
        else:
            await websocket.close()
    except Exception as e:
        print(f"Error in WebSocket endpoint: {e}")
