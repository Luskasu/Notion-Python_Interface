from os.path import isfile
from loguru import logger

def setup_enf() -> bool:
    with open(".env", "w") as env_file:
        token:str = input("paste here you Notion API integration token (it starts with 'secret-....') \n Access https://www.notion.so/pt/help/create-integrations-with-the-notion-api for more information.\n API-SECRET: ")
        env_file.write(f"NOTION_TOKEN={token}")
    return True
        

if __name__ == '__main__':
    if isfile(".env"):
        logger.info(".env file alread exists.")
    else:
        logger.info(".env not found. Creating .env file....")
        setup_enf()