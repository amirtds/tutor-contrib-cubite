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

# MFEs we do NOT ship in the Cubite distribution. Dropping them cuts MFE
# build time roughly in half and keeps small VMs (4GB RAM) from OOM-killing
# the parallel npm installs that buildx kicks off per MFE. These four are
# admin/instructor tools or rarely-used flows; the core learner + author
# experience is fully covered by the remaining 7 MFEs.
CUBITE_DROPPED_MFES = (
    "admin-console",
    "communications",
    "gradebook",
    "ora-grading",
)

try:
    from tutormfe.hooks import MFE_APPS, PLUGIN_SLOTS

    @MFE_APPS.add()
    def _cubite_trim_mfes(apps):
        for name in CUBITE_DROPPED_MFES:
            apps.pop(name, None)
        return apps

    # Register the Powered by Cubite footer widget into every MFE's
    # footer_slot. The third element of each tuple is the *JSX expression*
    # that becomes a single entry in the `plugins: []` array for that slot
    # — tutor-mfe inlines it inside the env.config.jsx template inside the
    # try{} block where DIRECT_PLUGIN is available via dynamic import.
    _POWERED_BY_PLUGIN_JSX = """{
        op: PLUGIN_OPERATIONS.Insert,
        widget: {
          id: 'cubite-powered-by',
          type: DIRECT_PLUGIN,
          priority: 60,
          RenderWidget: PoweredByCubite,
        },
      }"""
    PLUGIN_SLOTS.add_item(("all", "footer_slot", _POWERED_BY_PLUGIN_JSX))

except ImportError:
    # tutor-mfe is not installed — skip silently. The brand patches that
    # apply only to MFE Dockerfiles will be inert in that case.
    pass

# -----------------------------------------------------------------------------
# Config defaults — overridable in `config.yml` with `tutor config save --set`
# -----------------------------------------------------------------------------
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("CUBITE_VERSION", "1.0.0"),
        # npm-installable spec for the brand package. Accepts any form npm
        # understands: `name@version`, `github:owner/repo#ref`, a tarball URL,
        # or a local file path.
        ("CUBITE_BRAND_PACKAGE_SPEC", "github:amirtds/brand-openedx-cubite#master"),
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
        # Browser-facing URL paths (start with /static/, served by the LMS).
        # Used in LOGO_URL, MFE_CONFIG[*_URL], etc.
        ("CUBITE_LOGO_PATH", "/static/cubite/logo.svg"),
        ("CUBITE_LOGO_WHITE_PATH", "/static/cubite/logo-white.svg"),
        ("CUBITE_LOGO_TRADEMARK_PATH", "/static/cubite/logo-trademark.svg"),
        ("CUBITE_FAVICON_PATH", "/static/cubite/favicon.ico"),
        # staticfiles-relative names. Django's FAVICON_PATH setting is passed
        # to staticfiles_storage.url() which requires a path relative to
        # STATIC_ROOT — an absolute URL would trigger SuspiciousFileOperation.
        ("CUBITE_FAVICON_STATICFILES", "cubite/favicon.ico"),
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
        # Brand assets land in the openedx image build context so the
        # `openedx-dockerfile-pre-assets` patch can COPY them in.
        # The template prefix is NOT stripped — files at
        # templates/cubite-brand/X are written to env/{dst}/cubite-brand/X.
        # So dst=build/openedx puts assets at env/build/openedx/cubite-brand/.
        ("cubite-brand", "build/openedx"),
    ]
)
