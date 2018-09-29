# HQ-Lib
HQ Trivia API, written in Python

## Installation
1. Install from pip:
```bash
pip3 install HQApi
```

2. Install from sources:
```bash
git clone https://github.com/katant/HQ-Lib.git
cd HQ-Lib
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

## Methods
| Method             | Description                                       |
|--------------------|---------------------------------------------------|
| `get_users_me`     | Information about your account                    |
| `get_user`         | Information about account by ID                   |
| `get_payouts_me`   | Information about payouts                         |
| `get_show`         | Information about next show                       |
| `easter_egg`       | Easter egg, gives 1 life once a week              |
| `make_payout`      | Makes payout to your paypal (Can't bypass ban)    |
| `custom`           | Custom request                                    |

## Regions
| Region | Description           |
|--------|-----------------------|
| `1`    | US, United States     |
| `2`    | UK, Great Britain     |
| `3`    | DE, Germany           |
| `4`    | AU, Australia         |
