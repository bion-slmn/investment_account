# investment_account

This project involves the creation of APIs to manage investment accounts.
Each user can hold three account types, named ACC1, ACC2, and ACC3.
An account must include the following attributes: a name, an owner, an account type, and a balance, which defaults to 0.

When the account balance changes, a transaction is recorded.
Withdrawals are represented as negative transactions, while deposits are recorded as positive values.
This ensures a clear and auditable trail for all balance adjustments.

#### Account Permissions

For **ACC1**, the user has **view-only** permissions, allowing them to access and view the account and its associated transactions.

For **ACC2**, the user has **full control** over the account and transactions, with the ability to **read, create, update, and delete** both the account and its transactions.

For **ACC3**, the user has permission to **create** the account, but no other actions (viewing, updating, or deleting) are allowed.

Here’s a refined version of your instruction:

---

## Getting Started

This project uses **Django** and **Redis** for caching. To set up the project, follow the steps below:

### 1. Install Required Packages

Ensure you have all the necessary dependencies installed by running:

```
pip install -r requirements.txt
```

### 2. Start Redis Server

Start the Redis server with the following command:

```
sudo service redis-server start
```

### 3. Run the Django Application

Once Redis is running, start the Django development server:

```
python3 manage.py runserver
```

## USER CREATION

### Regular User

The user has the register by passing a unique username and password

#### Endpoint:

```
POST api/register-user/
```

#### Example

```
curl localhost:8000/api/register-user/ \
-X POST -H "Content-Type: application/json "\
-d '{"username": "bionsolomon2", "password": "123455"}' | jq
```

#### Expected Results

```
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
```

### Register ADMIN

Use the Django provide command to create and Admin

```
python3 manage.py createsuperuser
```

## LOGIN IN

A user must pass the user name and passowrd to the api to get the access token

> POST api/login/

#### Example

```
curl localhost:8000/api/login/ -X POST \
 -H "Content-Type: application/json" \
 -d '{"username": "bionsolomon2", "password": "*********"}'
```

#### Expeccted Results

```
{
"refresh": "<refresh token>",
"access": "<access token>"
}
```

## ACCOUNT CREATION

### ACCOUNT 1 CREATION

A regualr user doesnt have permission to create investment account type 1, hence it will fail with 403 status code

> POST api/create-account/

#### Example

```
curl localhost:8000/api/create-account/ \
-H "Content-Type: application/json" \
-d '{"name": "Account 1", "account_type": "ACC1"}'
-H "Authorization: Bearer <access token>" | jq
```

#### Returns

```
{
"detail": "You do not have permission to perform this action."
}
```

### ACCOUNT 2 CREATION

A user is allowed to create this account type

#### Example

```
curl localhost:8000/api/create-account/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access token>" \
  -d '{"name": "Account 2.0", "account_type": "ACC2", "balance": 200}' | jq

```

#### Returns

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

The user is allowed to also create account type 3

#### Example

```
curl localhost:8000/api/create-account/ \
-H "Content-Type: application/json" \
-d '{"name": "Account 3", "account_type": "ACC3"}' \
-H "Authorization: Bearer <access token>" | jq
```

#### Returns

```
{
"name": "Account 3",
"description": null,
"amount_deposited": "0.00",
"owner": 3,
"account_type": "ACC3"
}
```

## VIEW ACCOUNT

### VIEW ACCOUNT TYPE 1

A user is allowed to view account type 1 and 2.
The user will see all the transactions and account details
The account id should be passed as to the API

#### Endpoint:

```
api/view-account/<account_id>/
```

#### Example

```
curl localhost:8000/api/view-account/3/ \
-H "Authorization: Bearer <access token>" | jq
```

#### Returns

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

#### Example

```
curl localhost:8000/api/view-account/5/ \
-H "Authorization: Bearer <access token>" | jq
```

#### Returns

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

User is not allowed to view the account details

#### Example

```
curl localhost:8000/api/view-account/2/ \
-H "Authorization: Bearer <access token>" | jq
```

#### Returns

```
{
  "error": "Permission Denied, You do not have permission to perform this action."
}
```

## UPDATING ACCOUNT

A user is only accepted to update or make a transaction in account 2

#### Endpoint:

```
PUT api/update-account/<account_id>/
```

### UPDATING ACCOUNT TYPE 1 AND ACCOUNT TYPE 3

For this 2 account types permission is denied for a the user

#### Example

```
curl localhost:8000/api/update-account/3/ \
-H "Authorization: Bearer <access token>" \
-X PUT -d '{"amount_deposited": 1000}' | jq
```

#### Returns

```
{
"error": "Permission Denied, You do not have permission to perform this action."
}
```

### UPDATING ACOUNT TYPE 2

A user is allowed to update or make transaction, to withdraw -balance is passed and positive is a deposit

#### Example

```
curl localhost:8000/api/update-account/5/  \
-H "Authorization: Bearer <access token>" \
-X PUT -d '{"balance": 1000}'-H \
"Content-Type: application/json" | jq
```

#### Returns

```
{
"id": 5,
"account_type": "ACC2",
"name": "Account 2.0",
"description": null,
"balance": "1200.00",
"owner": 3
}
```

## DELETING AN ACCOUNT

A user can only delete account type 2 the rest permission is denied

#### Endpoint:

```
DELETE api/delete-account/<account_id>/
```

### DELETING ACCOUNT TYPE 1 AND ACCOUNT TYPE 3

For these account types permission id denied and a status is 403

#### Example

```
curl localhost:8000/api/delete-account/3/ \
-H "Authorization: Bearer <access token>" \
-X DELETE
```

#### Returns

```
{
  "error": "Permission Denied, You do not have permission to perform this action."
}
```

### DLEETING ACCOUNT TYPE 2

#### Example

```
curl localhost:8000/api/delete-account/1/ \
-H "Authorization: Bearer <access token>"
\-X DELETE
```

#### Returns

```
"Sucessfully deleted"
```

### ADMIN GETTING TRANSACTION OF OF A USER

An admin must log in and obtain an access token to use this API. The user_id is required in the API request.

Optional filters include start_date and end_date.
The start_date should be later than the end_date, and the end_date must be in the past.
If no start_date is provided, today's date is used.

#### Endpoint:

```
GET api/view-user-accounts/<user_id>/

GET api/view-user-accounts/<user_id>/?end_date=2024-07-01

GET api/view-user-accounts/<user_id>/?end_date=2024-07-01&start_date=2024-08-03

```

#### Example

```
curl localhost:8000/api/view-user-accounts/1/ -H "Authorization: Bearer <token> "
```

#### Returns

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
