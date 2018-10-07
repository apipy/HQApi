import requests


class CheckVersion:
    version = 1.21
    try:
        v = requests.get("https://raw.githubusercontent.com/katant/HQApi/master/version").text
        v = float(v)
        if v > float(version):
            print("Your version of HQApi is outdated. Please, update it via 'pip3 install --upgrade HQApi'!")
    except ValueError:
        version = 0
