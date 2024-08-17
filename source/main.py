from loguru import logger
from client import Client

if __name__ == '__main__':
    logger.add("logs/main.log", rotation="12:00", retention="10 days")
    logger.info("starting")
    try:
        client = Client("22ee7b2c71ce4331a690d2bc9a1fd976")
        a = client.new_page("aaaaaaaaa", "👍")        
        
        
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("END")