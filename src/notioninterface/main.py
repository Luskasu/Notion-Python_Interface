from loguru import logger
from client import Client



if __name__ == '__main__':
    logger.add("logs/main.log", rotation="12:00", retention="10 days")
    logger.info("starting")
    try:
        client = Client("eb0732ffc77245039cff079d5e179cb8")

        rotina_de_nerd = ["fazer janta", "***jogar*** lol", "chorar *no* **banho**"]
        client.home.add_paragraph("")
        client.home.add_paragraph("**rotina de** ***Nerd***")
        client.home.add_to_do_list(rotina_de_nerd)

    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("END")