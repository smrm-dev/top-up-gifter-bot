from sdk import *
from json import loads
from requests import post
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,KeyboardButton
from hashlib import md5
from datetime import datetime
from random import randint
from texts import texts
import dataset
import os


# '''
# https://meet.brightid.org/#/
# https://play.google.com/store/apps/details?id=org.brightid
# https://apps.apple.com/us/app/brightid/id1428946820
# '''

bright_id = BrightIdSDK()


db = dataset.connect('sqlite:///mydatabase.db')

users = db['user']

start_keyboard = {
    'en': [
        [InlineKeyboardButton(text='Follow steps', callback_data='download,')],
        [InlineKeyboardButton(text='Help', callback_data='help,')],
        [InlineKeyboardButton(text='🇮🇷', callback_data='fa,'), InlineKeyboardButton(text='🇬🇧', callback_data='en,')],
        
    ],
    'fa': [
        [InlineKeyboardButton(text='شروع مراحل', callback_data='download,')],
        [InlineKeyboardButton(text='راهنما', callback_data='help,')],
        [InlineKeyboardButton(text='🇮🇷', callback_data='fa,'), InlineKeyboardButton(text='🇬🇧', callback_data='en,')],
    ]
}

download_keyboard = {
    'en': [
    [InlineKeyboardButton(text='Android', url='https://play.google.com/store/apps/details?id=org.brightid'),
        InlineKeyboardButton(text='IOS',url='https://apps.apple.com/us/app/brightid/id1428946820')],
        [InlineKeyboardButton(text='Back', callback_data='back,start'), InlineKeyboardButton(text='Next', callback_data='BrightID_verify,')]
],
    'fa':[
    [InlineKeyboardButton(text='Android', url='https://play.google.com/store/apps/details?id=org.brightid'),
        InlineKeyboardButton(text='IOS',url='https://apps.apple.com/us/app/brightid/id1428946820')],
        [InlineKeyboardButton(text='قبلی', callback_data='back,start'), InlineKeyboardButton(text='بعدی', callback_data='BrightID_verify,')]
],

}

BrightID_verify_keyboard = {
    'en': [
    [InlineKeyboardButton(text='Back', callback_data='back,download'), InlineKeyboardButton(text='Next', callback_data='deeplink,')]
],

    'fa': [
    [InlineKeyboardButton(text='قبلی', callback_data='back,download'), InlineKeyboardButton(text='بعدی', callback_data='deeplink,')]
],
}

receive_credit_keyboard = {
    'en': [
        [InlineKeyboardButton(text='Receive 5,000 IRT top-up', callback_data='check,')],
        [InlineKeyboardButton(text='Back', callback_data='back,deeplink')]
    ],

    'fa':[
        [InlineKeyboardButton(text='دریافت شارژ هدیه ۵,۰۰۰ تومانی', callback_data='check,')],
        [InlineKeyboardButton(text='قبلی', callback_data='back,deeplink')]
    ]
}

choose_operator_keyboard = {
    'en':[
        [InlineKeyboardButton(text='Hamrahe Aval', callback_data='get_phone,MCI'),
            InlineKeyboardButton(text='Irancell', callback_data='get_phone,MTN'),
            InlineKeyboardButton(text='Rightel', callback_data='get_phone,RTL'),
            InlineKeyboardButton(text='Talia', callback_data='get_phone,TAL')],
        [InlineKeyboardButton(text='Back', callback_data='back,receive')]],

    'fa':[
        [InlineKeyboardButton(text='همراه اول', callback_data='get_phone,MCI'),
            InlineKeyboardButton(text='ایرانسل', callback_data='get_phone,MTN'),
            InlineKeyboardButton(text='رایتل', callback_data='get_phone,RTL'),
            InlineKeyboardButton(text='تالیا', callback_data='get_phone,TAL')],
        [InlineKeyboardButton(text='قبلی', callback_data='back,receive')]]
}

app = Client(':memory:')

def check_status(user_id):
    user = users.find_one(id=str(user_id))
    return user['isWaitingForPhone']

def return_last_bot_message(client, last_message):
    for message_id in range(last_message.message_id,0,-1):
        message = client.get_messages(last_message.from_user.id, message_id)
        if message.empty:
            continue
        if message.from_user.is_self:
            return message
        else:
            message.delete()
    return None

def check_phone_number(user_input):
    if len(user_input) != 11:
        return False
    elif user_input[:2] != '09':
        return False
    elif not user_input.isdigit():
        return False
    return True

