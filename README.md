# HQApi
HQ Trivia API, written in Python

## Installation
1. Install from pip:
```bash
pip3 install HQApi
```

2. Install from sources:
```bash
git clone https://github.com/katant/HQ-Lib.git
cd HQApi
python3 setup.py install
```

## Usage
Example code to get next US show game:
```python
from HQApi import HQApi

bearer = "Bearer"
api = HQApi(bearer)

print(str(api.get_show()))
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

## HQWebsocket Methods
| Method             | Description        |
|--------------------|--------------------|
| `join`             | Return websocket   |
| `send_json`        | Send custom json   |
| `send_answer`      | Send answer        |
| `send_life`        | Send life          |

## Regions
| Region | Description           |
|--------|-----------------------|
| `1`    | US, United States     |
| `2`    | UK, Great Britain     |
| `3`    | DE, Germany           |
| `4`    | AU, Australia         |
