DARE Learning
=============

DARE Learning is a Zimbabwe-focused customization of the open-source Kolibri
learning platform. Kolibri remains the application foundation; this work does
not replace its learner, teacher, content-management, synchronization, or
offline capabilities. The current branding is a first step, not a claim that
curriculum content, offline AI, or institutional subscriptions are already
available.

Branding
--------

The customization uses Kolibri's existing ``ThemeHook`` mechanism rather than
changing shared frontend components. The DARE values are configured in
``kolibri/plugins/default_theme/kolibri_plugin.py`` and the logo is in
``kolibri/plugins/default_theme/static/assets/dare_learning/``. The theme sets
the product name, a deep-purple and gold palette, and the tagline
“African knowledge. African learning.” The PWA manifest and browser title use
the themed product name. The DARE logo is currently an SVG; additional raster
icons may be supplied later if required by target platforms.

The theme's existing background photograph and its Lewa Wildlife Conservancy
credit are retained. Kolibri's footer attribution, Learning Equality
copyright, third-party attributions, privacy disclosures, and the MIT license
are also retained. Product branding does not replace those notices.

Architecture and extension boundaries
-------------------------------------

The repository contains a Django/Python backend in ``kolibri/``, Vue frontend
plugins in ``kolibri/plugins/``, shared JavaScript packages in ``packages/``,
and platform/build code in ``platforms/`` and ``build_tools/``. Kolibri's plugin
and hook system is the preferred boundary for optional user-facing features.
The upstream plugin guide is ``docs/backend_architecture/plugins.rst``.

Kolibri's API documentation notes that most APIs are internal and unstable;
only endpoints under ``/public/`` are maintained for backwards compatibility
(``docs/getting_started.rst``). External DARE services should therefore use
documented public endpoints or a separately versioned adapter, not depend on
incidental internal viewsets.

Offline learning
----------------

Kolibri already supports local content access and search, content import and
export, learner and teacher workflows, and synchronization/discovery between
devices on a local network. Relevant implementation areas include
``kolibri/core/content/``, ``kolibri/core/discovery/``, and the Learn and Coach
plugins. Search metadata is derived from existing labels such as grade levels,
categories, learning activities, accessibility labels, learner needs, and
languages. These functions are part of the existing product and must remain
usable without an internet connection.

Content can be imported through Kolibri's established channel/content
workflows. A school-local server can host imported materials and serve
connected devices; an internet connection is not a runtime requirement for
content already available locally. Validate this behavior on the target
hardware and network before deployment; no deployment or new offline behavior
is claimed by this customization.

Curriculum metadata strategy
----------------------------

Kolibri content metadata includes fields such as ``grade_levels`` and
``categories`` (see ``kolibri/core/content/base_models.py``), and its search
code filters supported metadata labels (see
``kolibri/core/content/utils/search.py``). These are useful existing
classification points, but they do not by themselves define an official
Zimbabwean syllabus or guarantee that arbitrary curriculum metadata survives
every import/export schema version.

An initial DARE catalogue can organize resources by Form 1–6, subject, and
topic using content-channel organization and supported metadata where it fits.
Candidate subjects include Mathematics, Biology, Chemistry, Physics, Geography,
History, Agriculture, English, and Computer Science. These names are
organizational suggestions only, not verified syllabus content. No material
should be labelled ZIMSEC-approved or treated as an examination paper without
independent verification and rights review.

Before storing additional curriculum identifiers, topic codes, or curriculum
versions, verify that the chosen representation is preserved by the content
schema, channel import/export, sync, and search paths. Keep curriculum-specific
mapping in content/catalogue metadata or an optional plugin; do not add
Zimbabwe-only assumptions to unrelated Kolibri core components. Cambridge and
other African curricula should be represented as separate, versioned mappings
so they can coexist without a core rewrite.

Proposed offline AI tutor integration
-------------------------------------

