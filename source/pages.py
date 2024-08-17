from json import dumps
from loguru import logger
from requests import Response, patch, get
from os import getenv
from config import *
import re

class Page():
    def __init__(self, title:str, emoji:str, root:str, response:Response):
        self.headers = {
            "Authorization": f"Bearer {getenv('NOTION_TOKEN')}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }

        self.title = title
        self.emoji = emoji
        self.root = root
        self.emoji = emoji
        self.root = root
        self.PAGE_URL = response.json().get('url')
        self.PAGE_ID = self.PAGE_URL.split('-')[-1]
        self.subpages = response.json().get('child_page')
        for key in response.json().get("object"):
            print(key)
    
    def __str__(self) -> str:
        return f"{self.title}, {self.PAGE_URL}, {self.emoji}, {self.root}"
    
    def get_all_subpages(self) -> list:
        url = f"{NOTION_BASE_URL}/blocks/{self.PAGE_ID}/children"
        all_subpages = []


        response = get(url, headers=self.headers)
        print(response.json())
        
        return all_subpages

    def add_heading(self, text:str, level:int, is_toggleable:bool):
        
        url = f"{NOTION_BASE_URL}/blocks/{self.PAGE_ID}/children"
        data = {
            "children": [
                {
                    "object": "block",
                    "type": f"heading_{level}",
                    f"heading_{level}": {
                        "rich_text":[ {
                            "type": "text",
                            "text": {
                                "content": text
                            }
                        }],
                        "is_toggleable": is_toggleable
                    }
                }
            ]
        }
        response = patch(url, headers=self.headers, data=dumps(data))
        if response.status_code == 200:
            logger.info(f"heading added successfully at page {self.title}")
        else:
            logger.info(f"Failed to add headding. Status code: {response.status_code}")
            logger.info(response.text)
            return
        return response

    def add_banner(self, image_url:str) -> Response:
        self.BANNER_URL = image_url
        url = f"{NOTION_BASE_URL}/pages/{self.PAGE_ID}"
        data = {
            "cover": {
                "type": "external",
                "external": {
                    "url": self.BANNER_URL
                }
            }
        }
        response = patch(url, headers=self.headers, data=dumps(data))

        if response.status_code == 200:
            logger.info(f"banner added successfully to the page {self.title}")
        else:
            logger.info(f"Failed to add banner. Status code: {response.status_code}")
            logger.info(response.text)
            return

        return response

    def add_paragraph(self, text:str) -> Response:
        text_list = []
        url = f"{NOTION_BASE_URL}/blocks/{self.PAGE_ID}/children"


        texts = extract_text_formatting(text)

        for t in texts:
            dic = {
                    "type": "text",
                    "text": {
                        "content": t[1]
                    },
                    "annotations": {
                        "bold": True if t[0] == "bold" or t[0] == "bold_italic" else False,
                        "italic": True if t[0] == "italic" or t[0] == "bold_italic" else False
                    }
                }

            text_list.append(dic)

        data = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": text_list
                    }
                }
            ]
        }
        response = patch(url, headers=self.headers, data=dumps(data))

        if response.status_code == 200:
            logger.info(f"paragraph created successfully at {self.PAGE_URL}")
        else:
            logger.info(f"Failed to add paragraph. Status code: {response.status_code}")
            logger.info(response.text)
            return

        return response

def extract_text_formatting(text) -> list:
    result = []
    pattern = r'\*\*\*(.*?)\*\*\*|\*\*(.*?)\*\*|\*(.*?)\*|(.+?(?=\*\*\*|\*\*|\*|$))'
    matches = re.findall(pattern, text)

    for bold_italic, bold, italic, normal in matches:
        if bold_italic:
            result.append(["bold_italic", bold_italic])
        if bold:
            result.append(["bold", bold])
        elif italic:
            result.append(["italic", italic])
        elif normal:
            result.append(["normal", normal])
    return result