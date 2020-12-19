import logging
import brightid
from pyrogram import filters, emoji
from pyrogram.types import CallbackQuery, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, Message
from datetime import datetime
import base64
import os

from ..TopUpGifter import TopUpGifter
from ..utils.State import State
from ..utils.User import User
from ..utils.consts import texts, keyborads
from ..utils.filters import *


@TopUpGifter.on_callback_query(is_multiple_query())
def prevent_multiple_queries_from_a_user(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query.answer(text=texts['errors']['multiple_queries'][user.language], show_alert=True)


@TopUpGifter.on_callback_query(is_not_valid_message())
def bypass_invalid_messages(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query.answer(text=texts['errors']['not_valid_message'][user.language], show_alert=True)


@TopUpGifter.on_callback_query(is_not_valid_query())
def bypass_invalid_queries(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query.answer(text=texts['errors']['not_valid_query'][user.language], show_alert=True)


@TopUpGifter.on_callback_query(equality_filter('back'))
def go_to_previous_step(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query_data = query.data.split(',')
    user.state = State.get_previous_state(user.state)
    user.last_interaction = datetime.now()
    client.users.update(user.to_dict(), ['id'])
    client.db.commit()
    query.continue_propagation()


@TopUpGifter.on_callback_query(existance_filter(['en', 'fa']))
def change_language(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query_data = query.data.split(',')
    action = query_data[0]
    if user.language == action:
        query.answer()
    else:
        query.edit_message_text(text=texts[State.START][action], reply_markup=InlineKeyboardMarkup(keyborads[State.START][action]))
        user.language = action
        user.last_interaction = datetime.now()
        client.users.update(user.to_dict(), ['id'])    
        client.db.commit()
        query.answer()


@TopUpGifter.on_callback_query(back_filter(State.START))
async def start_step(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query_data = query.data.split(',')
    action = query_data[0]
    current_message = await query.message.reply(text=texts[State.START][user.language], reply_markup=InlineKeyboardMarkup(keyborads[State.START][user.language]))
    user.current_message_id = current_message.message_id
    user.last_interaction = datetime.now()
    client.users.update(user.to_dict(), ['id'])
    client.db.commit()
    await query.answer()
    

@TopUpGifter.on_callback_query(equality_filter('link') | back_filter(State.LINK))
async def linking_step(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))
    user = User(user_info)
    query_data = query.data.split(',')
    action = query_data[0]
    deep_link = brightid.tools.create_deep_link(client.app_name, user.context_id)
    qr_deep_link = brightid.tools.create_deep_link(client.app_name, user.context_id, schema='brightid')
    qr_code_base_64 = brightid.tools.create_qr(qr_deep_link, scale=10)
    qr_code = base64.b64decode(qr_code_base_64)
    filename = f'{user.context_id}.png'
    with open(filename, 'wb') as f:
        f.write(qr_code)
    await query.message.reply_photo(filename)
    os.remove(filename)
    current_message = await query.message.reply(text=texts[State.LINK][user.language], reply_markup=InlineKeyboardMarkup(keyborads[State.LINK](deep_link)[user.language]))
    user.state = State.LINK
    user.current_message_id = current_message.message_id
    user.last_interaction = datetime.now()
    client.users.update(user.to_dict(), ['id'])
    client.db.commit()
    await query.answer()


@TopUpGifter.on_callback_query(equality_filter('choose_operator') & is_verified_and_not_awarded() & not_in_receiving() | back_filter(State.CHOOSE_OPERATOR))
async def choose_operator(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query_data = query.data.split(',')
    action = query_data[0]
    current_message = await query.message.reply(text=texts[State.CHOOSE_OPERATOR][user.language], reply_markup=InlineKeyboardMarkup(keyborads[State.CHOOSE_OPERATOR][user.language]))
    user.state = State.CHOOSE_OPERATOR
    user.current_message_id = current_message.message_id
    user.last_interaction = datetime.now()
    client.users.update(user.to_dict(), ['id'])
    client.db.commit()
    await query.answer()


@TopUpGifter.on_callback_query(equality_filter('get_phone'))
async def get_phone(client: TopUpGifter, query: CallbackQuery):
    user_id = str(query.from_user.id)
    user_info = dict(client.users.find_one(id=user_id))    
    user = User(user_info)
    query_data = query.data.split(',')
    action = query_data[0]
    current_message = await query.message.reply(text=texts[State.GET_PHONE][user.language], reply_markup=InlineKeyboardMarkup(keyborads[State.GET_PHONE][user.language]))
    user.state = State.GET_PHONE
    user.operator = query_data[1]
    user.current_message_id = current_message.message_id
    user.last_interaction = datetime.now()
    client.users.update(user.to_dict(), ['id'])
    client.db.commit()
    await query.answer()


# @TopUpGifter.on_callback_query()
# def change_language1(client: TopUpGifter, query: CallbackQuery):
#     user_id = str(query.from_user.id)
#     user_info = dict(client.users.find_one(id=user_id))    
#     user = User(user_info)
#     query_data = query.data.split(',')
#     action = query_data[0]