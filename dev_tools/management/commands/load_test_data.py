import importlib
import json
import logging
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from rdmo.core.xml import parse_xml_to_elements
from rdmo.management.imports import import_elements

logger = logging.getLogger(__name__)

RDMO_VERSION = importlib.metadata.version("rdmo")
RDMO_MEDIA_ROOT = settings.BASE_DIR.parent / 'rdmo' / 'testing' / "media"
RDMO_CATALOG_DIR = settings.BASE_DIR.parent / 'rdmo-content' / 'rdmo-catalog'

class Command(BaseCommand):
    help = "Load test data from fixture directories and set permissions."

    def add_arguments(self, parser):
        parser.add_argument(
            '--fixtures',
            action='store_true',
            help='Load test fixtures into the database.'
        )
        parser.add_argument(
            '--files',
            action='store_true',
            help='Copy test media files to MEDIA_ROOT.'
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Load JSON data from catalogs.json.'
        )
        parser.add_argument(
            '--rdmo-catalog',
            action='store_true',
            help='Load all content from rdmo-catalog'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(f"Starting with RDMO({RDMO_VERSION})."))
        self.stdout.write(self.style.NOTICE(f"Fixture dirs: {', '.join(map(str,settings.FIXTURE_DIRS))}."))
        if options['fixtures']:
            self.load_fixtures()
        if options['files']:
            self.copy_files()
        if options['json']:
            self.load_json_data()
        if options['rdmo_catalog']:
            self.load_content_from_rdmo_catalog()

    def load_fixtures(self):
        """Load database fixtures from the fixture directories."""
        fixture_order = [
            "sites",
            "groups",
            "users",
            "accounts",
            "domain",
            "conditions",
            "options",
            "questions",
            "tasks",
            "views",
            "overlays",
            "projects",
            "config",
        ]

        fixture_files = []

        for fixture_dir in settings.FIXTURE_DIRS:
            fixture_dir = Path(fixture_dir)

            for stem in fixture_order:
                fixture_files.extend(sorted(fixture_dir.glob(f"{stem}.json")))

        if not fixture_files:
            raise CommandError("No fixture files found.")

        self.stdout.write(self.style.WARNING("Loading fixtures:"))
        for fixture in fixture_files:
            self.stdout.write(f"  {fixture}")

        call_command("loaddata", *map(str, fixture_files), verbosity=2)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully loaded test fixtures from: {}".format(
                    ", ".join(map(str, fixture_files))
                )
            )
        )

    def copy_files(self):
        """Copy test media files to MEDIA_ROOT."""
        target_path = Path(settings.MEDIA_ROOT)

        if RDMO_MEDIA_ROOT.exists():
            try:
                shutil.copytree(RDMO_MEDIA_ROOT, target_path, dirs_exist_ok=True)
                self.stdout.write(self.style.SUCCESS("Successfully copied test media files."))
            except Exception as e:
                logger.error("Error copying media files: %s", str(e))
                raise CommandError("Failed to copy media files.") from e
        else:
            self.stdout.write(self.style.WARNING(f"Media path does not exist: {RDMO_MEDIA_ROOT}"))

    def load_json_data(self):
        """Load JSON data from catalogs.json."""
        for fixture_dir in settings.FIXTURE_DIRS:
            json_file = Path(fixture_dir).parent / 'import' / 'catalogs.json'
            if json_file.exists():
                try:
                    data = {'elements': json.loads(json_file.read_text())}
                    self.stdout.write(self.style.SUCCESS(f"Successfully loaded JSON data from: {json_file}"))
                    return data
                except json.JSONDecodeError as e:
                    logger.error("Error parsing JSON data: %s", str(e))
                    raise CommandError("Failed to load JSON data.") from e
            else:
                self.stdout.write(self.style.WARNING(f"JSON file not found: {json_file}"))

    def load_content_from_rdmo_catalog(self):
        """Import all XML contents from the rdmo-catalog repository using internal RDMO functions."""

        if not RDMO_CATALOG_DIR.exists():
            self.stdout.write(self.style.WARNING(f"RDMO_CATALOG does not exist at {RDMO_CATALOG_DIR}"))
            return

        self.stdout.write(f"Importing RDMO catalog from {RDMO_CATALOG_DIR}")

        try:
            # Import fixed XML files
            for relative_path in [
                'rdmorganiser/domain/attributes.xml',
                'rdmorganiser/conditions/conditions.xml',
                'rdmorganiser/options/optionsets.xml',
                'rdmorganiser/conditions/conditions.xml'  # yes, duplicated in original
            ]:
                self._import_xml_file(RDMO_CATALOG_DIR / relative_path)

            # Import from directories
            self._import_xml_from_directory(RDMO_CATALOG_DIR, 'rdmorganiser/questions')
            self._import_xml_file(RDMO_CATALOG_DIR / 'rdmorganiser/tasks/tasks.xml')
            self._import_xml_from_directory(RDMO_CATALOG_DIR, 'rdmorganiser/views')

            self.stdout.write(self.style.SUCCESS("Successfully imported RDMO catalog."))
        except CommandError as e:
            logger.error("Import failed: %s", str(e))
            raise CommandError("Failed to load RDMO catalog.") from e

    def _import_xml_file(self, xml_path: Path):
        """Helper to import a single XML file with error handling."""
        if not xml_path.exists():
            self.stdout.write(self.style.WARNING(f"File does not exist: {xml_path}"))
            return

        try:
            elements, errors = parse_xml_to_elements(xml_file=xml_path)
            if errors:
                raise CommandError(" ".join(map(str, errors)))
            import_elements(elements)
            self.stdout.write(self.style.SUCCESS(f"Imported: {xml_path}"))
        except Exception as e:
            logger.error("Failed to import %s: %s", xml_path, str(e))
            raise

    def _import_xml_from_directory(self, base_path: Path, sub_dir: str):
        """Helper to import all XML files in a given subdirectory."""
        directory = base_path / sub_dir
        if not directory.exists():
            self.stdout.write(self.style.WARNING(f"Directory does not exist: {directory}"))
            return

        for xml_file in directory.rglob('*.xml'):
            self._import_xml_file(xml_file)
