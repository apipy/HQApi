from HQApi import HQApi

api = HQApi("")

phone = int(input("Phone... "))
verification = api.send_code("+" + str(phone), "sms")
# To request call, send sms, wait 30 seconds and then request call
code = int(input("Code... "))

api.confirm_code(verification["verificationId"], str(code))

name = str(input("Name... "))
refferal = str(input("Refferal... "))
while True:
    try:
        bearer = api.register(verification["verificationId"], name, refferal)
        break
    except:
        print("Too long")
        pass
print("Bearer: "+bearer["accessToken"])
