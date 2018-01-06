## Mycofile: A Flask RESTful API for cultivators

### Introduction

Mycofile is designed specifically for amateur mycologists but may be of use to cultivators of many varieties. The service acts as a culture library and cultivation log, allowing the tracking of steps in the expansion of mycelial masses. 

### Technical Outline

A Flask RESTful API forms the foundation of the service and communication occurs via JSONified messages. A SQLite database and SQLAlchemy complete the current backend configuration. A React.js client is currently under development.

### API Endpoints

| HTTP Method | Auth | URI                                     | Action                       |
|-------------|------|-----------------------------------------|------------------------------|
| GET         |      | http://[..]/api/v1/ping                 | Ping - system status test    |
|-------------|------|-----------------------------------------|------------------------------|
| GET         |      | http://[..]/api/v1/cultures             | Return all cultures          |
| GET         |      | http://[..]/api/v1/cultures/[unique_id] | Return single culture        |
| POST        |      | http://[..]/api/v1/cultures             | Add culture                  |
| PUT         |      | http://[..]/api/v1/cultures/[unique_id] | Update culture               |
| DELETE      |      | http://[..]/api/v1/cultures/[unique_id] | Delete culture               |
|-------------|------|-----------------------------------------|------------------------------|
| GET         |      | http://[..]/api/v1/lines                | Return all lines             |
| GET         |      | http://[..]/api/v1/lines/[id]           | Return single line object    |
| POST        |      | http://[..]/api/v1/lines                | Add line object              |
| PUT         |      | http://[..]/api/v1/lines/[id]           | Update line object           |
| DELETE      |      | http://[..]/api/v1/lines/[id]           | Delete line object           |

### License

MIT License.

### Author

@mycognosist (you can find me in the Scuttleverse).
