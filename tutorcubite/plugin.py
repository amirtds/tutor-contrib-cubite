"""Tutor plugin: apply the Cubite brand to Open edX (Ulmo+).

Responsibilities:
  - Wire the @cubite/brand-openedx npm package into every MFE build
  - Inject "Powered by Cubite" into the global MFE footer via
    frontend-plugin-framework
  - Set platform name / site name / logo URLs across LMS + Studio + MFEs
  - Override the legacy LMS footer for non-MFE pages
"""

from __future__ import annotations

import os
from glob import glob

from tutor import hooks

HERE = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# Config defaults — overridable in `config.yml` with `tutor config save --set`
# -----------------------------------------------------------------------------
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("CUBITE_VERSION", "1.0.0"),
        # npm spec for the brand package. Public npm by default; switch to a
        # git URL or local tarball for development.
        ("CUBITE_BRAND_PACKAGE_SPEC", "@cubite/brand-openedx@^1.0.0"),
        # The npm alias name the MFEs import. Do not change unless you know
        # what you are doing — Paragon expects `@openedx/brand`.
        ("CUBITE_BRAND_ALIAS", "@openedx/brand"),
        # Branding text + link target for the "Powered by" line.
        ("CUBITE_POWERED_BY_URL", "https://cubite.io"),
        ("CUBITE_POWERED_BY_TEXT", "Powered by Cubite"),
        # Platform-level naming.
        ("CUBITE_PLATFORM_NAME", "Cubite"),
        ("CUBITE_PLATFORM_DESCRIPTION", "Learning platform powered by Cubite"),
        ("CUBITE_SUPPORT_EMAIL", "support@cubite.io"),
        ("CUBITE_CONTACT_EMAIL", "hello@cubite.io"),
        # Static asset paths served by the LMS (relative to LMS_HOST).
        ("CUBITE_LOGO_PATH", "/static/cubite/logo.svg"),
        ("CUBITE_LOGO_WHITE_PATH", "/static/cubite/logo-white.svg"),
        ("CUBITE_LOGO_TRADEMARK_PATH", "/static/cubite/logo-trademark.svg"),
        ("CUBITE_FAVICON_PATH", "/static/cubite/favicon.ico"),
    ]
)

# -----------------------------------------------------------------------------
# Patches — each file in patches/ is registered under its filename.
# Tutor injects patch contents at named patch points throughout its templates.
# -----------------------------------------------------------------------------
for patch_path in sorted(glob(os.path.join(HERE, "patches", "*"))):
    with open(patch_path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(patch_path), patch_file.read())
        )

# -----------------------------------------------------------------------------
# Templates — rendered into Tutor's env on `tutor config save`.
# templates/cubite/build/   → image build contexts
# templates/cubite/apps/    → mounted runtime config
# -----------------------------------------------------------------------------
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(os.path.join(HERE, "templates"))
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        # Contribute files into env/build/ — specifically the openedx image
        # build context at env/build/openedx/cubite-brand/.
        ("cubite/build", "build"),
        # Plugin-private app templates rendered under env/plugins/cubite/.
        ("cubite/apps", "plugins"),
    ]
)
