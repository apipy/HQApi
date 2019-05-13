from HQApi import HQApi

api = HQApi()

phone = int(input("Phone... "))
verification = api.send_code("+" + str(phone), "sms")
# To request call, send sms, wait 30 seconds and then request call
code = int(input("Code... "))

api.confirm_code(verification["verificationId"], code)

name = str(input("Name... "))
referral = str(input("Referral... "))
while True:
    try:
        token = api.register(verification["verificationId"], name, referral)
        break
    except:
        print("Too long")
print("Token: " + token["accessToken"])
