# Notion Python Interface
![Notion](https://img.shields.io/badge/-Notion-333333?style=flat&logo=notion) ![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)<br>
Notion Python Interface is a python client to insteract with Notion API. It allows to create and manage pages and taxt blocks in notion through python scripts. It was my first rest api project, and it is still in development! However, fell free to download and test as you like

## Features

- Create new pages in your notion workspace
- Add headers, paragraph, banners and some comming soon text blocks in a page
- Manage children pages
- Markdown formating support
- integrated Loguru's logs

## Installing

To install Notion Python Interface, run:

```bash
pip install notion-python-client
```

### Setup
1. The first thing you need is to create an integration in notion and make sure you have shared the home page you want to edit with it.<br> Read [Notion Integrations](https://www.notion.so/pt/help/create-integrations-with-the-notion-api) if you are not familiar with notion integrations.
2. Since you have a integrantion, run the file setup_env.py or just create a file called ".env" in root directory and write "NOTION_TOKEN=your_api_token" (without quote). you can also store it in yout system local variables.

PAGE IN CONSTRUCTION

## License
this project is under the [MIT License](LICENSE).
