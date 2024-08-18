from json import dumps
from requests import Response, patch, get
from os import getenv
from re import findall
from dataclasses import dataclass, field
from loguru import logger
from config import *

@dataclass
class Page:
    title:str
    icon:str
    root: str
    response: Response 
    page_url:str = field(init=False)
    page_id:str = field(init=False)
    subpages:dict = field(init=False)
    headers: dict = field(init=False)

    def __post_init__(self):
        self.headers =  {
            "Authorization": f"Bearer {getenv('NOTION_TOKEN')}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }
        self.page_url = self.response.json().get('url')
        self.page_id = self.page_url.split('-')[-1]

    def __str__(self) -> str:
        return f"{self.title}, {self.page_url}, {self.icon}, {self.root}"

    def get_all_subpages(self) -> list:
        all_subpages = {}
        blocks = self.get_all_blocks()
        
        for block in blocks:
            if block.get("has_children"):
                all_subpages.update({block.get('child_page').get('title') : block.get('id')})
        
        return all_subpages

    def get_all_blocks(self) -> list:
        url = f"{NOTION_BASE_URL}/blocks/{self.page_id}/children"
        all_blocks = list(dict())
        
        response = get(url, headers=self.headers)
        
        for block in response.json().get("results"):
            all_blocks.append(block)

        return all_blocks

    def add_heading(self, text:str, level:int, is_toggleable:bool):
        url = f"{NOTION_BASE_URL}/blocks/{self.page_id}/children"
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
        url = f"{NOTION_BASE_URL}/pages/{self.page_id}"
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
        url = f"{NOTION_BASE_URL}/blocks/{self.page_id}/children"


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
            logger.info(f"paragraph created successfully at {self.page_url}")
        else:
            logger.info(f"Failed to add paragraph. Status code: {response.status_code}")
            logger.info(response.text)
            return

        return response

def extract_text_formatting(text) -> list:
    result = []
    pattern = r'\*\*\*(.*?)\*\*\*|\*\*(.*?)\*\*|\*(.*?)\*|(.+?(?=\*\*\*|\*\*|\*|$))'
    matches = findall(pattern, text)

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