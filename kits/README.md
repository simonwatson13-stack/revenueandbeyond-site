# Paid kits (private)

Files here are bundled into the `tools` Netlify function and served only after Stripe confirms
payment (see netlify/functions/tools.mjs). They are never published on the site.

File names must match the `file` field of each kit in data/products.json.
