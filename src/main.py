from loguru import logger
from client import Client

if __name__ == '__main__':
    logger.add("logs/main.log", rotation="12:00", retention="10 days")
    logger.info("starting")
    try:
        client = Client("eb0732ffc77245039cff079d5e179cb8")
        sub = client.home.get_all_subpages()
        
        for element in sub.items():
            print(element)


    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("END")