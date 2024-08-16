from loguru import logger
from client import Client

if __name__ == '__main__':
    logger.add("logs/main.log", rotation="12:00", retention="10 days")
    logger.info("starting")
    try:
        client = Client("22ee7b2c71ce4331a690d2bc9a1fd976")
        lixo = client.new_page("socorro jesus", "🤡")
        lixo.add_paragraph("normal **bold** *italic* ***os dois fds*** ")
        lixo.add_banner("https://i.pinimg.com/736x/93/3f/a8/933fa89df46195c342dcf7dfcd06be0b.jpg")
        lixo.add_heading("1 LIVRO", 1, False)
        lixo.add_heading("1 Capitulo", 2, False)
        lixo.add_heading("1 Seção", 3, True)
        
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("END")