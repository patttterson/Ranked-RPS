from flask import Blueprint

game_bp = Blueprint('game', __name__)

@game_bp.route('/start-game', methods=['POST'])
def start_game():
    return {"message": "nah"}
