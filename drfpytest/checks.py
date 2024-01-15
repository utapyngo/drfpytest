# pragma: no cover
"""Custom django checks.

qa.W001: Missing migration.
"""
import os

import django.apps
from django.apps import apps
from django.core.checks import register
from django.core.checks import Tags
from django.core.management import CommandError
from django.test import override_settings

nomigrations = None


def check_migrations(app_configs):
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.loader import MigrationLoader
    from django.db.migrations.questioner import MigrationQuestioner
    from django.db.migrations.state import ProjectState
    from django.db.migrations.writer import MigrationWriter

    app_labels = {app.label for app in app_configs}
    loader = MigrationLoader(connection=None, ignore_no_migrations=True)
    conflicts = {
        app_label: conflict
        for app_label, conflict in loader.detect_conflicts().items()
        if app_label in app_labels
    }
    if conflicts:
        name_str = '; '.join(
            '{} in {}'.format(', '.join(names), app) for app, names in conflicts.items()
        )
        raise CommandError(
            f'Conflicting migrations detected; '
            f'multiple leaf nodes in the migration graph: ({name_str}).'
        )
    questioner = MigrationQuestioner(specified_apps=app_labels, dry_run=True)
    current_state = ProjectState.from_apps(apps)
    autodetector = MigrationAutodetector(loader.project_state(), current_state, questioner)

    with override_settings(LANGUAGE_CODE='en'):
        changes = autodetector.changes(
            graph=loader.graph, trim_to_apps=app_labels, convert_apps=app_labels
        )

    def get_migration_strings(migrations):
        for migration in migrations:
            writer = MigrationWriter(migration)
            try:
                migration_string = os.path.relpath(writer.path)
            except ValueError:
                migration_string = writer.path
            if migration_string.startswith('..'):
                migration_string = writer.path
            yield '  ' + migration_string
            for operation in migration.operations:
                yield '    - ' + operation.describe()

    if changes:
        for app_label, app_migrations in changes.items():
            yield django.core.checks.Warning(
                f'The following migrations in the "{app_label}" app are missing: \n'
                + '\n'.join(get_migration_strings(app_migrations)),
                id='qa.W001',
            )


@register(Tags.models)
def check_models(app_configs, **kwargs):
    if not app_configs:
        app_configs = [
            c for c in django.apps.apps.get_app_configs() if 'site-packages' not in c.path
        ]
    if not nomigrations:
        yield from check_migrations(app_configs)
