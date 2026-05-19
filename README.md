# tutor-contrib-cubite

Tutor plugin that applies the **Cubite** brand to an Open edX deployment
(Ulmo and later). It:

- Wires [`@cubite/brand-openedx`](https://www.npmjs.com/package/@cubite/brand-openedx)
  into every MFE build (replaces the default `@openedx/brand` package).
- Injects a **Powered by Cubite** link into the global MFE footer via the
  `footer_slot` plugin slot from `frontend-plugin-framework`.
- Sets `PLATFORM_NAME`, support/contact emails, and logo / favicon URLs across
  LMS, Studio, and MFE runtime config.
- Copies brand SVGs + favicons into the LMS image so they are served at
  `/static/cubite/...`.

## Install

```bash
pip install git+https://github.com/cubite/tutor-contrib-cubite
tutor plugins enable cubite
tutor config save
tutor images build openedx mfe
tutor local launch
```

## Configuration

All settings have sensible defaults — override only what you need:

```bash
tutor config save \
  --set CUBITE_PLATFORM_NAME="Acme Academy" \
  --set CUBITE_SUPPORT_EMAIL="support@acme.example" \
  --set CUBITE_POWERED_BY_URL="https://cubite.io"
```

| Key                            | Default                                       |
|--------------------------------|-----------------------------------------------|
| `CUBITE_BRAND_PACKAGE_SPEC`    | `@cubite/brand-openedx@^1.0.0`                |
| `CUBITE_BRAND_ALIAS`           | `@openedx/brand`                              |
| `CUBITE_POWERED_BY_URL`        | `https://cubite.io`                           |
| `CUBITE_POWERED_BY_TEXT`       | `Powered by Cubite`                           |
| `CUBITE_PLATFORM_NAME`         | `Cubite`                                      |
| `CUBITE_PLATFORM_DESCRIPTION`  | `Learning platform powered by Cubite`         |
| `CUBITE_SUPPORT_EMAIL`         | `support@cubite.io`                           |
| `CUBITE_CONTACT_EMAIL`         | `hello@cubite.io`                             |
| `CUBITE_LOGO_PATH`             | `/static/cubite/logo.svg`                     |
| `CUBITE_LOGO_TRADEMARK_PATH`   | `/static/cubite/logo-trademark.svg`           |
| `CUBITE_LOGO_WHITE_PATH`       | `/static/cubite/logo-white.svg`               |
| `CUBITE_FAVICON_PATH`          | `/static/cubite/favicon.ico`                  |

## What changes after install?

- **MFE footer**: a "Powered by Cubite" link appears below the standard
  footer content on every MFE that renders the `footer_slot`.
- **Logos**: every MFE that reads `LOGO_URL` from MFE runtime config gets
  the Cubite mark.
- **Studio**: header logo + favicon updated.
- **Legacy LMS pages** (login fallback, certificates, transactional emails):
  logo + platform name updated via Django settings.

## License

Apache-2.0