@app.on_message()
def my_handler(client, message):

    user = users.find_one(id=str(message.from_user.id))
    if user and check_status(message.from_user.id):
          
        user['isWaitingForPhone'] = False
        users.update(user, ['id'])
        db.commit()

        last_message = message
        last_bot_message = return_last_bot_message(client, last_message)
        if last_bot_message.text == texts['phone_number'][user['lang']]:
            if check_phone_number(message.text):
                user_operator = last_bot_message.reply_markup.inline_keyboard[0][0].callback_data.split(',')[-1]
                client.edit_message_text(message.from_user.id, last_bot_message.message_id, text=texts['phone_submitted'][user['lang']], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Receive' if user['lang'] == 'en' else 'دریافت', callback_data=f'send,{user_operator},{message.text}')],[InlineKeyboardButton(text='Back'  if user['lang'] == 'en' else 'قبلی', callback_data=f'back,get_phone')]]))
            else:
                client.edit_message_text(message.from_user.id, last_bot_message.message_id, text=texts['errors']['again'][user['lang']] + '\n' + texts['operator'][user['lang']], reply_markup=InlineKeyboardMarkup(choose_operator_keyboard[user['lang']]))

        else:
            if last_bot_message:
                last_bot_message.delete()
            client.send_message(message.from_user.id, text=texts['errors']['again'][user['lang']] + '\n' +  texts['operator'][user['lang']], reply_markup=InlineKeyboardMarkup(choose_operator_keyboard[user['lang']]))
            
    elif message.text == '/start':
        if not user:
            users.insert(dict(id=str(message.from_user.id), contextId=make_md5_hash(str(message.from_user.id)), isLinked = False, isVerified=False, isAwarded=False, isWaitingForPhone=False, refCode='_', lang='en'))
            client.send_message(message.from_user.id, text=texts['start']['en'], reply_markup= InlineKeyboardMarkup(start_keyboard['en']))

            db.commit()
        else:
            client.send_message(message.from_user.id, text=texts['start'][user['lang']], reply_markup= InlineKeyboardMarkup(start_keyboard[user['lang']]))
    message.delete()





back_button = lambda prev_state : [[InlineKeyboardButton(text='Back', callback_data=f'back,{prev_state}')]]
back_next_row = lambda prev_state, action: [ [InlineKeyboardButton(text='Back', callback_data=f'back,{prev_state}'), InlineKeyboardButton(text='Next', callback_data=f'{action},')]]
@app.on_callback_query()
def my_handler(client, query):

    query_data = query.data.split(',')
    action = query_data[0]
    user = users.find_one(id=str(query.from_user.id)) 

    if action == 'back':
        if query_data[1] == 'BrightID_verify':
            client.delete_messages(query.from_user.id, int(query_data[2]))
        action = query_data[1]

    if action == 'check':
        context_id = make_md5_hash(str(query.from_user.id))      
        result = check_context_id(context_id)
        if result[0] == 'not_linked':
            client.answer_callback_query(query.id, text=texts['errors']['link'][user['lang']], show_alert=True)
        elif result[1] == 'not_verified':
            client.answer_callback_query(query.id, text=texts['errors']['verify'][user['lang']], show_alert=True)
        elif result[2] == 'received':
            client.answer_callback_query(query.id, text=texts['errors']['awarded'][user['lang']], show_alert=True)
        elif result == ('linked', 'verified','not_received'):
            action = 'choose_operator'
        else:
            client.answer_callback_query(query.id, text=text['errors']['our_side'][user['lang']], show_alert=True)

    if action == 'start':
        client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['start'][user['lang']], reply_markup=InlineKeyboardMarkup(start_keyboard[user['lang']]))
        client.answer_callback_query(query.id)
    elif action == 'fa' or action == 'en':
        if user['lang'] == action:
            client.answer_callback_query(query.id)
        else:
            user['lang'] = 'fa' if action == 'fa' else 'en'
            users.update(user,['id'])
            db.commit()
            client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['start'][user['lang']], reply_markup=InlineKeyboardMarkup(start_keyboard[user['lang']]))
            client.answer_callback_query(query.id)



    elif action == 'help':
        client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['help'][user['lang']], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data='back,start')]]))
        client.answer_callback_query(query.id)
    elif action == 'download':
        client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['download_links'][user['lang']], reply_markup=InlineKeyboardMarkup(download_keyboard[user['lang']]))
        client.answer_callback_query(query.id)
    elif action == 'BrightID_verify':
        client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['BrightID_verify'][user['lang']], reply_markup=InlineKeyboardMarkup(BrightID_verify_keyboard[user['lang']]))
        client.answer_callback_query(query.id)
    elif action == 'deeplink':
        context_id = make_md5_hash(str(query.from_user.id))
        link_account_url = bright_id.createDeepLink(context_id)
        bright_id.createQrCode(link_account_url[0], context_id)
        client.delete_messages(query.from_user.id,query.message.message_id)
        qr_message = client.send_photo(chat_id=query.from_user.id, photo=f'{context_id}.png')
        deep_link_keyboard = {
            'en': [
                [InlineKeyboardButton(text='Link Account', url=link_account_url[1])], 
                [InlineKeyboardButton(text='Back', callback_data=f'back,BrightID_verify,{qr_message.message_id}'), InlineKeyboardButton(text='Next', callback_data=f'receive,{qr_message.message_id}')]
                ],

            'fa':[
                [InlineKeyboardButton(text='اتصال حساب', url=link_account_url[1])], 
                [InlineKeyboardButton(text='قبلی', callback_data=f'back,BrightID_verify,{qr_message.message_id}'), InlineKeyboardButton(text='بعدی', callback_data=f'receive,{qr_message.message_id}')]
                ]
        }
        client.send_message(query.from_user.id, text=texts['link_account'][user['lang']], reply_markup=InlineKeyboardMarkup(deep_link_keyboard[user['lang']]))
        os.remove(f'{context_id}.png')
        client.answer_callback_query(query.id)
    elif action == 'receive':
        if query_data[1] != 'receive':
            client.delete_messages(query.from_user.id,int(query_data[1]))
        client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['receive'][user['lang']], reply_markup=InlineKeyboardMarkup(receive_credit_keyboard[user['lang']]))
        client.answer_callback_query(query.id)
    elif action == 'choose_operator':
        client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['operator'][user['lang']], reply_markup=InlineKeyboardMarkup(choose_operator_keyboard[user['lang']]))
        client.answer_callback_query(query.id)
    elif action == 'get_phone':
        client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['phone_number'][user['lang']], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Back' if user['lang'] == 'en' else 'قبلی', callback_data=f'back,choose_operator,{query_data[1]}')]]))
        client.answer_callback_query(query.id)
        
        user = users.find_one(id=str(query.from_user.id))
        user['isWaitingForPhone'] = True
        users.update(user,['id'])
        db.commit()

    elif action == 'send':
        result = bright_id.checkContextId(make_md5_hash(str(query.from_user.id)))
        user_accounts_reward_status = [user['isAwarded'] for user in users.find(id=result['data']['contextIds'])]
        if True in user_accounts_reward_status:
            client.answer_callback_query(query.id, text=texts['errors']['awarded'][user['lang']], show_alert=True)
        else:
            credit_seller_url = 'https://inax.ir/webservice.php'
            data = {
                "method": "topup",
                "username": "<inax.ir_username>",
                "password": "<inax.ir_password>",
                "amount": "<amount of credit card in IRT>",
                "operator": query_data[1],
                "mobile": query_data[2],
                "charge_type": "normal",
                "order_id": str(query.from_user.id),
                # "order_id": "3",
                "company": "top-up gifter bot"
            }

            result = post(url=credit_seller_url, json=data)
            if result.status_code == 200:
                result = loads(result.text)
                if result['code'] == 1:
                    client.edit_message_text(query.from_user.id, query.message.message_id, text=f'''{texts['finish'][user['lang']]}{result['ref_code']}''', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Back' if user['lang'] == 'en' else 'قبلی', callback_data='back,start')]]))
                    
                    user = users.find_one(id=str(query.from_user.id))                   
                    user['isAwarded'] = True
                    user['refCode'] = result['ref_code']
                    users.update(user,['id'])
                    db.commit()
                    client.answer_callback_query(query.id)

                else:
                    client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['errors']['again'][user['lang']] + '\n' +  texts['operator'][user['lang']], reply_markup=InlineKeyboardMarkup(choose_operator_keyboard[user['lang']]))
                    client.answer_callback_query(query.id, text=result["msg"], show_alert=True)

            else:
                client.edit_message_text(query.from_user.id, query.message.message_id, text=texts['errors']['again'][user['lang']] + '\n' + texts['receive'][user['lang']], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Receive' if user['lang'] == 'en' else 'دریافت', callback_data=f'send,{query_data[1]},{query_data[2]}')],[InlineKeyboardButton(text='Back' if user['lang'] == 'en' else 'قبلی', callback_data=f'back,get_phone')]]))
                client.answer_callback_query(query.id)


def make_md5_hash(tel_id:str):
    has_res = md5(bytes(tel_id, 'ascii'))
    return has_res.hexdigest()

def check_context_id(context_id):
    is_sponsored = False
    while not is_sponsored:
        result = bright_id.checkContextId(context_id)
        if result.get('error'):
            if result['errorNum'] == 2:
                return ('not_linked', '_', '_', '_')
            elif result['errorNum'] == 3:
                return ('linked', 'not_verified', '_', '_')
            elif result['errorNum'] == 4:
                sponsor_result = bright_id.sponsorContextId(context_id)
        else:
            user = users.find_one(contextId=context_id) 
            if not user['isLinked'] or not user['isVerified']:
                user['isLinked'], user['isVerified'] = True, True
                users.update(user,['contextId'])
                db.commit()
            user_accounts_reward_status = [user['isAwarded'] for user in users.find(contextId=result['data']['contextIds'])]
            if True in user_accounts_reward_status:
                return ('linked', 'verified', 'received')
            return ('linked', 'verified', 'not_received')


app.run()
