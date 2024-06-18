"""Default: create wheel."""
import glob
from doit.tools import create_folder


DOIT_CONFIG = {'default_tasks': ['check', 'html', 'wheel']}
PO_DEST = 'AlarmCallBot/po'


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
        'actions': ['git clean -xdf']
    }


def task_html():
    """Make HTML documentation via sphinx."""
    return {
        'actions': ['sphinx-build -M html docs build']
    }


def task_test():
    """Perform testing."""
    yield {
        'actions': ['coverage run -m unittest -v'],
        'verbosity': 2,
        'name': 'run'
    }
    yield {
        'actions': ['coverage report'],
        'verbosity': 2,
        'name': 'report'
    }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
        'actions': ['pydocstyle AlarmCallBot']
    }


def task_codestyle():
    """Check codestyle against flake8."""
    return {
        'actions': ['flake8 AlarmCallBot']
    }


def task_check():
    """Perform all checks."""
    return {
        'actions': None,
        'task_dep': ['codestyle', 'docstyle', 'test']
    }


def task_pot():
    """Re-create .pot."""
    return {
        'actions': ['pybabel extract -o bot.pot AlarmCallBot/bot'],
        'file_dep': glob.glob('AlarmCallBot/*.py'),
        'targets': ['bot.pot'],
    }


def task_po():
    """Update translations."""
    return {
        'actions': ['pybabel update --ignore-pot-creation-date -D bot -d po -i bot.pot'],
        'file_dep': ['bot.pot'],
        'targets': ['po/ru_RU.UTF-8/LC_MESSAGES/bot.po'],
    }


def task_mo():
    """Compile translations."""
    return {
        'actions': [
            (create_folder, [f'{PO_DEST}/ru_RU.UTF-8/LC_MESSAGES']),
            f'pybabel compile -D bot -l ru_RU.UTF-8 -d {PO_DEST} -i po/ru_RU.UTF-8/LC_MESSAGES/bot.po'
        ],
        'file_dep': ['po/ru_RU.UTF-8/LC_MESSAGES/bot.po'],
        'targets': [f'{PO_DEST}/ru_RU.UTF-8/LC_MESSAGES/bot.mo'],
    }
