import logging
import dataset
import brightid

from .TopUpGifter import TopUpGifter


logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='bot.log', filemode='w', level=logging.INFO)

if __name__ == "__main__":
    db = dataset.connect('sqlite:///mydatabase.db')
    node = brightid.Node()
    TopUpGifter(
                db=db,
                node=node,
                app_name='top-up-gifter',
                sponsor_private_key='<SPONSER_PRIVATE_KEY>'
            ).run()