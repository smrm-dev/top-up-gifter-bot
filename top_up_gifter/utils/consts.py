from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from .State import State

texts = {
State.START: {

'en':
'''
Get yourself a verified BrightID account and I'll give you a free top-up for your mobile!
Learn more about BrightID and how to get verified at https://brightid.gitbook.io 
I can only do this for you once!
This is possible for these countries:
..🇮🇷.. IRAN
"Let's begin!"

''',

'fa':
'''
حساب BrightID خود را تایید هویت کنید تا من به شما شارژ رایگان هدیه دهم.
برای اطلاع از روند احراز هویت به لینک https://brightid.gitbook.io مراجعه کنید
این هدیه تنها یکبار قابل دریافت است.
'''
},

State.LINK: {

'en':
'''
Show me you are verified on BrightID!
Scan this QR code with your BrightID app OR tap on the "Link Account" button on your mobile phone.
Confirm the linking process on BrightID app once it is opened.
Click "Next" when BrightID app tells you the linking is successful.
''',

'fa':
'''
حالا باید حساب خود را به برنامه ما لینک کنید.
برای این کار کلید “اتصال حساب” را فشار دهید و یا با گوشی خود QR کد ارسال شده را اسکن کنید.
'''
},

State.CHOOSE_OPERATOR: {
    'en':
'''
Now choose your network career
''',

    'fa':
'''
لطفا اپراتور سیم کارت خود را انتخاب کنید:
'''
},

State.GET_PHONE: {
    'en': 
'''
Your top-up is all ready! Enter the phone number you want it for!
e.g. 0930*
''',

    'fa': 
'''
شماره ای که شارژ را برای آن میخواهید وارد کنید:
نمونه *0930
'''
},

State.CLAIMED: {
    'en':
'''Tada!
The phone number you entered has received a top-up!
Your top-up serial number is: ''',

    'fa':
'''
تبریک

هدیه دریافت شد.

کد پشتیبانی: '''
},

'errors':{
    'again': {
        'en': '**Try again**',

        'fa': '**دوباره تلاش کنید**'
    },

    'multiple_queries': {
        'en':
'''
Please wait until reaching the response.
''',
        'fa':
'''
لطفا تا دریافت جواب کمی صبر کنید.
'''
    },

    'not_valid_query': {
        'en':
'''
This in not a permitted query.
''',
        'fa':
'''
این درخواست مجاز نیست.
'''
    },

    'not_valid_message': {
        'en':
'''
This message is expired.
''',

        'fa':
'''
این پیام منقضی شده است.
'''
    },

    'not_linked': {
        'en': 
'''
Sorry but you did not link your BrightID account to our app.
Do the previous steps to link it.
''',

        'fa':
'''
متاسفانه شما حساب BrightID خود را به برنامه ما لینک نکرده اید.
مراحل قبل را مجددا انجام دهید.
'''
    },

    'not_verified':{
        'en':
'''
You are not yet verified on BrightID.
Learn how to get verified at https://brightid.gitbook.io
Try again once you are verified on BrightID
''',
        'fa':
'''
متاسفانه هویت شما در BrihgtID تایید نشده است.
'''
    },
    
    'awarded':{
        'en':
'''
Seems like you have already got your free top-up!
''',
        'fa':
'''
شما یکبار هدیه را دریافت کرده اید.
'''
    },

    'not_sponsored':{
        'en':
'''
Sorry but you are not sponsored.
We will sponsor you.
Please try again few seconds later.

'''        ,

        'fa':
'''
متاسفانه شما اسپانسر نیستید.
چند ثانیه دیگر مجددا تلاش کنید.
'''
    },

    'in_receiving':{
        'en':
'''
You are receving your top-up in an other telegram account.
''',
        'fa':
'''
شما در حساب تگلرام دیگری در حال دریافت شارژ هستید.
'''
    },

    'our_side':{
        'en': 
'''
Something happend in our side.
Please try again or contact customer support.
''',
        'fa':
'''
مشگلی در سمت ما پیش آمده است.
لطفا مجددا تلاش کنید و یا با پشتیانی تماس بگیرید.
'''
    }
}


}

keyborads = {
    State.START: {
        'en': [
            [InlineKeyboardButton(text='Start', callback_data='link,')],
            [InlineKeyboardButton(text='Help', url='google.com')],
            [InlineKeyboardButton(text='🇮🇷', callback_data='fa,'), InlineKeyboardButton(text='🇬🇧', callback_data='en,')],
        ],

        'fa': [
            [InlineKeyboardButton(text='شروع', callback_data='link,')],
            [InlineKeyboardButton(text='راهنما', url='google.com')],
            [InlineKeyboardButton(text='🇮🇷', callback_data='fa,'), InlineKeyboardButton(text='🇬🇧', callback_data='en,')],
        ]
    },


    State.LINK: lambda deep_link : {
        'en': [
            [InlineKeyboardButton(text='Link Account', url=f'{deep_link}')], 
            [InlineKeyboardButton(text='Back', callback_data=f'back,'), InlineKeyboardButton(text='Next', callback_data=f'choose_operator,')]
        ],

        'fa':[
            [InlineKeyboardButton(text='اتصال حساب', url=f'{deep_link}')], 
            [InlineKeyboardButton(text='قبلی', callback_data=f'back,'), InlineKeyboardButton(text='بعدی', callback_data=f'choose_operator,')]
        ]
    },

    State.CHOOSE_OPERATOR: {
        'en':[
            [InlineKeyboardButton(text='Hamrahe Aval', callback_data='get_phone,MCI'),
                InlineKeyboardButton(text='Irancell', callback_data='get_phone,MTN'),
                InlineKeyboardButton(text='Rightel', callback_data='get_phone,RTL')],
            [InlineKeyboardButton(text='Back', callback_data='back,')]
        ],

        'fa':[
            [InlineKeyboardButton(text='همراه اول', callback_data='get_phone,MCI'),
                InlineKeyboardButton(text='ایرانسل', callback_data='get_phone,MTN'),
                InlineKeyboardButton(text='رایتل', callback_data='get_phone,RTL')],
            [InlineKeyboardButton(text='قبلی', callback_data='back,')]
        ]
    },

    State.GET_PHONE: {
        'en': [
            [InlineKeyboardButton(text='Back', callback_data='back,')]
        ],

        'fa': [
            [InlineKeyboardButton(text='قبلی', callback_data='back,')]
        ],
    }
}
