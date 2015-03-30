# docker-infobip-mock

Mock of InfoBip provider (http://www.infobip.com/) for sending SMS

Capability:

* Receives messages by json protocol
* Stores messages into local DB based on sqlite
* Allows read last 10 stored messages in HTML page

Base OS is Ubuntu 14.04.

## Usage:

Pull this repository and build docker-image into repository path:

```bash
docker build -t lukashes/infobip-mock .
```

That is all. Now we will run it:

```bash
docker run -P lukashes/infobip-mock
```

## Allowed URLs:

* POST /api/v3/sendsms/json

## Checking messages:

In your browser open http://localhost:5000/messages and you will see all messages.
If you want to delete it - just kill docker container and run it again.
