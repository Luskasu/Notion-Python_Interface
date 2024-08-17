from os import getenv
from dotenv import load_dotenv
from loguru import logger
from pages import Page
from requests import post, get
from json import dumps
from config import *

class Client():
    def __init__(self, home_id:str, token=getenv("NOTION_TOKEN")):
        self.headers = {
            "Authorization": f"Bearer {getenv('NOTION_TOKEN')}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }
        logger.info("STARTING CLIENT")
        load_dotenv(".env")
        self.token = token
        self.home = self.get_page_by_id(home_id)
        logger.info(f"client home defined to page {self.home.title} at url {self.home.PAGE_URL}\n (id {self.home.PAGE_ID})")
        logger.info("CLIENT DONE")
    
    

    def get_page_by_id(self, page_id:str) -> Page:

        url = f"{NOTION_BASE_URL}/pages/{page_id}"

        response = get(url, headers=self.headers)

        page_icon = response.json().get("icon")
        page_root = response.json().get("parent")
        page_title = response.json().get("properties")
        page_title = page_title["title"]["title"][0]["text"]["content"]
        page_url = response.json().get("url")

        return Page(page_title, page_icon, page_root, response)

    def new_page(self, title:str, emoji:str, root:str="") -> Page:
        url = f"{NOTION_BASE_URL}/pages"
        if root == "":
            root = self.home.PAGE_ID

        data = {
            "parent": {"type": "page_id", "page_id": root},
            "icon": {
                "type": "emoji",
                "emoji": emoji
            },
            "properties": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }
        response = post(url, headers=self.headers, data=dumps(data))
        
        if response.status_code == 200:
            logger.info(f"Page {title} created successfully at {response.json().get('url')}")
        else:
            logger.info(f"Failed to create page. Status code: {response.status_code}")
            logger.info(response.text)
            return
        
        return Page(title, emoji, root, response)