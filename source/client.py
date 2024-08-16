from os import getenv
from dotenv import load_dotenv
from loguru import logger
from pages import Page
from requests import post
from json import dumps

class Client:
    def __init__(self, home:str, token=getenv("NOTION_TOKEN")):
        load_dotenv(".env")
        self.token = token
        self.home = home
        logger.info("client done")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def new_page(self, title:str, emoji:str, root:str="") -> Page:
        url = "https://api.notion.com/v1/pages"
        if root == "":
            root = self.home


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