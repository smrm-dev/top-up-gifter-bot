# Be name khoda
import base64
import random
import time
import json
import ed25519

import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
config = config['sdk']
testMode = json.loads(config['TEST_MODE'])
deepLink = 'test.brightid.org' if testMode else 'node.brightid.org'
testURL = 'http://test.brightid.org/brightid/v5'
nodeURL = 'http://node.brightid.org/brightid/v5' if testMode else testURL
appURL = 'https://app.brightid.org/node/v5' if testMode else testURL


class BrightIdSDK:
	# contextId = '0xE8FB09228d1373f931007ca7894a08344B80901c'
    def checkContext():
        response = requests.get(f'{appURL}/verifications/{config["CONTEXT"]}')
        return response.json()

    def checkContextId(contextId:str):
        contextId = contextId.lower()
        response = requests.get(f'{appURL}/verifications/{config["CONTEXT"]}/{contextId}')
        result = response.json()
        return result

    def sponserContextId(contextId:str):
        contextId = contextId.lower()
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

    def createDeepLink(contextId):
        result = f'brightid://link-verification/http:%2f%2f{deepLink}/{config["CONTEXT"]}/{contextId}'
        return result
    
    def addParameter(param, paramType=None, contextId=None):
        addContext = '' if contextId == None else f'/{contextId}'
        addParameter = param if paramType == None else f'?{paramType}={param}'
        url = appURL + addContext + addParameter
        response = requests.get(url)
        return response.json()


# Dar panah khoda