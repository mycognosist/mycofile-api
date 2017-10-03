## Mycofile: A Flask RESTful API for cultivators

### Introduction

Mycofile is designed specifically for amateur mycologists but may be of use to cultivators of many varieties. The service acts as a culture library and cultivation log, allowing the tracking of steps in the expansion of mycelial masses. 

### Technical Outline

A Flask RESTful API forms the foundation of the service and communication occurs via JSONified messages. A SQLite database and SQLAlchemy complete the current backend configuration. A React.js client is currently under development.

### API Endpoints

| HTTP Method | CRUD METHOD | AUTHENTICATED | URI                                        | Action                    |
|-------------|-------------|---------------|--------------------------------------------|---------------------------|
| GET         |             | NO            | http://[hostname]/ping                     | Ping - system status test |
|-------------|-------------|---------------|--------------------------------------------|---------------------------|
| GET         | READ        |               | http://[hostname]/api/users                | Return all users          |
| GET         | READ        |               | http://[hostname]/api/users/[id]           | Return single user        |
| POST        | CREATE      |               | http://[hostname]/api/users                | Add user                  |
|-------------|-------------|---------------|--------------------------------------------|---------------------------|
| POST        |             | NO            | http://[hostname]/api/auth/register        | Register a user           |
| POST        |             | NO            | http://[hostname]/api/auth/login           | Log in a user             |
| GET         |             | YES           | http://[hostname]/api/auth/logout          | Log out a user            |
| GET         |             | YES           | http://[hostname]/api/auth/status          | Get user status           |
|-------------|-------------|---------------|--------------------------------------------|---------------------------|
| GET         | READ        |               | http://[hostname]/api/cultures             | Return all cultures       |
| GET         | READ        |               | http://[hostname]/api/cultures/[unique_id] | Return single culture     |
| POST        | CREATE      |               | http://[hostname]/api/cultures             | Add culture               |
| PUT         | UPDATE      |               | http://[hostname]/api/cultures/[unique_id] | Update culture            |
| DELETE      | DELETE      |               | http://[hostname]/api/cultures/[unique_id] | Delete culture            |
|-------------|-------------|--------------------------------------------|---------------------------|

### License

MIT License.

### Author

@mycognosist (you can find me on Twitter or SSB).
