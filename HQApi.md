# HQApi Methods

### Get info about account
To get info about your account, use **get_users_me** method:
```python
api.get_users_me()
```

### Get info about different account
To get info about different account, use **get_user** method:
```python
api.get_user(id)
```

Parameters:
- `id` (`string`) - User ID

### Search
To search people by name, use **search** method:
```python
api.search(name)
```

Parameters:
- `name` (`string`) - Name to search

### Get payout info
To get account payout info, use **get_payouts_me** method:
```python
api.get_payouts_me()
```

### Get next show
To get next show, use **get_show** method:
```python
api.get_show()
```

`Tip: This method doesn't requires token`

### Easter egg
To use easter egg, use **easter_egg** method:
```python
api.easter_egg(type)
```

Parameters:
- `type` (`string`) - Type of easter egg, defaults to `makeItRain`

`Tip: You can use it each two weeks`

### Make payout
To make payout, use **make_payout** method:
```python
api.make_payout(email)
```

Parameters:
- `email` (`string`) - Email to cashout

### Send registration code
To send registration code, use **send_code** method:
```python
api.send_code(phone, method)
```

Parameters:
- `phone` (`string`) - Phone in +xxxxxxxxxxx format
- `method` (`string`) - Method (`sms` or `call`), defaults to `sms`

`Tip: To request call, send sms, wait 30 seconds and then request call`


### Confirm registration code
To confirm code from sms, use **confirm_code** method:
```python
api.confirm_code(verificationid, code)
```

Parameters:
- `verificationid` (`string`) - Verification id from **send_code** method
- `method` (`string`) - Code from sms

### Register account
To register account, use **register** method:
```python
api.register(verificationid, name, referral)
```

Parameters:
- `verificationid` (`string`) - Verification id from **send_code** method
- `name` (`string`) - Username
- `referral` (`string`) - Referring username, defaults to `None`

### AWS Credentials
To get AWS Credentials, use **aws_credentials** method:
```python
api.aws_credentials()
```

### Delete avatar
To delete avatar, use **delete_avatar** method:
```python
api.delete_avatar()
```

### Add friend
To add friend, use **add_friend** method:
```python
api.add_friend(id)
```

Parameters:
- `id` (`string`) - User ID

### Friend status
To get friend status, use **friend_status** method:
```python
api.friend_status(id)
```

Parameters:
- `id` (`string`) - User ID

### Remove friend
To remove friend, use **remove_friend** method:
```python
api.remove_friend(id)
```

Parameters:
- `id` (`string`) - User ID

### Accept friend
To accept friend, use **add_friend** method:
```python
api.accept_friend(id)
```

Parameters:
- `id` (`string`) - User ID

### Check username
To accept friend, use **check_username** method:
```python
api.check_username(name)
```

Parameters:
- `name` (`string`) - User name