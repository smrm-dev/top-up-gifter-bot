from pyrogram import Client

app = Client(
    "tel-v-bot",
    bot_token="<your_bot_token>"
)

with app:
    print(app.get_users("username"))