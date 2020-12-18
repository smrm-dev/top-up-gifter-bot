from pyrogram import Client
from brightid import Node

class TopUpGifter(Client):
    def __init__(self, db, node, app_name:str, sponsor_private_key:str):
        super().__init__(
            'session',
            plugins=dict(root=f"top_up_gifter.plugins")
            )
        self.db = db
        self.users = db['user']
        self.node = node
        self.app_name = app_name
        self.sponsor_private_key = sponsor_private_key