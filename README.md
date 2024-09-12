# investment_account

curl localhost:8000/api/register-user/ -X POST -H "Content-Type: application/json
" -d '{"username": "bionsolomon2", "password": "123455"}' | jq

{
"id": 2,
"password": "123455",
"last_login": null,
"is_superuser": false,
"username": "bionsolomon",
"first_name": "",
"last_name": "",
"email": "",
"is_staff": false,
"is_active": true,
"date_joined": "2024-09-10T08:01:54.856626Z",
"groups": [],
"user_permissions": []
}

curl localhost:8000/api/login/ -X POST -H "Content-Type: application/json" -d '{"
username": "bionsolomon2", "password": "123455"}' | jq

{
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNjA0MjQ3MiwiaWF0IjoxNzI1OTU2MDcyLCJqdGkiOiIwODc1YTA5MmNjNWY0YjJiODA4MGY0ZGM1OTI0OWU4MCIsInVzZXJfaWQiOjN9.Nh1J5e7zuGCQotsILD1Pnv9HOlCxmrWukDEyDH6o8Zc",
"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTU5NjcyLCJpYXQiOjE3MjU5NTYwNzIsImp0aSI6IjIwYzQ4MmE1MWU3NjQwYjc4MTk1MWZmMTVkYTViZTEzIiwidXNlcl9pZCI6M30.mHIYogViHXjwCOa-oyByA-3tdTegfshDZfww7J9TscE"
}

## ACCOUNT CREATION

### ACCOUNT 1 CREATION

curl localhost:8000/api/create-account/ -H "Content-Type: application/json" -d '{"name": "Account 1", "account_type": "ACC1"}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTU5NjcyLCJpYXQiOjE3MjU5NTYwNzIsImp0aSI6IjIwYzQ4MmE1MWU3NjQwYjc4MTk1MWZmMTVkYTViZTEzIiwidXNlcl9pZCI6M30.mHIYogViHXjwCOa-oyByA-3tdTegfshDZfww7J9TscE" | jq

{
"detail": "You do not have permission to perform this action."
}

### ACCOUNT 2 CREATION

```
curl localhost:8000/api/create-account/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MTI1OTg2LCJpYXQiOjE3MjYxMjIzODYsImp0aSI6ImQ4YjAxYjlkMTZhNjQxMzU5OGRmNmY1YzBhMjc1OWZjIiwidXNlcl9pZCI6M30.S8FAng-n7sW0q5C8VGd8OTtFHI74OD5GHe_HueJQM94" \
  -d '{"name": "Account 2.0", "account_type": "ACC2", "balance": 200}' | jq

```

```
{
  "id": 5,
  "account_type": "ACC2",
  "name": "Account 2.0",
  "description": null,
  "balance": "200.00",
  "owner": 3
}
```

### ACCOUNT 3 CREATION

curl localhost:8000/api/create-account/ -H "Content-Type: application/json" -d '{"name": "Account 3", "account_type": "ACC3"}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6Ik
pXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTU5NjcyLCJpYXQiOjE3MjU5NTYwNzIsImp0aSI6IjIwYzQ4MmE
1MWU3NjQwYjc4MTk1MWZmMTVkYTViZTEzIiwidXNlcl9pZCI6M30.mHIYogViHXjwCOa-oyByA-3tdTegfshDZfww7J9TscE" | jq

{
"name": "Account 3",
"description": null,
"amount_deposited": "0.00",
"owner": 3,
"account_type": "ACC3"
}

## VIEW ACCOUNT

### VIEW ACCOUNT TYPE 1

curl localhost:8000/api/view-account/3/ -H "Authorization: Bearer eyJhbGciOiJIUz
I1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTU5NjcyLCJpYXQiOjE3MjU5NTYwNzIsImp
0aSI6IjIwYzQ4MmE1MWU3NjQwYjc4MTk1MWZmMTVkYTViZTEzIiwidXNlcl9pZCI6M30.mHIYogViHXjwCOa-oyByA-3tdTegfshDZ
fww7J9TscE" | jq

```
{
  "account": {
    "id": 3,
    "account_type": "ACC1",
    "name": "Account 1",
    "description": null,
    "balance": "0.00",
    "owner": 1
  },
  "transcations": []
}
```

### VIEW ACCOUNT TYPE 2

curl localhost:8000/api/view-account/5/ -H "Authorization: Bearer eyJhbGciOiJIUz
I1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTU5NjcyLCJpYXQiOjE3MjU5NTYwNzIsImp
0aSI6IjIwYzQ4MmE1MWU3NjQwYjc4MTk1MWZmMTVkYTViZTEzIiwidXNlcl9pZCI6M30.mHIYogViHXjwCOa-oyByA-3tdTegfshDZ
fww7J9TscE" | jq

```
{
  "account": {
    "id": 5,
    "account_type": "ACC2",
    "name": "Account 2.0",
    "description": null,
    "balance": "200.00",
    "owner": 3
  },
  "transcations": [
    {
      "id": 2,
      "transaction_type": "Deposit",
      "created_at": "2024-09-12T06:39:09.200183Z",
      "amount": "200.00",
      "transaction_by": 3,
      "account": 5
    }
  ]
}
```

### VIEW ACCOUNT TYPE 3

url localhost:8000/api/view-account/2/ -H "Authorization: Bearer eyJhbGciOiJIUz
I1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTU5NjcyLCJpYXQiOjE3MjU5NTYwNzIsImp
0aSI6IjIwYzQ4MmE1MWU3NjQwYjc4MTk1MWZmMTVkYTViZTEzIiwidXNlcl9pZCI6M30.mHIYogViHXjwCOa-oyByA-3tdTegfshDZ
fww7J9TscE" | jq

