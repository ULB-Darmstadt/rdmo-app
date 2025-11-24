import sys

from django.utils.translation import gettext_lazy as _

# Example: mount a sibling repo / a tests app somewhere nearby
EXTRA_APPS_DIR = BASE_DIR / ".." / "rdmo" / "testing" / "plugins"   # adjust
if EXTRA_APPS_DIR.exists():
    sys.path.insert(0, str(EXTRA_APPS_DIR.parent))  # make parent importable

# INSTALLED_APPS += [
#     'plugins',
# ]
PLUGINS = [
    # rdmo plugins
    'rdmo.projects.exports.RDMOXMLExport',
    'rdmo.projects.exports.CSVCommaExport',
    'rdmo.projects.exports.CSVSemicolonExport',
    'rdmo.projects.exports.JSONExport',
    'rdmo.projects.imports.RDMOXMLImport',
    # rdmo/testing plugins
    'plugins.optionset_providers.providers.SimpleProvider',
    'plugins.project_issue_providers.providers.SimpleIssueProvider',
    'plugins.project_export.exports.SimpleExportPlugin',
    'plugins.project_snapshot_export.exports.SimpleSnapshotExportPlugin',
    'plugins.project_import.imports.SimpleImportPlugin',
    # 3rd_part plugins
    "MaRDMO.main.MaRDMOExportProvider",
    "rdmo_sensorsearch.providers.SensorsProvider",
]

if not 'plugins' in INSTALLED_APPS and EXTRA_APPS_DIR.exists():
    # PROJECT_SNAPSHOT_EXPORTS = [
    #     ('xml', _('RDMO XML'), 'plugins.project_snapshot_export.exports.SimpleSnapshotExportPlugin'),
    # ]

    OPTIONSET_PROVIDERS = [
        ('simple', _('Simple provider'), 'rdmo.options.providers.SimpleProvider')
    ]

    PROJECT_ISSUE_PROVIDERS = [
        ('simple', _('Simple provider'), 'rdmo.projects.providers.SimpleIssueProvider')
    ]

    # PROJECT_IMPORTS = [
    #     ('url', _('from URL'), 'plugins.project_import.imports.SimpleImportPlugin'),
    # ]

    PROJECT_EXPORTS = [
        ('xml', _('as RDMO XML'), 'rdmo.projects.exports.RDMOXMLExport'),
        ('csvcomma', _('as CSV (comma separated)'), 'rdmo.projects.exports.CSVCommaExport'),
        ('csvsemicolon', _('as CSV (semicolon separated)'), 'rdmo.projects.exports.CSVSemicolonExport'),
    ]
