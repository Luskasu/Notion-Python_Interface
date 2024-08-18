from loguru import logger
from client import Client

if __name__ == '__main__':
    logger.add("logs/main.log", rotation="12:00", retention="10 days")
    logger.info("starting")
    try:
        client = Client("22ee7b2c71ce4331a690d2bc9a1fd976")
        data_classe_test = client.get_page_by_id("33217aca5b6f4eb6b91a010e4ca11a00")
        sub = data_classe_test.get_all_subpages()
        print(sub.get("aaaaaa"))

    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("END")