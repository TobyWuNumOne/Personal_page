# PocketBase Service (cms)

This service runs PocketBase as a headless CMS for the site.
- Runtime: Docker (Alpine)
- Exposes: $PORT (Railway will inject)
- Data dir: /pb/pb_data (mount a Railway Volume here)
- Public dir: /pb/pb_public

## Deploy (high-level)
1. Push this repo to GitHub.
2. On Railway: New project → Deploy from repo.
3. Add a Volume and mount it to /pb/pb_data.
4. Open the service URL to create the admin account.
5. Set CORS allowed origins to your domains.

## Backup
Download `/pb/pb_data` regularly (SQLite database lives there).
