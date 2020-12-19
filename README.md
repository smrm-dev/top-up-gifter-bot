# Top-up Gifter bot
> Developed for participating in BrightID bounties in [gitcoin hackathon gr8](https://gitcoin.co/hackathon/gr8).

> This bot gives each person a free top-up.

This repository contains the source code of [@top_up_gifter_bot](https://t.me/top_up_gifter_bot) and instructions for runnig a copy of yourself.

# Requirements
- Python3.6 or higher
- A Telegram API key
- A Telegram bot token
- A BrightID context
- A [inax.ir](inax.ir) account

# Run
1. `git clone https://github.com/mrmousavi78/top-up-gifter-bot.git`
2. `cd top-up-gifter-bot`
3. `python3 -m venv venv && . venv/bin/activate` to create and activate a virtual environment.
4. `pip install -U -r requirements.txt`, to install the requirements.
5. Edit the `config.ini` file with your values.
6. Place your app `sponsor private key` in `__main__.py` like this:
    `sponsor_private_key='SPONSOR_PRIVATE_KEY'`
7. Place you own [inax.ir] account parameters in `top_up_gfter/plugins/messages.py` like this:
```
    data = {
        "method": "topup",
        "username": "<inax.ir_username>",
        "password": "<inax.ir_password>",
        "amount": "<amount of credit card in IRT>",
        "operator": user.operator,
        "mobile": message.text,
        "charge_type": "normal",
        "order_id": str(randint(5,10000)),
        "company": "top-up gifter bot"
    }
```
8. Run with `python -m top_up_gifter`.
9. Stop with <kbd>Ctrl</kbd> + <kbd>C</kbd> and `deactivate` the virtual environment.

# python-brightid
> For SDK bonus

> BrightID SDK for Python

This bot uses [python-brightid](https://pypi.org/project/python-brightid/) for integrating BrightID

[Pooya Fekri](https://github.com/PooyaFekri/) developed this SDK and you can see the source code here: https://github.com/PooyaFekri/python-brightid

# Top-up Gifter BrightID node
> For running BrightID node bonus

Top-up Gifter will use its own BrightID node on http://node.topupgifter.com/brightid/v5/state
# Medium story

You can see [Top-up Gifter](https://mrmousavi.medium.com/top-up-gifter-e03442f77d1e) on medium for guides on how to receive free top-up.