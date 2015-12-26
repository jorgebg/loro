# Loro

Python twitter bot:
- Configured by an external JSON document retrieved through HTTP.
- For each new mention since the last favorited tweet:
    - Tries to reply
    - Favorites the mention tweet

## Handlers endpoint example response

```bash
$ curl http://example.com/index.json
[
    {
        "description": "asdfmovie song",
        "keywords": [
            "trains song",
            "Tom Ska"
        ],
        "title": "I like trains",
        "url": "https://www.youtube.com/watch?v=hHkKJfcBXcw"
    },
    {
        "description": "asdfmovie gag",
        "keywords": [
            "Tom Ska",
            "internet",
            "meme"
        ],
        "title": "Im Going To Do A Internet",
        "url": "http://knowyourmeme.com/memes/im-gonna-do-an-internet"
    }
]
```
