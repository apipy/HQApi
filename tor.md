# Tor with HQApi

Before we can start, this won't help you to bypass cashout rate limits

## Setup Tor

1. At first, download `Tor Expert Bundle`
2. Create file `torrc` in `Tor` folder
3. Paste `MaxCircuitDirtiness 10` and `NewCircuitPeriod 10` to `torrc` file. It will tell Tor to change IP every 10 seconds
4. (Win) Install Tor as service: `C:\Tor\tor.exe --service install -options -f "C:\Tor\torrc"`


## Setup HQApi

Just change proxy to `socks5://localhost:9050` or check this example

```python
from HQApi import HQApi

api = HQApi(proxy="socks5://localhost:9050")

print(api.get_show())
```
