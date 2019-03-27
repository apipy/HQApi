# HQApi
HQ Trivia & Words API, written in Python 

[![Build Status](https://travis-ci.org/katant/HQApi.svg?branch=master)](https://travis-ci.org/katant/HQApi)

## Installation
1. Install from pip (Outdated, use sources method):
```bash
pip3 install HQApi
```

2. Install from sources:
```bash
git clone https://github.com/katant/HQApi.git
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

## HQApi Methods
| Method             | Description                                       |
|--------------------|---------------------------------------------------|
| `get_users_me`     | Information about your account                    |
| `get_user`         | Information about account by ID                   |
| `get_payouts_me`   | Information about payouts                         |
| `get_show`         | Information about next show                       |
| `easter_egg`       | Easter egg, gives 1 life once a week              |
| `make_payout`      | Makes payout to your paypal (Can't bypass ban)    |
| `send_code`        | Send sms or call to number                        |
| `confirm_code`     | Confirm received sms                              |
| `register`         | Register account                                  |
| `aws_credentials`  | Get credentials                                   |
| `delete_avatar`    | Delete avatar                                     |
| `add_friend`       | Add friend                                        |
| `friend_status`    | Get friend status                                 |
| `remove_friend`    | Delete friend                                     |
| `accept_friend`    | Accept friend                                     |
| `check_username`   | Check username availability                       |
| `custom`           | Custom request                                    |

[More info about methods](https://github.com/katant/HQApi/blob/master/HQApi.md) 

## HQWebsocket Methods
| Method             | Description        |
|--------------------|--------------------|
| `get`              | Return websocket   |
| `close`            | Close websocket    |
| `send_json`        | Send custom json   |
| `send_answer`      | Send answer        |
| `send_life`        | Send life          |
| `send_comment`     | Send comment       |
| `send_letter`      | Send letter        |
| `send_wheel`       | Send wheel letter  |
| `get_erasers`      | Get erasers        |
| `send_eraser`      | Send eraser        |

## Examples
| Example             | Description                                                                                    |
|---------------------|------------------------------------------------------------------------------------------------|
| `get_show.py`       | [Get next show](https://github.com/katant/HQApi/blob/master/examples/get_show.py)              |
| `life_bot.py`       | [Life bot to generate lifes](https://github.com/katant/HQApi/blob/master/examples/life_bot.py) |
| `register_login.py` | [Login or register](https://github.com/katant/HQApi/blob/master/examples/register_login.py)    |
| `websocket.py`      | [Work with websocket](https://github.com/katant/HQApi/blob/master/examples/websocket.py)       |
