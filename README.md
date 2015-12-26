# Loro
Python twitter reply & fav bot

## Environment variables
```
CONSUMER_KEY="secret"
CONSUMER_SECRET="secret"
ACCESS_TOKEN="secret"
ACCESS_TOKEN_SECRET="secret"
HANDLERS_URL="http://falaciaslogicas.com/index.json"
```

## Handlers example endpoint response

```bash
$ curl http://falaciaslogicas.com/index.json
[
    {
        "description": "El argumento puede tener múltiples significados distintos.",
        "keywords": [
            "anfibología",
            "disemia",
            "polisemia",
            "ambigüedad"
        ],
        "title": "Anfibología",
        "url": "http://falaciaslogicas.com/anfibologia/"
    },
    {
        "description": "El argumento se da por cierto ya que es defendido por una autoridad.",
        "keywords": [
            "Ad verecundiam"
        ],
        "title": "Apelación a la Autoridad",
        "url": "http://falaciaslogicas.com/apelacion-a-la-autoridad/"
    },
    {
        "description": "El argumento se da por cierto porque \"todo el mundo lo hace\".",
        "keywords": [
            "Ad populum"
        ],
        "title": "Apelación a la Multitud",
        "url": "http://falaciaslogicas.com/apelacion-a-la-multitud/"
    }
]
```
