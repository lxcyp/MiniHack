import configparser, sys

def getBotUsername():
    path = sys.path[0]
    config = configparser.ConfigParser()
    config.read(path + '/test.cfg')
    bot_username = config.get('TWITTER', 'bot_username')
    return bot_username

def getApiKey():
    path = sys.path[0]
    config = configparser.ConfigParser()
    config.read(path + '/test.cfg')

    api_key = config.get('TWITTER', 'api_key')
    return api_key

def getApiSecret():
    path = sys.path[0]
    config = configparser.ConfigParser()
    config.read(path + '/test.cfg')

    api_secret = config.get('TWITTER', 'api_secret')
    return api_secret

