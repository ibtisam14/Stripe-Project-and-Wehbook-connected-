# Small product selling website using django with stripe integration


# .env file

```
SECRET_KEY = ""
STRIPE_PUBLIC_KEY = ""
STRIPE_PRIVATE_KEY = ""
STRIPE_WEBHOOK_SECRET_KEY = ""
```


# local webhook start command

```
$ stripe listen --forward-to localhost:8000/webhooks/stripe/