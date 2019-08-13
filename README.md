# HQApi [![Join the chat at https://gitter.im/HQApi/community](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/HQApi/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Build Status](https://travis-ci.org/apipy/HQApi.svg?branch=master)](https://travis-ci.org/apipy/HQApi) [![Downloads](https://pepy.tech/badge/hqapi)](https://pepy.tech/project/hqapi)
HQ Trivia & Words API, written in Python 

## Installation
1. Install from pip (Outdated, use sources method):
```bash
pip3 install HQApi
```

2. Install from sources:
```bash
git clone https://github.com/apipy/HQApi.git
cd HQApi
python3 setup.py install
```

## Usage
Example code to get next show time and info:
```python
from HQApi import HQApi

api = HQApi()

print(api.get_show())
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
| `upload_avatar.py`  | [Upload avatar](https://github.com/apipy/HQApi/blob/master/examples/websocket_event.py)            |
| `offair_trivia.py`  | [Offair trivia](https://github.com/apipy/HQApi/blob/master/examples/websocket_event.py)            |

## Tor
[How to setup Tor to bypass rate limits](https://github.com/apipy/HQApi/blob/master/tor.md)
