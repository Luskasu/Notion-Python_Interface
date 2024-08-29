from json import dumps
from requests import Response, patch, get, post
from os import getenv
from re import findall
from loguru import logger
from config import *
from data_obj import *

class Page:
    def __init__(self, title:str, icon:str, root:str, response:Response, banner_url:str = None):
        self.headers =  {
            "Authorization": f"Bearer {getenv('NOTION_TOKEN')}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }
        self.title = title
        self.icon = icon
        self.root = root
        self.response = response
        self.page_url = self.response.json().get('url')
        self.page_id = self.page_url.split('-')[-1]

        if banner_url is not None:
            self.add_banner(banner_url)

    def __str__(self) -> str:
        return f"{self.title}, {self.page_url}, {self.icon}, {self.root}"

    def new_page(self, title:str, icon:str = "👍", root_id:str=""):
        """Create a new page in root and retuns an instance of Page class with its attributes.

        Args:
            title (str): The the page title.
            icon (str): An emoji or a external url for a custom image. It will be displayed together the page title.
            root_id (str): The id from root where the new page will be attached. By default, it will be the current page_id.

        Returns:
            Page: a object with the attributes for the new page if created successfully, None otherwise
        """
        if root_id == "":
            root_id = self.page_id

        if icon.startswith("http"):
            icon_object = {
                    "type": "external",
                    "external": {
                        "url": icon
                    }
                }
        else:
            icon_object = {
                    "type": "emoji",
                    "emoji": icon
                }
        data = {
            "parent": {"type": "page_id", "page_id": root_id},
            "icon": icon_object,
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
        response = post(PAGES_ENDPOINT, headers=self.headers, data=dumps(data))

        if response.status_code == 200:
            logger.info(f"Page {title} created successfully at {response.json().get('url')}")
        else:
            logger.info(f"Failed to create page. Status code: {response.status_code}")
            logger.info(response.text)
            return None
        
        return Page(title, icon, root_id, response)

    def list_subpages(self) -> dict:
        """List all subpage blocks in dict format.

        Returns:
            dict: containing all subpages by following format {'page name' : Page}
        
        """
        subpages = {}
        for block in self.list_blocks():
            if block.type == "child_page":
                subpages.update({block.content : block})
        return subpages

    def list_blocks(self) -> list:
        """list all blocks in this page.

        Returns:
            list: where each element is a block object
            
        """
        url = f"{BLOCKS_ENDPOINT}/{self.page_id}/children"
        response = get(url, headers=self.headers)
        if response.status_code == 200:
            blocks = []
            for block in response.json().get("results"):
                try:
                    content = list(block.values())[-1]
                    if next(iter(content)) == 'title':
                        content = content["title"]
                    elif next(iter(content)) == 'rich_text':
                        content = content["rich_text"][0]["text"]["content"]
                    else:
                        logger.info("content not title or rich text")
                        logger.info(type(content))
                    
                    logger.info(list(block.values()))
                except:
                    logger.info("ERRROOOOOOOOOOOR")


                blocks.append(Block(
                    block["id"],
                    block["parent"]["page_id"],
                    block.get("created_time"),
                    block.get("last_edited_time"),
                    block["created_by"]["id"],
                    block["last_edited_by"]["id"],
                    block.get("has_children"),
                    block.get("archived"),
                    block.get("in_trash"),
                    block.get("type"),
                    content
                ))
            return blocks
        
    def add_banner(self, image_url:str) -> Response:
        """Adds a banner to your page by an internet url for image.
        Args:
            image_url(str): The valid image url.

        Returns:
            Response: a response object from request's patch
        """
        self.banner_url = image_url
        url = f"{PAGES_ENDPOINT}/{self.page_id}"
        data = {
            "cover": {
                "type": "external",
                "external": {
                    "url": self.banner_url
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

#write blocks
    def add_paragraph(self, text:str, markdown:bool = True) -> Response:
        """Writes a paragraph block in page by the text. It will also convert MD to notion UI format.

        Args:
            text(str): The text to write.
            markdown(bool): If true, all the text wrapped by * will be converted to italic form,  ** to bold form and *** to italic bold form in notion UI. If false, the text will be send without be modified
        
        Returns:
            Response: the response object from patch request.
        """
        url = f"{BLOCKS_ENDPOINT}/{self.page_id}/children"
        
        if markdown:
            md_text = extract_text_formatting(text)
        else:
            md_text = text

        text_list = [ {
                    "type": "text",
                    "text": {
                        "content": t[1]
                    },
                    "annotations": {
                        "bold": True if t[0] == "bold" or t[0] == "bold_italic" else False,
                        "italic": True if t[0] == "italic" or t[0] == "bold_italic" else False
                    }
                } for t in md_text]

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

    def add_heading(self, text:str, level:int=1, is_toggleable:bool=False) -> Response:
        """Writes a heading block in current page with specified level.
        Args:
            text(str): The text to heading.
            level(int): the level of heading. It will be 1, 2 or 3.
        Returns:
            Response: the response object of the patch request
        """
        if is_toggleable > 3 or is_toggleable < 1:
            raise "heading must be an integer number between 1 to 3."
        url = f"{BLOCKS_ENDPOINT}/{self.page_id}/children"
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

    def add_bulleted_list(self, texts_list:list, markdown:bool=True) -> Response:
        """write a bulleted list to the current page
        Args:
            texts_list(list): A string list where each element will be a line on bulleted list,.
        Returns:
            Response: the response object of the patch request.        
        """
        url = f"{BLOCKS_ENDPOINT}/{self.page_id}/children"
        
        childrens = []
        for line in texts_list:
            if markdown:
                md_line = extract_text_formatting(line)
            else:
                md_line = line
            text_list = [{
                        "type": "text",
                        "text": {
                            "content": chunk[1]
                        },
                        "annotations": {
                            "bold": True if chunk[0] == "bold" or chunk[0] == "bold_italic" else False,
                            "italic": True if chunk[0] == "italic" or chunk[0] == "bold_italic" else False
                        }
                    } for chunk in md_line]

            children = {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": 
                    {
                        "rich_text":text_list
                    }
            }
            childrens.append(children)
        
        #final data
        data = {
            "children": childrens
        }

        response = patch(url, data=dumps(data), headers=self.headers)
        if response.status_code == 200:
            logger.info("foi")
        else:
            logger.exception(response.text)

    def add_numbered_list(self, texts_list:list, markdown:bool=True) -> Response:
        url = f"{BLOCKS_ENDPOINT}/{self.page_id}/children"
        
        childrens = []
        for line in texts_list:
            if markdown:
                md_line = extract_text_formatting(line)
            else:
                md_line = line
            text_list = [{
                        "type": "text",
                        "text": {
                            "content": chunk[1]
                        },
                        "annotations": {
                            "bold": True if chunk[0] == "bold" or chunk[0] == "bold_italic" else False,
                            "italic": True if chunk[0] == "italic" or chunk[0] == "bold_italic" else False
                        }
                    } for chunk in md_line]

            children = {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": 
                    {
                        "rich_text":text_list
                    }
            }
            childrens.append(children)
        
        #final data
        data = {
            "children": childrens
        }

        response = patch(url, data=dumps(data), headers=self.headers)
        if response.status_code == 200:
            logger.info("foi")
        else:
            logger.exception(response.text)

    def add_to_do_list(self, texts_list:list, markdown:bool=True) ->Response:
        url = f"{BLOCKS_ENDPOINT}/{self.page_id}/children"
        
        childrens = []
        for line in texts_list:
            if markdown:
                md_line = extract_text_formatting(line)
            else:
                md_line = line
            text_list = [{
                        "type": "text",
                        "text": {
                            "content": chunk[1]
                        },
                        "annotations": {
                            "bold": True if chunk[0] == "bold" or chunk[0] == "bold_italic" else False,
                            "italic": True if chunk[0] == "italic" or chunk[0] == "bold_italic" else False
                        }
                    } for chunk in md_line]

            children = {
                "object": "block",
                "type": "to_do",
                "to_do": 
                    {
                        "rich_text":text_list,
                    "checked": False   
                    }
            }

            
            childrens.append(children)
        
        #final data
        data = {
            "children": childrens
        }

        response = patch(url, data=dumps(data), headers=self.headers)
        if response.status_code == 200:
            logger.info("foi")
        else:
            logger.exception(response.text)

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

#criar os metodos 
#   Numbered list item
#   To do
#   add_image
#   add_quote 
#   Table
#   Template