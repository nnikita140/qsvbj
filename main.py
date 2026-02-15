from dbm import sqlite3
from telebot import TeleBot
from io import BytesIO
import db
from image_manager import init_board

BASE_URL = 'images'
TOKEN = ''
bot = TeleBot(TOKEN)


def converter_to_bytes(board):
    image_io = BytesIO()
    board.save(image_io, 'PNG')
    image_io.seek(0)
    return image_io

@bot.message_handler(commands=['create_game'])
def create_game(message):
    global game_id
    game_id = db.create_game(message.from_user.id)
    bot.send_message(message.from_user.id, 'Вы создали игру с id:' + game_id)
    board, init_pos = init_board()
    db.create_game_state(game_id, 0, init_pos)
    bot.send_photo(message.chat.id, converter_to_bytes(board))


@bot.message_handler(commands=['join_game'])
def join_game(message):
    _, game_id = message.text.split(' ')
    if db.game_full(game_id):
        bot.send_message(message.chat.id, 'Игра уже началась')
        return
    db.join_game(message.from_user.id, game_id)
    bot.send_message(message.chat.id, 'Вы присоединились к игре с id: ' + message.text)
    white_user_id = db.get_user_id(game_id, 'white')
    if white_user_id:
        bot.send_message(white_user_id[0], 'К игре присоединился игрок' + message.from_user.first_name)