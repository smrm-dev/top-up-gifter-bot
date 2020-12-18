import logging
from pyrogram import filters, emoji
from pyrogram.types import CallbackQuery, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, Message
from datetime import datetime
from requests import post
from json import loads

from ..TopUpGifter import TopUpGifter
from ..utils.consts import texts, keyborads
from ..utils.functions import make_md5_hash
from ..utils.User import User
from ..utils.State import State
from ..utils.filters import is_waiting_for_phone, check_phone



@TopUpGifter.on_message(filters.command(['start']))
async def start_handler(client: TopUpGifter, message: Message):
    user_id = str(message.from_user.id)
    user_info = client.users.find_one(id=user_id)
    current_message = await message.reply(text=texts[State.START]['en'], reply_markup=InlineKeyboardMarkup(keyborads[State.START]['en']))
    if user_info:
        user = User(user_info)
        user.state = State.START
        user.current_message_id = current_message.message_id
        user.last_interaction = datetime.now()
        client.users.update(user.to_dict(), ['id'])
        client.db.commit()
    else:
        client.users.insert(dict(
                                 id=user_id,
                                 contextId=make_md5_hash(user_id),
                                 lang='en',
                                 state=State.START,
                                 currentMessageId=current_message.message_id,
                                 operator='_',
                                 isAwarded=False,
                                 refCode='_',
                                 lastInteraction = datetime.now()
                                )
                            )


@TopUpGifter.on_message(is_waiting_for_phone() & check_phone())
async def send_top_up(client: TopUpGifter, message: Message):
    user_id = str(message.from_user.id)
    user_info = client.users.find_one(id=user_id)
    user = User(user_info)
    credit_seller_url = 'https://inax.ir/webservice.php'

    data = {
        "method": "topup",
        "username": "<inax.ir_username>",
        "password": "<inax.ir_password>",
        "amount": "<amount of top-up in IRT>",
        "operator": user.operator,
        "mobile": message.text,
        "charge_type": "normal",
        # "order_id": str(query.from_user.id),
        "order_id": str(randint(5,10000)),
        # "order_id": "3",
        "company": "top-up-gifter"
    }

    result = await post(url=credit_seller_url, json=data)
    if result.status_code == 200:
        logging.info(f'{user_id} : 200')
        result = loads(result.text)
        if result['code'] == 1:
            logging.info(f'{user_id} : Award claimed!')
            current_message = await message.reply(text=texts[State.CLAIMED][user.language] + result['ref_code'])
            user.state = State.CLAIMED
            user.current_message_id = current_message.message_id
            user.last_interaction = datetime.now()
            user.is_awarded = True                          
            user.ref_code = result['ref_code']
            client.users.update(user.to_dict(),['id'])
            client.db.commit()

        else:
            logging.info(f'{user_id} : Fail to claim!')
    else:
        logging.info(f'{user_id} : bad status')
