# revenueandbeyond.com

The live website, as static files. Netlify publishes the `site/` folder on every push to `main` (see `netlify.toml`). There is no build step.

- `site/` the website exactly as served. Edit pages here.
- `tools/add_insight.py` adds a newsletter issue to the Insights section (new page, top of the Insights list, sitemap). Used by the Monday scheduled task after each Sunday Founder Read send.

Seeded on 16 Oct 2026 from the published Netlify deploy of 10 Oct 2026 (deploy 6aca63f1f7fe4fba91f373d6).

Rules
- Every change goes through this repo. Netlify Drop uploads would be overwritten by the next push.
- Keep the hidden pre-engagement form page and any other unlinked pages inside `site/`, or they disappear on the next deploy.