```
{
  "error": "Permission Denied, You do not have permission to perform this action."
}
```

## UPDATING ACCOUNT

### UPDATING ACCOUNT TYPE 1

curl localhost:8000/api/update-account/3/ -H "Authorization: Bearer eyJhbGciOiJI
UzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTYzOTU0LCJpYXQiOjE3MjU5NTYwNzIsI
mp0aSI6IjJiZTc2YzUwY2U4MTQ5NDlhNjIyMThhYjQ5MDQ0OTdjIiwidXNlcl9pZCI6M30.u6lKL9yojif98fTVnSjT7wLfW1i0HUD
v29FjWM7eC0E" -X PUT -d '{"amount_deposited": 1000}' | jq

{
"error": "Permission Denied, You do not have permission to perform this action."
}

### UPDATING ACOUNT TYPE 2

curl localhost:8000/api/update-account/1/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTYzOTU0LCJpYXQiOjE3MjU5NTYwNzIsImp0aSI6IjJiZTc2YzUwY2U4MTQ5NDlhNjIyMThhYjQ5MDQ0OTdjIiwidXNlcl9pZCI6M30.u6lKL9yojif98fTVnSjT7wLfW1i0HUDv29FjWM7eC0E" -X PUT -d '{"balance": 1000}'-H "Content-Type: application/json" | jq

{
"id": 5,
"account_type": "ACC2",
"name": "Account 2.0",
"description": null,
"balance": "1200.00",
"owner": 3
}

### UPDATING ACCOUNT TYPE 3

curl localhost:8000/api/update-account/2/ -H "Authorization: Bearer eyJhbGciOiJI
UzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTYzOTU0LCJpYXQiOjE3MjU5NTYwNzIsI
mp0aSI6IjJiZTc2YzUwY2U4MTQ5NDlhNjIyMThhYjQ5MDQ0OTdjIiwidXNlcl9pZCI6M30.u6lKL9yojif98fTVnSjT7wLfW1i0HUD
v29FjWM7eC0E" -X PUT -d '{"amount_deposited": 1000}' | jq
{
"error": "Permission Denied, You do not have permission to perform this action."
}

## DELETING AN ACCOUNT

### DELETING ACCOUNT TYPE 1

curl localhost:8000/api/delete-account/3/ \-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTYzOTU0LCJpYXQiOjE3MjU5NTYwNzIsImp0aSI6IjJiZTc2YzUwY2U4MTQ5NDlhNjIyMThhYjQ5MDQ0OTdjIiwidXNlcl9pZCI6M30.u6lKL9yojif98fTVnSjT7wLfW1i0HUDv29FjWM7eC0E" \-X DELETE | jq

```
{
  "error": "Permission Denied, You do not have permission to perform this action."
}
```

### DLEETING ACCOUNT TYPE 2

curl localhost:8000/api/delete-account/1/ \-H "Authorization: Bearer eyJhbGciOiJI
UzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTYzOTU0LCJpYXQiOjE3MjU5NTYwNzIsI
mp0aSI6IjJiZTc2YzUwY2U4MTQ5NDlhNjIyMThhYjQ5MDQ0OTdjIiwidXNlcl9pZCI6M30.u6lKL9yojif98fTVnSjT7wLfW1i0HUD
v29FjWM7eC0E" \-X DELETE | jq

```
"Sucessfully deletered"
```

### DELETING ACCOUNT TYPE 3

curl localhost:8000/api/delete-account/2/ \-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1OTYzOTU0LCJpYXQiOjE3MjU5NTYwNzIsImp0aSI6IjJiZTc2YzUwY2U4MTQ5NDlhNjIyMThhYjQ5MDQ0OTdjIiwidXNlcl9pZCI6M30.u6lKL9yojif98fTVnSjT7wLfW1i0HUDv29FjWM7eC0E" \-X DELETE | jq

```
{
  "error": "Permission Denied, You do not have permission to perform this action."
}
```

### ADMIN GETTING TRANSACTION OF OF A USER

```
{
  "Username": "bionsolomon2",
  "total_balance": 1400,
  "transactions": [
    {
      "id": 1,
      "transaction_type": "Deposit",
      "created_at": "2024-09-12T06:37:44.844667Z",
      "amount": 200,
      "transaction_by_id": 3,
      "account_id": 4,
      "account_type": "ACC2"
    },
    {
      "id": 2,
      "transaction_type": "Deposit",
      "created_at": "2024-09-12T06:39:09.200183Z",
      "amount": 200,
      "transaction_by_id": 3,
      "account_id": 5,
      "account_type": "ACC2"
    },
    {
      "id": 3,
      "transaction_type": "Deposit",
      "created_at": "2024-09-12T07:01:52.405599Z",
      "amount": 1000,
      "transaction_by_id": 3,
      "account_id": 5,
      "account_type": "ACC2"
    },
    {
      "id": 4,
      "transaction_type": "Deposit",
      "created_at": "2024-09-12T07:05:02.071181Z",
      "amount": 1000,
      "transaction_by_id": 3,
      "account_id": 5,
      "account_type": "ACC2"
    },
    {
      "id": 5,
      "transaction_type": "Withdrawal",
      "created_at": "2024-09-12T07:05:39.317264Z",
      "amount": -1000,
      "transaction_by_id": 3,
      "account_id": 5,
      "account_type": "ACC2"
    }
  ],
  "From": "2024-09-12",
  "To": "All Transactions"
}
```
