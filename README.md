# Group Task API

This is an API backend for a group task application. The API can be accessed in **this website (replace when finalized)**. It support the following functionalities.

## Users

---

### Retrieve Users List

Show the list of all users. This feature is only for debugging purposes.

**Endpoint:** `GET /users`

**Permission:** Only superuser can perform this request

**Sample Success Response (Only Data):** 

``` json
{
    "data": [
        {
            "url": "/users/3",
            "pk": 3,
            "username": "johnDoe",
            "email": "johnDoe@me.com",
        },
        {
            "url": "/users/5",
            "pk": 5,
            "username": "janeSteven",
            "email": "janeSteven@me.com",
        },
    ]
}
```

### Create a User

Create a new user based on the given username, email and password. It's important to turn on the HTTPS encription.

**Endpoint:** `POST /users`

**Permission:** No permission is required to create a new user

**Sample Request Payload**

``` json
{
    "username": "johnDoe",
    "email": "johnDoe@me.com",
    "password": "password123",
}
```

**Success Response:** Response Status 201 (Created)

### Retrieve Users Detail

**Endpoint:** `GET /users/<id>`

**Permission:** Only the user can view their own user detail. For now the app doesn't support updating or deleting a user detail.

**Sample Success Response (Data):**

``` json
{
    "data": {
        "url": "/users/3",
        "pk": 3,
        "username": "johnDoe",
        "email": "johnDoe@me.com",
    }
}
```

## Groups

---

### My Groups

Get the list of all groups that a user is currently a part of. Group data is presented in a form of summary

**Endpoint:** `GET /users/<id>/groups`

**Permission:** Only the user can view their group list

**Sample Success Response (Data):**

``` json
{
    "data": { 
        "url": "/users/3",
        "pk": 3,
        "username": "johnDoe",
        "my_groups": [
            {
                "url": "/groups/2",
                "pk": 2,
                "name": "Biology Group Project",
            },
            {
                "url": "/groups/6",
                "pk": 6,
                "name": "Soccer Club Singapore"
            },
        ],
    }
}
```
### Add Person to Group
**Endpoint** `PUT /groups/<group_id>/users/<user_id>`

**Permission:** The user must be the member of the group to add new member to the group

**Success Response:** Request Status 201 (Created)

### Create a Group
By default, the user will be in the group they have created.

**Endpoint:** `POST /groups/`

**Permission:** A user must be authenticated to create a group.

**Request Payload:**
```json
{
    "name": "Biology Group Project",
}
```

**Success Response:** Response Status 201 (Created)

### Group Details
Contains the detail of a group, including the tasks as well as the members of the group

**Endpoint:** `GET /groups/<id>`

**Permission:** Only the members of the group can view the group details

**Success Response (Data):**

``` json
{
    "data": {
        "url": "/groups/2",
        "pk": 2,
        "name": "Biology Group Project",
        "group_tasks": [
            {
                "url": "/tasks/5",
                "pk": 5,
                "name": "Create slides",
                "desc": "5 pages of slides regarding penguin diets and their habitat",
                "group": {
                    "url": "/groups/2",
                    "pk": 2,
                    "name": "Biology Group Project",
                },
                "in_charge": {
                    "url": "/users/3",
                    "pk": 3,
                    "username": "johnDoe",
                    "email": "johnDoe@me.com",
                },
                "due_date": "2020-10-08",
                "is_done": false,
            },
        ],
        "members": [
            {
                "url": "/users/3",
                "pk": 3,
                "username": "johnDoe",
                "email": "johnDoe@me.com",
            },
            {
                "url": "/users/5",
                "pk": 5,
                "username": "janeSteven",
                "email": "janeSteven@me.com",
            },
        ]
    }
}
```

## Tasks

---

### My Tasks
Due date is formatted as `YYYY/MM/DD`.

**Endpoint:** `GET /users/<id>/tasks`

**Permission:** Only the user can view their own tasks list

**Sample Success Response (Data):**

``` json
{
    "data": { 
        "url": "/users/3",
        "pk": 3,
        "username": "johnDoe",
        "my_tasks": [
            {
                "url": "/tasks/5",
                "pk": 5,
                "name": "Create slides",
                "desc": "5 pages of slides regarding penguin diets and their habitat",
                "group": {
                    "url": "/groups/2",
                    "pk": 2,
                    "name": "Biology Group Project",
                },
                "in_charge": {
                    "url": "/users/3",
                    "pk": 3,
                    "username": "johnDoe",
                    "email": "johnDoe@me.com",
                },
                "due_date": "2020-10-08",
                "is_done": false,
            },
            {
                "url": "/tasks/18",
                "pk": 18,
                "name": "Buy Soccer Ball",
                "desc": "Any brand is fine with $30 budget",
                "group": {
                    "url": "/groups/5",
                    "pk": 5,
                    "name": "Soccer Club Singapore",
                },
                "in_charge": {
                    "url": "/users/3",
                    "pk": 3,
                    "username": "johnDoe",
                    "email": "johnDoe@me.com",
                },
                "due_date": "2020-10-13",
                "is_done": true,
            },
        ],
    }
}
```

### Create Task
A valid task is defined as:
1. The `in_charge` of the task is in the group
2. The group exist
3. The user must be a member of the group which they create the task for

**Endpoint** `POST /tasks`

**Permission:** The user must be a member of the group which they create the task for.

**Sample Request Payload:**
```json
{
    "name": "Create slides",
    "desc": "5 pages of slides regarding penguin diets and their habitat",
    "group": {
        "pk": 2,
    },
    "in_charge": {
        "pk": 3,
    },
    "due_date": "2020-08-07"
}
```

**Response:** Response status 201 (Created)
