## Mycofile: A Flask RESTful API for cultivators

### Introduction

Mycofile is designed specifically for amateur mycologists but may be of use to cultivators of many varieties. The service acts as a culture library and cultivation log, allowing the tracking of steps in the expansion of mycelial masses. 

### Technical Outline

A Flask RESTful API forms the foundation of the service and communication occurs via JSONified messages. A SQLite database and SQLAlchemy complete the current backend configuration. A React.js client is currently under production.

### API Endpoints

| HTTP Method | CRUD METHOD | URI                                        | Action                    |
|-------------|-------------|--------------------------------------------|---------------------------|
| GET         | READ        | http://[hostname]/api/cultures             | Return all cultures       |
| GET         | READ        | http://[hostname]/api/cultures/[unique_id] | Return single culture     |
| POST        | CREATE      | http://[hostname]/api/cultures             | Add culture               |
| PUT         | UPDATE      | http://[hostname]/api/cultures/[unique_id] | Update culture            |
| DELETE      | DELETE      | http://[hostname]/api/cultures/[unique_id] | Delete culture            |
|-------------|-------------|--------------------------------------------|---------------------------|
| GET         |             | http://[hostname]/ping                     | Ping - system status test |

### License

MIT License.

### Author

@mycognosist (you can find me on Twitter or SSB).
