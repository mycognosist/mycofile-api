## Mycofile: A Flask RESTful API for cultivators

### Introduction

Mycofile is designed specifically for amateur mycologists but may be of use to cultivators of many varieties. The service acts as a culture library and cultivation log, allowing the tracking of steps in the expansion of mycelial masses. 

### Technical Outline

A Flask RESTful API forms the foundation of the service and communication occurs via JSONified messages. A SQLite database and SQLAlchemy complete the current backend configuration. A React.js client is currently under development.

### API Endpoints

| HTTP Method | Authenticated | URI                                        | Action                       |
|-------------|---------------|--------------------------------------------|------------------------------|
| GET         | NO            | http://[..]/api/v1/ping                    | Ping - system status test    |
|-------------|---------------|--------------------------------------------|------------------------------|
| GET         |               | http://[..]/api/v1/users                   | Return all users             |
| GET         |               | http://[..]/api/v1/users/[user_id]         | Return single user           |
| POST        |               | http://[..]/api/v1/users                   | Add user                     |
|-------------|---------------|--------------------------------------------|------------------------------|
| POST        | NO            | http://[..]/api/v1/auth/register           | Register a user              |
| POST        | NO            | http://[..]/api/v1/auth/login              | Log in a user                |
| GET         | YES           | http://[..]/api/v1/auth/logout             | Log out a user               |
| GET         | YES           | http://[..]/api/v1/auth/status             | Get user status              |
|-------------|---------------|--------------------------------------------|------------------------------|
| GET         |               | http://[..]/api/v1/cultures                | Return all cultures          |
| GET         |               | http://[..]/api/v1/cultures/[unique_id]    | Return single culture        |
| GET         |               | http://[..]/api/v1/cultures/user/[user_id] | Return all cultures for user |
| POST        |               | http://[..]/api/v1/cultures                | Add culture                  |
| PUT         |               | http://[..]/api/v1/cultures/[unique_id]    | Update culture               |
| DELETE      |               | http://[..]/api/v1/cultures/[unique_id]    | Delete culture               |
|-------------|---------------|--------------------------------------------|------------------------------|
| GET         |               | http://[..]/api/v1/lines                   | Return all lines             |
| GET         |               | http://[..]/api/v1/lines/[id]              | Return single line           |
| POST        |               | http://[..]/api/v1/lines                   | Add line object              |
| PUT         |               | http://[..]/api/v1/lines/[id]              | Update line object           |
| DELETE      |               | http://[..]/api/v1/lines/[id]              | Delete line object           |

### License

MIT License.

### Author

@mycognosist (you can find me on Twitter or SSB).