No AI tutor, local model, retrieval service, or AI citation workflow is
implemented. A future DARE tutor should be an optional plugin or local service
integration, not a permanent internet dependency:

* Index only approved local resources and return references to the actual
  content nodes and passages used.
* Retrieve evidence first; only generate an explanation when a configured
  local model is available. If evidence or the model is unavailable, report
  that limitation rather than inventing an answer.
* Use Kolibri's resource/API integration patterns and backend permission
  checks. Keep the local model and its resource requirements optional so
  existing school servers continue to work without them.
* Test citations, insufficient-evidence responses, access control, resource
  limits, and operation with networking disabled before claiming offline AI
  support.

This proposal does not select a model, add a model dependency, or claim that
offline AI is available.

Proposed institutional subscription integration
------------------------------------------------

No billing, payment credential storage, subscription enforcement, or
institutional entitlement system is implemented. DARE Institutional Cloud
should remain the authority for school subscriptions and billing; Kolibri
should retain its existing facility, user, role, and local authentication
workflows.

Before implementation, define a versioned server-to-server contract for
institution identity and entitlements, its authentication and revocation
rules, and behavior during prolonged offline periods. Enforce access on the
trusted server side; a client-only check is not authorization. A Kolibri
plugin or external adapter can translate verified entitlement state into
product capabilities while remaining decoupled from payment processing.
Never store payment credentials in Kolibri. Review available OIDC integration
and the deployment's user-management requirements separately; do not assume
that an OIDC provider alone implements institutional subscriptions.

Development and checks
----------------------

Follow ``docs/getting_started.rst`` for the full upstream prerequisites. The
repository's agent setup and root scripts use the following development
sequence:

.. code-block:: bash

   uv sync --group dev --all-packages
   pnpm install
   export KOLIBRI_RUN_MODE=dev
   kolibri configure setup
   pnpm devserver

Useful focused checks include:

.. code-block:: bash

   uv run pytest kolibri/core/test/test_theme.py
   uv run pytest kolibri/core/content/test/test_search.py
   uv run pytest kolibri/core/content/test/test_channel_import.py
   pnpm test-jest packages/kolibri/styles/internal/__tests__/initializeTheme.spec.js
   prek run --files kolibri/core/test/test_theme.py kolibri/core/templatetags/core_tags.py kolibri/plugins/default_theme/kolibri_plugin.py packages/kolibri/styles/internal/__tests__/initializeTheme.spec.js
   pnpm run build

Run checks in the project's documented environment. Passing unit tests do not
replace an end-to-end check on representative low-memory hardware with the
network disconnected.

Upstream updates and changed files
----------------------------------

Keep DARE customizations small and isolated to the theme, its assets, and
DARE-specific documentation. Before updating, compare the branch with the
Learning Equality Kolibri development branch, merge upstream changes (rather
than rebasing shared work), and resolve any overlap in the customized theme
or favicon behavior. Re-run the focused tests and review upstream license and
attribution changes. Do not deploy directly from an upstream merge.

The DARE-specific work is in:

* ``README.md`` and ``docs/dare_learning.rst``: identify this customization and
  document its setup, boundaries, proposals, and limitations.
* ``kolibri/plugins/default_theme/kolibri_plugin.py`` and
  ``kolibri/plugins/default_theme/static/assets/dare_learning/dare-learning.svg``:
  apply the DARE product name, palette, logo, and tagline through the existing
  theme mechanism.
* ``kolibri/core/templatetags/core_tags.py`` and
  ``kolibri/core/test/test_theme.py``: allow a theme SVG to supply the favicon
  when no ICO is configured, while retaining the existing ICO priority and
  default fallback.
* ``packages/kolibri/styles/internal/__tests__/initializeTheme.spec.js``:
  keep the frontend theme fixture aligned with the configured DARE theme.

No production deployment, payment system, AI provider, curriculum content, or
database migration is included.
