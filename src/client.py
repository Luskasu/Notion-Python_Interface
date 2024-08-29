from os import getenv
from dotenv import load_dotenv
from loguru import logger
from pages import Page
from requests import post, get
from json import dumps
from config import *
from data_obj import *

class Client:
    def __init__(self, home_id:str, token=getenv("NOTION_TOKEN")):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }
        logger.info("STARTING CLIENT")
        load_dotenv(".env")

        self.token = token
        self.home = self.open_page_by_id(home_id)
        logger.info(f"client home defined to page {self.home.title} at url {self.home.page_url}\n (id {self.home.page_id})")
        logger.info("CLIENT DONE")
      
    def get_user_by_id(self, user_id) -> User:
        url = f"{USERS_ENDPOINT}/{user_id}"
        response = get(url, headers=self.headers)
        results = response.json().get("results")
        
        return User(
            results["id"],
            results["type"],
            results["name"],
            results["avatar_url"]
        )

    def open_page_by_id(self, page_id:str) -> Page:
        url = f"{PAGES_ENDPOINT}/{page_id}"
        response = get(url, headers=self.headers)

        if response.status_code == 200:
            page_icon = response.json().get("icon")
            page_root = response.json().get("parent")
            page_title = response.json().get("properties")
            page_title = page_title["title"]["title"][0]["text"]["content"]
            logger.info(f"Page {page_title} at {response.json().get('url')} retrieved successfully")
        else:
            logger.info(f"Failed to create page. Status code: {response.status_code}")
            logger.info(response.text)
            return
    
        return Page(page_title, page_icon, page_root, response)
    
    def new_page(self, title:str) -> Page:
        return self.home.new_page(title)
