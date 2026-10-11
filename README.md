# Link shortener

Works like bit.ly, but has the ability to customize preview images and other open graph tags. So you can customize how a link looks if you share it on facebook, twitter and co.

Runs on Django 5.2 LTS, with a [django-unfold](https://unfoldadmin.com/) admin and a
REST API for automation.

## Setup

Clone repository

```
docker compose up -d
docker compose exec web python manage.py createsuperuser
```

The admin is at http://127.0.0.1:8000/admin/, the API docs at
http://127.0.0.1:8000/api/v1/docs/.

To make a short link resolve you first need a **Domain** whose name matches the
host the request arrives on (`127.0.0.1:8000` when developing), and a **Group**
that both the domain and your user belong to.

## Deployment

Every push to `master` is tested, built into
`ghcr.io/digital-organizing/link-shortener` and deployed to the organisation's
app platform, where the app runs as `link-shortener-prod` on the host
`app-daily`. The deploy job joins the tailnet, logs in to the app host through
Tailscale SSH and asks for the deploy; it needs the repository
secrets `TS_OAUTH_CLIENT_ID` and `TS_OAUTH_SECRET` and no SSH key. The
platform runs `python manage.py migrate` before it switches to the new image.

What runs on the server and what the app gets there is decided in the
`digital-organizing/infra` repository, not here:
`apps/link-shortener.compose.yml` (the service and its volume),
`apps/link-shortener.yml` (the domains it answers on,
its budget, the settings that are not secret) and
`secrets/daily/link-shortener.prod.yaml` (`SECRET_KEY`, the database
password). The database arrives as one variable, `DATABASE_URL`.

The app is one container. It serves its static files itself (WhiteNoise;
they are collected into the image at build time) and the uploaded preview
images from the `media` volume. There is no web server in front of it besides
the platform's proxy.

To add a domain the shortener answers on: add it to the app file in the infra
repository, and create the Domain object in the admin.

- `shortener/` — models, the redirect/preview views and the admin
- `shortener/metadata.py` — the open graph scraper, shared by the admin and the API
- `api/` — REST API, the user-bound API key model and its admin


## Tests

```
docker compose exec web python manage.py test
```
