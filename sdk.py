# Be name khoda
import base64
import random
import time
import json
import ed25519
import pyqrcode
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
config = config['sdk']
testMode = json.loads(config['TEST_MODE'])
deepLink = 'test.brightid.org' if testMode else 'node.brightid.org'
testURL = 'http://test.brightid.org/brightid/v5'
nodeURL = 'http://node.brightid.org/brightid/v5' if not testMode else testURL
appURL = 'https://app.brightid.org/node/v5' if not testMode else testURL


class BrightIdSDK:
	# contextId = '0xE8FB09228d1373f931007ca7894a08344B80901c'
    def createQrCode(deepLink,contextId):
        qrCode = pyqrcode.create(deepLink)
        qrCode.png(contextId+'.png', scale=8)
         
    def checkContext(self):
        response = requests.get(f'{appURL}/verifications/{config["CONTEXT"]}')
        return response.json()

    def checkContextId(self, contextId:str):
        response = requests.get(f'{appURL}/verifications/{config["CONTEXT"]}/{contextId}')
        result = response.json()
        return result

    def appInfo(self):
        url = appURL + f'/apps/{config["APP_NAME"]}'
        response = requests.get(url)
        return response.json()
    
    def sponsorContextId(self, contextId:str):
        URL = nodeURL + '/operations'
        op = {
			'name': 'Sponsor',
			'app': config['APP_NAME'],
			'contextId': contextId,
			'timestamp': int(time.time()*1000),
			'v': 5
		}
        signing_key = ed25519.SigningKey(base64.b64decode(config['SPONSER_PRIVATE']))
        message = json.dumps(op, sort_keys=True, separators=(',', ':')).encode('ascii')
        sig = signing_key.sign(message)
        op['sig'] = base64.b64encode(sig).decode('ascii')
        response = requests.post(URL, json=op)
        return response.json()

    def createDeepLink(self, contextId):
        qr = f'brightid://link-verification/http:%2f%2f{deepLink}/{config["CONTEXT"]}/{contextId}'
        _link = 'http://'+deepLink if testMode else 'https://app.brightid.org'
        deep = f'{_link}/link-verification/http:%2f%2f{deepLink}/{config["CONTEXT"]}/{contextId}/'
        return qr, deep
    
    def addParameter(self, param, paramType=None, contextId=None):
        addContextId = '' if contextId == None else f'/{contextId}'
        addParameter = f'?{param}'if paramType == None else f'?{paramType}={param}'
        url = appURL+ f'/verifications/{config["CONTEXT"]}' + addContextId + addParameter
        response = requests.get(url)
        return response.json()

    def blockUserVerification(self, contextId, action):
        '''
        'sponsorship', 'link', 'verification'
        '''
        url = nodeURL + f'/testblocks/{config["APP_NAME"]}/{action}/{contextId}'
        params = (
            ('testingKey' ,config['TESTING_KEY']),
            )
        response = requests.put(url, params=params)
        return response
    
    def removeBlockingUser(self, contextId, action):
        url = nodeURL + f'/testblocks/{config["APP_NAME"]}/{action}/{contextId}'
        params = (('testingKey' ,config['TESTING_KEY']),)
        response = requests.delete(url, params=params)
        return response 


# Dar panah khoda