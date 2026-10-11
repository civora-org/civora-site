# civora.sk

The public landing page for [Civora](https://civora.sk) Zmluvy, the contracts module for Slovak municipalities. The site is a single static page in Slovak, served from GitHub Pages at <https://civora.sk>.

This repository holds only the site. The product, the code and the planning live in the other Civora repositories. See the [Civora platform README](https://github.com/civora-org/civora-platform) for the map.

## Contents

| Path | Purpose |
|---|---|
| `index.html` | The whole page: markup, CSS and JavaScript inline |
| `404.html` | Page for unknown paths. Marked `noindex` |
| `img/` | Screenshots of the product, as PNG and WebP at four widths, and the Open Graph image |
| `fonts/` | Source Sans 3 as self-hosted WOFF2, split into Latin and Slovak-extended subsets |
| `favicon.svg` | Site icon |
| `robots.txt` | Allows all crawlers and points to the sitemap |
| `sitemap.xml` | The home page with its screenshot URLs. Edited by hand |
| `CNAME` | Custom domain (`civora.sk`) for GitHub Pages |
| `.nojekyll` | Stops GitHub Pages from running Jekyll on the files |

The page sections, in order: hero, problem, process, features, a product gallery, the pilot-programme section and a contact call to action.

## Technology

- Plain HTML, CSS and JavaScript. There is no framework, no package manager and no build step.
- All CSS and JavaScript are inline in `index.html`. There are no other scripts or stylesheets.
- Fonts are preloaded from `fonts/`. The page loads no scripts, stylesheets, fonts or frames from third-party hosts.
- The page includes JSON-LD structured data, a canonical link, Open Graph tags and a Twitter card tag. The 404 page carries `<meta name="robots" content="noindex">`.

## Run locally

Use any static file server from the repository root, so that the paths match production:

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

No install is needed. Any server that serves `.webp` as `image/webp` and `.woff2` as a font works.

## Deployment

- The site is published by **GitHub Pages**, with the legacy build from the `main` branch at the root (`/`).
- **Merging to `main` publishes the site.** GitHub builds it; the repository has no CI workflow of its own.
- The custom domain comes from `CNAME`, and HTTPS is enforced on it. GitHub serves `404.html` for unknown paths.
- DNS for `civora.sk` is managed outside this repository.

## Product screenshots

The gallery uses screenshots from the public demo host. They show fictional data only. Never publish a screenshot with real names, e-mail addresses or contract data.

Each screenshot has five files:

- `<name>.png`, the source image;
- `<name>-480.webp`, `<name>-800.webp`, `<name>-1200.webp` and `<name>-1440.webp`, the WebP widths used in `srcset`.

The repository has no script that makes the screenshots or the WebP files. Create them before committing.

### Cache-busting

Every reference to a screenshot or to the Open Graph image has a version query, `?v=YYYYMMDD`. The date is the day the images were last replaced. The current value is `20261006`, and it appears in `img` and `srcset` attributes, the Open Graph image and the JSON-LD image.

When you replace an image:

1. Replace the files in `img/`, keeping the same names, or add new names.
2. Change every `v=` value in `index.html` to today's date, so browsers fetch the new files instead of the cached ones. Commit `c76ae75` added the version query for the refreshed screenshots.
3. If you add or rename a frame, update the gallery list in `index.html` and the image entries in `sitemap.xml`. The sitemap does not carry the version query.
4. Update `<lastmod>` in `sitemap.xml` when the page content changes.

### Gallery behaviour

The gallery is a list of frames with `data-id` attributes. On screens 960 px and wider, the selector swaps the featured frame. On narrow screens and without JavaScript, the frames stack. Selection uses `aria-selected`, and the swap respects `prefers-reduced-motion`.

## SEO and performance

- `robots.txt` allows crawling and points to `https://civora.sk/sitemap.xml`.
- The commit `09fcdc2` tuned the page for a Lighthouse score of 100. Run Lighthouse again after changes to images, fonts or the inline CSS and JavaScript.

## Content notes

- The public price list was replaced by a pilot-programme section in commit `0cf7b80`. Pricing documents are in the private platform repository.
- Contact links are in `index.html`: a `mailto:` link for the demo request and a contact block in the final section. Update them there.

## Contributing

1. Create a branch from `main`.
2. Make the change and check it in a local browser at phone and desktop widths.
3. Open a pull request into `main`. Merging publishes the site.

Use Conventional Commits for messages, as in the other Civora repositories.
