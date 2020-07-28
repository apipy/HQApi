# HQApi [![Join the chat at https://gitter.im/HQApi/community](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/HQApi/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Build Status](https://travis-ci.org/apipy/HQApi.svg?branch=master)](https://travis-ci.org/apipy/HQApi) [![Downloads](https://pepy.tech/badge/hqapi)](https://pepy.tech/project/hqapi)
HQ Trivia & Words API, written in Python. Looking for contributors

## Installation
1. Install from pip
```bash
python3 -m pip install HQApi
```

2. Install from sources:
```bash
git clone https://github.com/apipy/HQApi.git
cd HQApi
python3 -m pip install -e .
```

## Usage
Example code to get next show time and info:
```python
from HQApi import HQApi

api = HQApi()

print(api.get_show())
```
Or, you can use CLI to fetch methods
```bash
HQApi -h
```

## Examples
| Example             | Description                                                                                        |
|---------------------|----------------------------------------------------------------------------------------------------|
| `get_show.py`       | [Get next show](https://github.com/apipy/HQApi/blob/master/examples/get_show.py)                   |
| `decode_token.py`   | [Get info from token](https://github.com/apipy/HQApi/blob/master/examples/decode_token.py)         |
| `register_login.py` | [Login or register](https://github.com/apipy/HQApi/blob/master/examples/register_login.py)         |
| `websocket.py`      | [Work with websocket](https://github.com/apipy/HQApi/blob/master/examples/websocket.py)            |
| `websocket_event.py`| [Websocket with events](https://github.com/apipy/HQApi/blob/master/examples/websocket_event.py)    |
| `decode_token.py`   | [Decode JWT token](https://github.com/apipy/HQApi/blob/master/examples/decode_token.py)            |
| `upload_avatar.py`  | [Upload avatar](https://github.com/apipy/HQApi/blob/master/examples/upload_avatar.py)              |
| `offair_trivia.py`  | [Offair trivia](https://github.com/apipy/HQApi/blob/master/examples/offair_trivia.py)              |

## Tor
[How to setup Tor to bypass rate limits](https://github.com/apipy/HQApi/blob/master/tor.md)


## What is Red Enigma and Purple Jupiter?
Well, I can't tell publicly about it. You must research it by yourself. Don't even try to ask me. 
Tip: Don't update version. 1.49.8 is great.

## Contact author
* [@lapkioff](https://t.me/lapkioff) - Telegram
* katant.savelev@yandex.ru - Mail
I don't use any another accounts. Anyone who is claiming that he is Katant in Discord, VK, etc is fake.
