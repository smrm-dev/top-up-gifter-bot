from pyrogram import filters
from pyrogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from datetime import datetime
from time import time
import brightid

from .User import User
from .State import State
from ..TopUpGifter import TopUpGifter
from .consts import texts, keyborads


def equality_filter(data):
    return filters.create(
        lambda flt, _, query: flt.data == query.data.split(',')[0],
        data=data
    )


def existance_filter(data: list):
    return filters.create(
        lambda flt, _, query: query.data.split(',')[0] in flt.data,
        data=data
    )


def is_multiple_query():
    def func(flt, client, query):
        user_id = str(query.from_user.id)
        with client.db as db:        
            user_info = dict(client.users.find_one(id=user_id))
            user = User(user_info)
            query_interval = (datetime.now() - user.last_interaction).seconds
            user.last_interaction = datetime.now()
            client.users.update(user.to_dict(), ['id'])
            if query_interval == 0:
                return True
        return False
    return filters.create(func)


def is_not_valid_message():
    def func(flt, client, query):
        user_id = str(query.from_user.id)
        user_info = dict(client.users.find_one(id=user_id))
        user = User(user_info)
        if user.current_message_id == query.message.message_id:
            return False
        return True
    return filters.create(func)    


def is_not_valid_query():
    def func(flt, client, query):
        user_id = str(query.from_user.id)
        user_info = dict(client.users.find_one(id=user_id))
        user = User(user_info)
        query_data = query.data.split(',')
        action = query_data[0]
        if State.is_valid_query(user.state, action):
            return False
        return True
    return filters.create(func)


def back_filter(state: State):
    def func(flt, client, query):
        user_id = str(query.from_user.id)
        user_info = dict(client.users.find_one(id=user_id))
        user = User(user_info)
        query_data = query.data.split(',')
        action = query_data[0]
        if action == 'back' and user.state == flt.state:
            return True
        return False   
    return filters.create(func, state=state)


def is_verified_and_not_awarded():
    def func(flt, client: TopUpGifter, query:CallbackQuery):
        user_id = str(query.from_user.id)
        with client.db as db:
            user_info = dict(client.users.find_one(id=user_id))
            user = User(user_info)
            user_brightid_info = client.node.verifications.get(client.app_name, context_id=user.context_id)
            if user_brightid_info.get('error'):
                if user_brightid_info['errorNum'] == 2:
                    query.answer(text=texts['errors']['not_linked'][user.language], show_alert=True)
                    return False
                elif user_brightid_info['errorNum'] == 3:
                    query.answer(text=texts['errors']['not_verified'][user.language], show_alert=True)
                    return False
                elif user_brightid_info['errorNum'] == 4:
                    query.answer(text=texts['errors']['not_sponsored'][user.language], show_alert=True)
                    op = {
                        'name': 'Sponsor',
                        'contextId': user.context_id,
                        'app': client.app_name,
                        'timestamp': int(time() * 1000),
                        'v': 5
                    }

                    op['sig'] = brightid.tools.sign(op, client.sponsor_private_key)
                    client.node.operations.post(op)
                    return False

            else:
                user_accounts_reward_status = [user_info['isAwarded'] for user_info in client.users.find(contextId=user_brightid_info['contextIds'])]
                if True in user_accounts_reward_status:
                    query.answer(text=texts['errors']['awarded'][user.language], show_alert=True)
                    return False
                return True
    return filters.create(func)

def not_in_receiving():
    def func(flt, client, query: CallbackQuery):
        user_id = str(query.from_user.id)
        with client.db as db:
            user_info = dict(client.users.find_one(id=user_id))
            user = User(user_info)
            user_brightid_info = client.node.verifications.get(client.app_name, context_id=user.context_id)
            user_accounts_states = [user_info['state'] for user_info in client.users.find(contextId=user_brightid_info['contextIds'], state=[State.CHOOSE_OPERATOR, State.GET_PHONE, State.CLAIMED])]
            if user_accounts_states:
                query.answer(text=texts['errors']['in_receiving'][user.language], show_alert=True)
                return False
            user.state = State.CHOOSE_OPERATOR
            user.last_interaction = datetime.now()
            client.users.update(user.to_dict(), ['id'])
            return True 
    return filters.create(func)


def is_waiting_for_phone():
    def func(flt, client, message):
        user_id = str(message.from_user.id)
        with client.db as db:
            user_info = dict(client.users.find_one(id=user_id))
            user = User(user_info)
            if user.state == State.GET_PHONE:
                return True
            return False    
    return filters.create(func)


def check_phone():
    async def func(flt, client: TopUpGifter, message: Message):
        user_id = str(message.from_user.id)
        user_info = dict(client.users.find_one(id=user_id))
        user = User(user_info)
        if len(message.text) != 11:         
            current_message = await message.reply(text=texts['errors']['again'][user.language] + '\n' + texts[State.GET_PHONE][user.language], reply_markup=InlineKeyboardMarkup(keyborads[State.GET_PHONE][user.language]))
            user.current_message_id = current_message.message_id
            user.last_interaction = datetime.now()
            client.users.update(user.to_dict(), ['id'])
            client.db.commit()
            return False
        elif message.text[:2] != '09':
            current_message = await message.reply(text=texts['errors']['again'][user.language] + '\n' + texts[State.GET_PHONE][user.language], reply_markup=InlineKeyboardMarkup(keyborads[State.GET_PHONE][user.language]))
            user.current_message_id = current_message.message_id
            user.last_interaction = datetime.now()
            client.users.update(user.to_dict(), ['id'])
            client.db.commit()
            return False
        elif not message.text.isdigit():
            current_message = await message.reply(text=texts['errors']['again'][user.language] + '\n' + texts[State.GET_PHONE][user.language], reply_markup=InlineKeyboardMarkup(keyborads[State.GET_PHONE][user.language]))
            user.current_message_id = current_message.message_id
            user.last_interaction = datetime.now()
            client.users.update(user.to_dict(), ['id'])
            client.db.commit()
            return False
        return True 
    return filters.create(func)