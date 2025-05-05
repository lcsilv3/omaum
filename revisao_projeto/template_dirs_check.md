# Verificação de Diretórios de Templates

## Configurações de Templates no settings.py



### Arquivo: omaum\settings.py

python
# Importações e configurações existentes
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicações do projeto
    'core',
    'alunos',
    'atividades',
    'cargos',
    'cursos',
    'frequencias',
    'iniciacoes',
    'matriculas',
    'notas',
    'pagamentos',
    'presencas',
    'punicoes',
    'relatorios',
    'turmas',
    # Third party apps
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Verifique por middlewares personalizados aqui
]

ROOT_URLCONF = 'omaum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'omaum', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'omaum.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# Configurações de autenticação
LOGIN_URL = '/entrar/'
# Adicionar estas linhas para resolver o problema de redirecionamento
LOGIN_REDIRECT_URL = '/'  # Redireciona para a página inicial após o login
LOGOUT_REDIRECT_URL = '/'  # Redireciona para a página inicial após o logout




### Arquivo: venv\Lib\site-packages\debug_toolbar\settings.py

python
import sys
import warnings
from functools import cache

from django.conf import settings
from django.dispatch import receiver
from django.test.signals import setting_changed

CONFIG_DEFAULTS = {
    # Toolbar options
    "DISABLE_PANELS": {
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    },
    "INSERT_BEFORE": "</body>",
    "RENDER_PANELS": None,
    "RESULTS_CACHE_SIZE": 25,
    "ROOT_TAG_EXTRA_ATTRS": "",
    "SHOW_COLLAPSED": False,
    "SHOW_TOOLBAR_CALLBACK": "debug_toolbar.middleware.show_toolbar",
    # Panel options
    "EXTRA_SIGNALS": [],
    "ENABLE_STACKTRACES": True,
    "ENABLE_STACKTRACES_LOCALS": False,
    "HIDE_IN_STACKTRACES": (
        "socketserver",
        "threading",
        "wsgiref",
        "debug_toolbar",
        "django.db",
        "django.core.handlers",
        "django.core.servers",
        "django.utils.decorators",
        "django.utils.deprecation",
        "django.utils.functional",
    ),
    "PRETTIFY_SQL": True,
    "PROFILER_CAPTURE_PROJECT_CODE": True,
    "PROFILER_MAX_DEPTH": 10,
    "PROFILER_THRESHOLD_RATIO": 8,
    "SHOW_TEMPLATE_CONTEXT": True,
    "SKIP_TEMPLATE_PREFIXES": ("django/forms/widgets/", "admin/widgets/"),
    "SQL_WARNING_THRESHOLD": 500,  # milliseconds
    "OBSERVE_REQUEST_CALLBACK": "debug_toolbar.toolbar.observe_request",
    "TOOLBAR_LANGUAGE": None,
    "IS_RUNNING_TESTS": "test" in sys.argv,
    "UPDATE_ON_FETCH": False,
    "DEFAULT_THEME": "auto",
}


@cache
def get_config():
    USER_CONFIG = getattr(settings, "DEBUG_TOOLBAR_CONFIG", {})
    CONFIG = CONFIG_DEFAULTS.copy()
    CONFIG.update(USER_CONFIG)
    return CONFIG


PANELS_DEFAULTS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.alerts.AlertsPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


@cache
def get_panels():
    try:
        PANELS = list(settings.DEBUG_TOOLBAR_PANELS)
    except AttributeError:
        PANELS = PANELS_DEFAULTS

    logging_panel = "debug_toolbar.panels.logging.LoggingPanel"
    if logging_panel in PANELS:
        PANELS = [panel for panel in PANELS if panel != logging_panel]
        warnings.warn(
            f"Please remove {logging_panel} from your DEBUG_TOOLBAR_PANELS setting.",
            DeprecationWarning,
            stacklevel=1,
        )
    return PANELS


@receiver(setting_changed)
def update_toolbar_config(*, setting, **kwargs):
    """
    Refresh configuration when overriding settings.
    """
    if setting == "DEBUG_TOOLBAR_CONFIG":
        get_config.cache_clear()
    elif setting == "DEBUG_TOOLBAR_PANELS":
        from debug_toolbar.toolbar import DebugToolbar

        get_panels.cache_clear()
        DebugToolbar._panel_classes = None
        # Not implemented: invalidate debug_toolbar.urls.




### Arquivo: venv\Lib\site-packages\debug_toolbar\panels\settings.py

python
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.debug import get_default_exception_reporter_filter

from debug_toolbar.panels import Panel

get_safe_settings = get_default_exception_reporter_filter().get_safe_settings


class SettingsPanel(Panel):
    """
    A panel to display all variables in django.conf.settings
    """

    template = "debug_toolbar/panels/settings.html"

    is_async = True

    nav_title = _("Settings")

    def title(self):
        return _("Settings from %s") % settings.SETTINGS_MODULE

    def generate_stats(self, request, response):
        self.record_stats({"settings": dict(sorted(get_safe_settings().items()))})




### Arquivo: venv\Lib\site-packages\dill\settings.py

python
#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2008-2016 California Institute of Technology.
# Copyright (c) 2016-2024 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/dill/blob/master/LICENSE
"""
global settings for Pickler
"""

from pickle import DEFAULT_PROTOCOL

settings = {
   #'main' : None,
    'protocol' : DEFAULT_PROTOCOL,
    'byref' : False,
   #'strictio' : False,
    'fmode' : 0, #HANDLE_FMODE
    'recurse' : False,
    'ignore' : False,
}

del DEFAULT_PROTOCOL





### Arquivo: venv\Lib\site-packages\django_extensions\settings.py

python
# -*- coding: utf-8 -*-
import os

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
REPLACEMENTS = getattr(settings, 'EXTENSIONS_REPLACEMENTS', {})

DEFAULT_SQLITE_ENGINES = (
    'django.db.backends.sqlite3',
    'django.db.backends.spatialite',
)
DEFAULT_MYSQL_ENGINES = (
    'django.db.backends.mysql',
    'django.contrib.gis.db.backends.mysql',
    'mysql.connector.django',
)
DEFAULT_POSTGRESQL_ENGINES = (
    'django.db.backends.postgresql',
    'django.db.backends.postgresql_psycopg2',
    'django.db.backends.postgis',
    'django.contrib.gis.db.backends.postgis',
    'psqlextra.backend',
    'django_zero_downtime_migrations.backends.postgres',
    'django_zero_downtime_migrations.backends.postgis',
)

SQLITE_ENGINES = getattr(settings, 'DJANGO_EXTENSIONS_RESET_DB_SQLITE_ENGINES', DEFAULT_SQLITE_ENGINES)
MYSQL_ENGINES = getattr(settings, 'DJANGO_EXTENSIONS_RESET_DB_MYSQL_ENGINES', DEFAULT_MYSQL_ENGINES)
POSTGRESQL_ENGINES = getattr(settings, 'DJANGO_EXTENSIONS_RESET_DB_POSTGRESQL_ENGINES', DEFAULT_POSTGRESQL_ENGINES)

DEFAULT_PRINT_SQL_TRUNCATE_CHARS = 1000




### Arquivo: venv\Lib\site-packages\isort\settings.py

python
"""isort/settings.py.

Defines how the default settings for isort should be loaded
"""

import configparser
import fnmatch
import os
import posixpath
import re
import stat
import subprocess  # nosec: Needed for gitignore support.
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Optional,
    Pattern,
    Set,
    Tuple,
    Type,
    Union,
)
from warnings import warn

from . import sorting, stdlibs
from .exceptions import (
    FormattingPluginDoesNotExist,
    InvalidSettingsPath,
    ProfileDoesNotExist,
    SortingFunctionDoesNotExist,
    UnsupportedSettings,
)
from .profiles import profiles as profiles
from .sections import DEFAULT as SECTION_DEFAULTS
from .sections import FIRSTPARTY, FUTURE, LOCALFOLDER, STDLIB, THIRDPARTY
from .utils import Trie
from .wrap_modes import WrapModes
from .wrap_modes import from_string as wrap_mode_from_string

if TYPE_CHECKING:
    tomllib: Any
else:
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        from ._vendored import tomli as tomllib

_SHEBANG_RE = re.compile(rb"^#!.*\bpython[23w]?\b")
CYTHON_EXTENSIONS = frozenset({"pyx", "pxd"})
SUPPORTED_EXTENSIONS = frozenset({"py", "pyi", *CYTHON_EXTENSIONS})
BLOCKED_EXTENSIONS = frozenset({"pex"})
FILE_SKIP_COMMENTS: Tuple[str, ...] = (
    "isort:" + "skip_file",
    "isort: " + "skip_file",
)  # Concatenated to avoid this file being skipped
MAX_CONFIG_SEARCH_DEPTH: int = 25  # The number of parent directories to for a config file within
STOP_CONFIG_SEARCH_ON_DIRS: Tuple[str, ...] = (".git", ".hg")
VALID_PY_TARGETS: Tuple[str, ...] = tuple(
    target.replace("py", "") for target in dir(stdlibs) if not target.startswith("_")
)
CONFIG_SOURCES: Tuple[str, ...] = (
    ".isort.cfg",
    "pyproject.toml",
    "setup.cfg",
    "tox.ini",
    ".editorconfig",
)
DEFAULT_SKIP: FrozenSet[str] = frozenset(
    {
        ".venv",
        "venv",
        ".tox",
        ".eggs",
        ".git",
        ".hg",
        ".mypy_cache",
        ".nox",
        ".svn",
        ".bzr",
        "_build",
        "buck-out",
        "build",
        "dist",
        ".pants.d",
        ".direnv",
        "node_modules",
        "__pypackages__",
        ".pytype",
    }
)

CONFIG_SECTIONS: Dict[str, Tuple[str, ...]] = {
    ".isort.cfg": ("settings", "isort"),
    "pyproject.toml": ("tool.isort",),
    "setup.cfg": ("isort", "tool:isort"),
    "tox.ini": ("isort", "tool:isort"),
    ".editorconfig": ("*", "*.py", "**.py", "*.{py}"),
}
FALLBACK_CONFIG_SECTIONS: Tuple[str, ...] = ("isort", "tool:isort", "tool.isort")

IMPORT_HEADING_PREFIX = "import_heading_"
IMPORT_FOOTER_PREFIX = "import_footer_"
KNOWN_PREFIX = "known_"
KNOWN_SECTION_MAPPING: Dict[str, str] = {
    STDLIB: "STANDARD_LIBRARY",
    FUTURE: "FUTURE_LIBRARY",
    FIRSTPARTY: "FIRST_PARTY",
    THIRDPARTY: "THIRD_PARTY",
    LOCALFOLDER: "LOCAL_FOLDER",
}

RUNTIME_SOURCE = "runtime"

DEPRECATED_SETTINGS = ("not_skip", "keep_direct_and_as_imports")

_STR_BOOLEAN_MAPPING = {
    "y": True,
    "yes": True,
    "t": True,
    "on": True,
    "1": True,
    "true": True,
    "n": False,
    "no": False,
    "f": False,
    "off": False,
    "0": False,
    "false": False,
}


@dataclass(frozen=True)
class _Config:
    """Defines the data schema and defaults used for isort configuration.

    NOTE: known lists, such as known_standard_library, are intentionally not complete as they are
    dynamically determined later on.
    """

    py_version: str = "3"
    force_to_top: FrozenSet[str] = frozenset()
    skip: FrozenSet[str] = DEFAULT_SKIP
    extend_skip: FrozenSet[str] = frozenset()
    skip_glob: FrozenSet[str] = frozenset()
    extend_skip_glob: FrozenSet[str] = frozenset()
    skip_gitignore: bool = False
    line_length: int = 79
    wrap_length: int = 0
    line_ending: str = ""
    sections: Tuple[str, ...] = SECTION_DEFAULTS
    no_sections: bool = False
    known_future_library: FrozenSet[str] = frozenset(("__future__",))
    known_third_party: FrozenSet[str] = frozenset()
    known_first_party: FrozenSet[str] = frozenset()
    known_local_folder: FrozenSet[str] = frozenset()
    known_standard_library: FrozenSet[str] = frozenset()
    extra_standard_library: FrozenSet[str] = frozenset()
    known_other: Dict[str, FrozenSet[str]] = field(default_factory=dict)
    multi_line_output: WrapModes = WrapModes.GRID  # type: ignore
    forced_separate: Tuple[str, ...] = ()
    indent: str = " " * 4
    comment_prefix: str = "  #"
    length_sort: bool = False
    length_sort_straight: bool = False
    length_sort_sections: FrozenSet[str] = frozenset()
    add_imports: FrozenSet[str] = frozenset()
    remove_imports: FrozenSet[str] = frozenset()
    append_only: bool = False
    reverse_relative: bool = False
    force_single_line: bool = False
    single_line_exclusions: Tuple[str, ...] = ()
    default_section: str = THIRDPARTY
    import_headings: Dict[str, str] = field(default_factory=dict)
    import_footers: Dict[str, str] = field(default_factory=dict)
    balanced_wrapping: bool = False
    use_parentheses: bool = False
    order_by_type: bool = True
    atomic: bool = False
    lines_before_imports: int = -1
    lines_after_imports: int = -1
    lines_between_sections: int = 1
    lines_between_types: int = 0
    combine_as_imports: bool = False
    combine_star: bool = False
    include_trailing_comma: bool = False
    from_first: bool = False
    verbose: bool = False
    quiet: bool = False
    force_adds: bool = False
    force_alphabetical_sort_within_sections: bool = False
    force_alphabetical_sort: bool = False
    force_grid_wrap: int = 0
    force_sort_within_sections: bool = False
    lexicographical: bool = False
    group_by_package: bool = False
    ignore_whitespace: bool = False
    no_lines_before: FrozenSet[str] = frozenset()
    no_inline_sort: bool = False
    ignore_comments: bool = False
    case_sensitive: bool = False
    sources: Tuple[Dict[str, Any], ...] = ()
    virtual_env: str = ""
    conda_env: str = ""
    ensure_newline_before_comments: bool = False
    directory: str = ""
    profile: str = ""
    honor_noqa: bool = False
    src_paths: Tuple[Path, ...] = ()
    old_finders: bool = False
    remove_redundant_aliases: bool = False
    float_to_top: bool = False
    filter_files: bool = False
    formatter: str = ""
    formatting_function: Optional[Callable[[str, str, object], str]] = None
    color_output: bool = False
    treat_comments_as_code: FrozenSet[str] = frozenset()
    treat_all_comments_as_code: bool = False
    supported_extensions: FrozenSet[str] = SUPPORTED_EXTENSIONS
    blocked_extensions: FrozenSet[str] = BLOCKED_EXTENSIONS
    constants: FrozenSet[str] = frozenset()
    classes: FrozenSet[str] = frozenset()
    variables: FrozenSet[str] = frozenset()
    dedup_headings: bool = False
    only_sections: bool = False
    only_modified: bool = False
    combine_straight_imports: bool = False
    auto_identify_namespace_packages: bool = True
    namespace_packages: FrozenSet[str] = frozenset()
    follow_links: bool = True
    indented_import_headings: bool = True
    honor_case_in_force_sorted_sections: bool = False
    sort_relative_in_force_sorted_sections: bool = False
    overwrite_in_place: bool = False
    reverse_sort: bool = False
    star_first: bool = False
    import_dependencies = Dict[str, str]
    git_ls_files: Dict[Path, Set[str]] = field(default_factory=dict)
    format_error: str = "{error}: {message}"
    format_success: str = "{success}: {message}"
    sort_order: str = "natural"
    sort_reexports: bool = False
    split_on_trailing_comma: bool = False

    def __post_init__(self) -> None:
        py_version = self.py_version
        if py_version == "auto":  # pragma: no cover
            py_version = f"{sys.version_info.major}{sys.version_info.minor}"

        if py_version not in VALID_PY_TARGETS:
            raise ValueError(
                f"The python version {py_version} is not supported. "
                "You can set a python version with the -py or --python-version flag. "
                f"The following versions are supported: {VALID_PY_TARGETS}"
            )

        if py_version != "all":
            object.__setattr__(self, "py_version", f"py{py_version}")

        if not self.known_standard_library:
            object.__setattr__(
                self, "known_standard_library", frozenset(getattr(stdlibs, self.py_version).stdlib)
            )

        if self.multi_line_output == WrapModes.VERTICAL_GRID_GROUPED_NO_COMMA:  # type: ignore
            vertical_grid_grouped = WrapModes.VERTICAL_GRID_GROUPED  # type: ignore
            object.__setattr__(self, "multi_line_output", vertical_grid_grouped)
        if self.force_alphabetical_sort:
            object.__setattr__(self, "force_alphabetical_sort_within_sections", True)
            object.__setattr__(self, "no_sections", True)
            object.__setattr__(self, "lines_between_types", 1)
            object.__setattr__(self, "from_first", True)
        if self.wrap_length > self.line_length:
            raise ValueError(
                "wrap_length must be set lower than or equal to line_length: "
                f"{self.wrap_length} > {self.line_length}."
            )

    def __hash__(self) -> int:
        return id(self)


_DEFAULT_SETTINGS = {**vars(_Config()), "source": "defaults"}


class Config(_Config):
    def __init__(
        self,
        settings_file: str = "",
        settings_path: str = "",
        config: Optional[_Config] = None,
        **config_overrides: Any,
    ):
        self._known_patterns: Optional[List[Tuple[Pattern[str], str]]] = None
        self._section_comments: Optional[Tuple[str, ...]] = None
        self._section_comments_end: Optional[Tuple[str, ...]] = None
        self._skips: Optional[FrozenSet[str]] = None
        self._skip_globs: Optional[FrozenSet[str]] = None
        self._sorting_function: Optional[Callable[..., List[str]]] = None

        if config:
            config_vars = vars(config).copy()
            config_vars.update(config_overrides)
            config_vars["py_version"] = config_vars["py_version"].replace("py", "")
            config_vars.pop("_known_patterns")
            config_vars.pop("_section_comments")
            config_vars.pop("_section_comments_end")
            config_vars.pop("_skips")
            config_vars.pop("_skip_globs")
            config_vars.pop("_sorting_function")
            super().__init__(**config_vars)
            return

        # We can't use self.quiet to conditionally show warnings before super.__init__() is called
        # at the end of this method. _Config is also frozen so setting self.quiet isn't possible.
        # Therefore we extract quiet early here in a variable and use that in warning conditions.
        quiet = config_overrides.get("quiet", False)

        sources: List[Dict[str, Any]] = [_DEFAULT_SETTINGS]

        config_settings: Dict[str, Any]
        project_root: str
        if settings_file:
            config_settings = _get_config_data(
                settings_file,
                CONFIG_SECTIONS.get(os.path.basename(settings_file), FALLBACK_CONFIG_SECTIONS),
            )
            project_root = os.path.dirname(settings_file)
            if not config_settings and not quiet:
                warn(
                    f"A custom settings file was specified: {settings_file} but no configuration "
                    "was found inside. This can happen when [settings] is used as the config "
                    "header instead of [isort]. "
                    "See: https://pycqa.github.io/isort/docs/configuration/config_files"
                    "#custom-config-files for more information.",
                    stacklevel=2,
                )
        elif settings_path:
            if not os.path.exists(settings_path):
                raise InvalidSettingsPath(settings_path)

            settings_path = os.path.abspath(settings_path)
            project_root, config_settings = _find_config(settings_path)
        else:
            config_settings = {}
            project_root = os.getcwd()

        profile_name = config_overrides.get("profile", config_settings.get("profile", ""))
        profile: Dict[str, Any] = {}
        if profile_name:
            if profile_name not in profiles:
                import pkg_resources

                for plugin in pkg_resources.iter_entry_points("isort.profiles"):
                    profiles.setdefault(plugin.name, plugin.load())

            if profile_name not in profiles:
                raise ProfileDoesNotExist(profile_name)

            profile = profiles[profile_name].copy()
            profile["source"] = f"{profile_name} profile"
            sources.append(profile)

        if config_settings:
            sources.append(config_settings)
        if config_overrides:
            config_overrides["source"] = RUNTIME_SOURCE
            sources.append(config_overrides)

        combined_config = {**profile, **config_settings, **config_overrides}
        if "indent" in combined_config:
            indent = str(combined_config["indent"])
            if indent.isdigit():
                indent = " " * int(indent)
            else:
                indent = indent.strip("'").strip('"')
                if indent.lower() == "tab":
                    indent = "\t"
            combined_config["indent"] = indent

        known_other = {}
        import_headings = {}
        import_footers = {}
        for key, value in tuple(combined_config.items()):
            # Collect all known sections beyond those that have direct entries
            if key.startswith(KNOWN_PREFIX) and key not in (
                "known_standard_library",
                "known_future_library",
                "known_third_party",
                "known_first_party",
                "known_local_folder",
            ):
                import_heading = key[len(KNOWN_PREFIX) :].lower()
                maps_to_section = import_heading.upper()
                combined_config.pop(key)
                if maps_to_section in KNOWN_SECTION_MAPPING:
                    section_name = f"known_{KNOWN_SECTION_MAPPING[maps_to_section].lower()}"
                    if section_name in combined_config and not quiet:
                        warn(
                            f"Can't set both {key} and {section_name} in the same config file.\n"
                            f"Default to {section_name} if unsure."
                            "\n\n"
                            "See: https://pycqa.github.io/isort/"
                            "#custom-sections-and-ordering.",
                            stacklevel=2,
                        )
                    else:
                        combined_config[section_name] = frozenset(value)
                else:
                    known_other[import_heading] = frozenset(value)
                    if maps_to_section not in combined_config.get("sections", ()) and not quiet:
                        warn(
                            f"`{key}` setting is defined, but {maps_to_section} is not"
                            " included in `sections` config option:"
                            f" {combined_config.get('sections', SECTION_DEFAULTS)}.\n\n"
                            "See: https://pycqa.github.io/isort/"
                            "#custom-sections-and-ordering.",
                            stacklevel=2,
                        )
            if key.startswith(IMPORT_HEADING_PREFIX):
                import_headings[key[len(IMPORT_HEADING_PREFIX) :].lower()] = str(value)
            if key.startswith(IMPORT_FOOTER_PREFIX):
                import_footers[key[len(IMPORT_FOOTER_PREFIX) :].lower()] = str(value)

            # Coerce all provided config values into their correct type
            default_value = _DEFAULT_SETTINGS.get(key, None)
            if default_value is None:
                continue

            combined_config[key] = type(default_value)(value)

        for section in combined_config.get("sections", ()):
            if section in SECTION_DEFAULTS:
                continue

            if section.lower() not in known_other:
                config_keys = ", ".join(known_other.keys())
                warn(
                    f"`sections` setting includes {section}, but no known_{section.lower()} "
                    "is defined. "
                    f"The following known_SECTION config options are defined: {config_keys}.",
                    stacklevel=2,
                )

        if "directory" not in combined_config:
            combined_config["directory"] = (
                os.path.dirname(config_settings["source"])
                if config_settings.get("source", None)
                else os.getcwd()
            )

        path_root = Path(combined_config.get("directory", project_root)).resolve()
        path_root = path_root if path_root.is_dir() else path_root.parent
        if "src_paths" not in combined_config:
            combined_config["src_paths"] = (path_root / "src", path_root)
        else:
            src_paths: List[Path] = []
            for src_path in combined_config.get("src_paths", ()):
                full_paths = (
                    path_root.glob(src_path) if "*" in str(src_path) else [path_root / src_path]
                )
                for path in full_paths:
                    if path not in src_paths:
                        src_paths.append(path)

            combined_config["src_paths"] = tuple(src_paths)

        if "formatter" in combined_config:
            import pkg_resources

            for plugin in pkg_resources.iter_entry_points("isort.formatters"):
                if plugin.name == combined_config["formatter"]:
                    combined_config["formatting_function"] = plugin.load()
                    break
            else:
                raise FormattingPluginDoesNotExist(combined_config["formatter"])

        # Remove any config values that are used for creating config object but
        # aren't defined in dataclass
        combined_config.pop("source", None)
        combined_config.pop("sources", None)
        combined_config.pop("runtime_src_paths", None)

        deprecated_options_used = [
            option for option in combined_config if option in DEPRECATED_SETTINGS
        ]
        if deprecated_options_used:
            for deprecated_option in deprecated_options_used:
                combined_config.pop(deprecated_option)
            if not quiet:
                warn(
                    "W0503: Deprecated config options were used: "
                    f"{', '.join(deprecated_options_used)}."
                    "Please see the 5.0.0 upgrade guide: "
                    "https://pycqa.github.io/isort/docs/upgrade_guides/5.0.0.html",
                    stacklevel=2,
                )

        if known_other:
            combined_config["known_other"] = known_other
        if import_headings:
            for import_heading_key in import_headings:
                combined_config.pop(f"{IMPORT_HEADING_PREFIX}{import_heading_key}")
            combined_config["import_headings"] = import_headings
        if import_footers:
            for import_footer_key in import_footers:
                combined_config.pop(f"{IMPORT_FOOTER_PREFIX}{import_footer_key}")
            combined_config["import_footers"] = import_footers

        unsupported_config_errors = {}
        for option in set(combined_config.keys()).difference(
            getattr(_Config, "__dataclass_fields__", {}).keys()
        ):
            for source in reversed(sources):
                if option in source:
                    unsupported_config_errors[option] = {
                        "value": source[option],
                        "source": source["source"],
                    }
        if unsupported_config_errors:
            raise UnsupportedSettings(unsupported_config_errors)

        super().__init__(sources=tuple(sources), **combined_config)

    def is_supported_filetype(self, file_name: str) -> bool:
        _root, ext = os.path.splitext(file_name)
        ext = ext.lstrip(".")
        if ext in self.supported_extensions:
            return True
        if ext in self.blocked_extensions:
            return False

        # Skip editor backup files.
        if file_name.endswith("~"):
            return False

        try:
            if stat.S_ISFIFO(os.stat(file_name).st_mode):
                return False
        except OSError:
            pass

        try:
            with open(file_name, "rb") as fp:
                line = fp.readline(100)
        except OSError:
            return False
        return bool(_SHEBANG_RE.match(line))

    def _check_folder_git_ls_files(self, folder: str) -> Optional[Path]:
        env = {**os.environ, "LANG": "C.UTF-8"}
        try:
            topfolder_result = subprocess.check_output(  # nosec # skipcq: PYL-W1510
                ["git", "-C", folder, "rev-parse", "--show-toplevel"], encoding="utf-8", env=env
            )
        except subprocess.CalledProcessError:
            return None

        git_folder = Path(topfolder_result.rstrip()).resolve()

        # files committed to git
        tracked_files = (
            subprocess.check_output(  # nosec # skipcq: PYL-W1510
                ["git", "-C", str(git_folder), "ls-files", "-z"],
                encoding="utf-8",
                env=env,
            )
            .rstrip("\0")
            .split("\0")
        )
        # files that haven't been committed yet, but aren't ignored
        tracked_files_others = (
            subprocess.check_output(  # nosec # skipcq: PYL-W1510
                ["git", "-C", str(git_folder), "ls-files", "-z", "--others", "--exclude-standard"],
                encoding="utf-8",
                env=env,
            )
            .rstrip("\0")
            .split("\0")
        )

        self.git_ls_files[git_folder] = {
            str(git_folder / Path(f)) for f in tracked_files + tracked_files_others
        }
        return git_folder

    def is_skipped(self, file_path: Path) -> bool:
        """Returns True if the file and/or folder should be skipped based on current settings."""
        if self.directory and Path(self.directory) in file_path.resolve().parents:
            file_name = os.path.relpath(file_path.resolve(), self.directory)
        else:
            file_name = str(file_path)

        os_path = str(file_path)

        normalized_path = os_path.replace("\\", "/")
        if normalized_path[1:2] == ":":
            normalized_path = normalized_path[2:]

        for skip_path in self.skips:
            if posixpath.abspath(normalized_path) == posixpath.abspath(
                skip_path.replace("\\", "/")
            ):
                return True

        position = os.path.split(file_name)
        while position[1]:
            if position[1] in self.skips:
                return True
            position = os.path.split(position[0])

        for sglob in self.skip_globs:
            if fnmatch.fnmatch(file_name, sglob) or fnmatch.fnmatch("/" + file_name, sglob):
                return True

        if not (os.path.isfile(os_path) or os.path.isdir(os_path) or os.path.islink(os_path)):
            return True

        if self.skip_gitignore:
            if file_path.name == ".git":  # pragma: no cover
                return True

            git_folder = None

            file_paths = [file_path, file_path.resolve()]
            for folder in self.git_ls_files:
                if any(folder in path.parents for path in file_paths):
                    git_folder = folder
                    break
            else:
                git_folder = self._check_folder_git_ls_files(str(file_path.parent))

            # git_ls_files are good files you should parse. If you're not in the allow list, skip.

            if (
                git_folder
                and not file_path.is_dir()
                and str(file_path.resolve()) not in self.git_ls_files[git_folder]
            ):
                return True

        return False

    @property
    def known_patterns(self) -> List[Tuple[Pattern[str], str]]:
        if self._known_patterns is not None:
            return self._known_patterns

        self._known_patterns = []
        pattern_sections = [STDLIB] + [section for section in self.sections if section != STDLIB]
        for placement in reversed(pattern_sections):
            known_placement = KNOWN_SECTION_MAPPING.get(placement, placement).lower()
            config_key = f"{KNOWN_PREFIX}{known_placement}"
            known_modules = getattr(self, config_key, self.known_other.get(known_placement, ()))
            extra_modules = getattr(self, f"extra_{known_placement}", ())
            all_modules = set(extra_modules).union(known_modules)
            known_patterns = [
                pattern
                for known_pattern in all_modules
                for pattern in self._parse_known_pattern(known_pattern)
            ]
            for known_pattern in known_patterns:
                regexp = "^" + known_pattern.replace("*", ".*").replace("?", ".?") + "$"
                self._known_patterns.append((re.compile(regexp), placement))

        return self._known_patterns

    @property
    def section_comments(self) -> Tuple[str, ...]:
        if self._section_comments is not None:
            return self._section_comments

        self._section_comments = tuple(f"# {heading}" for heading in self.import_headings.values())
        return self._section_comments

    @property
    def section_comments_end(self) -> Tuple[str, ...]:
        if self._section_comments_end is not None:
            return self._section_comments_end

        self._section_comments_end = tuple(f"# {footer}" for footer in self.import_footers.values())
        return self._section_comments_end

    @property
    def skips(self) -> FrozenSet[str]:
        if self._skips is not None:
            return self._skips

        self._skips = self.skip.union(self.extend_skip)
        return self._skips

    @property
    def skip_globs(self) -> FrozenSet[str]:
        if self._skip_globs is not None:
            return self._skip_globs

        self._skip_globs = self.skip_glob.union(self.extend_skip_glob)
        return self._skip_globs

    @property
    def sorting_function(self) -> Callable[..., List[str]]:
        if self._sorting_function is not None:
            return self._sorting_function

        if self.sort_order == "natural":
            self._sorting_function = sorting.naturally
        elif self.sort_order == "native":
            self._sorting_function = sorted
        else:
            available_sort_orders = ["natural", "native"]
            import pkg_resources

            for sort_plugin in pkg_resources.iter_entry_points("isort.sort_function"):
                available_sort_orders.append(sort_plugin.name)
                if sort_plugin.name == self.sort_order:
                    self._sorting_function = sort_plugin.load()
                    break
            else:
                raise SortingFunctionDoesNotExist(self.sort_order, available_sort_orders)

        return self._sorting_function

    def _parse_known_pattern(self, pattern: str) -> List[str]:
        """Expand pattern if identified as a directory and return found sub packages"""
        if pattern.endswith(os.path.sep):
            patterns = [
                filename
                for filename in os.listdir(os.path.join(self.directory, pattern))
                if os.path.isdir(os.path.join(self.directory, pattern, filename))
            ]
        else:
            patterns = [pattern]

        return patterns


def _get_str_to_type_converter(setting_name: str) -> Union[Callable[[str], Any], Type[Any]]:
    type_converter: Union[Callable[[str], Any], Type[Any]] = type(
        _DEFAULT_SETTINGS.get(setting_name, "")
    )
    if type_converter == WrapModes:
        type_converter = wrap_mode_from_string
    return type_converter


def _as_list(value: str) -> List[str]:
    if isinstance(value, list):
        return [item.strip() for item in value]
    filtered = [item.strip() for item in value.replace("\n", ",").split(",") if item.strip()]
    return filtered


def _abspaths(cwd: str, values: Iterable[str]) -> Set[str]:
    paths = {
        (
            os.path.join(cwd, value)
            if not value.startswith(os.path.sep) and value.endswith(os.path.sep)
            else value
        )
        for value in values
    }
    return paths


def _find_config(path: str) -> Tuple[str, Dict[str, Any]]:
    current_directory = path
    tries = 0
    while current_directory and tries < MAX_CONFIG_SEARCH_DEPTH:
        for config_file_name in CONFIG_SOURCES:
            potential_config_file = os.path.join(current_directory, config_file_name)
            if os.path.isfile(potential_config_file):
                config_data: Dict[str, Any]
                try:
                    config_data = _get_config_data(
                        potential_config_file, CONFIG_SECTIONS[config_file_name]
                    )
                except Exception:
                    warn(
                        f"Failed to pull configuration information from {potential_config_file}",
                        stacklevel=2,
                    )
                    config_data = {}
                if config_data:
                    return (current_directory, config_data)

        for stop_dir in STOP_CONFIG_SEARCH_ON_DIRS:
            if os.path.isdir(os.path.join(current_directory, stop_dir)):
                return (current_directory, {})

        new_directory = os.path.split(current_directory)[0]
        if new_directory == current_directory:
            break

        current_directory = new_directory
        tries += 1

    return (path, {})


def find_all_configs(path: str) -> Trie:
    """
    Looks for config files in the path provided and in all of its sub-directories.
    Parses and stores any config file encountered in a trie and returns the root of
    the trie
    """
    trie_root = Trie("default", {})

    for dirpath, _, _ in os.walk(path):
        for config_file_name in CONFIG_SOURCES:
            potential_config_file = os.path.join(dirpath, config_file_name)
            if os.path.isfile(potential_config_file):
                config_data: Dict[str, Any]
                try:
                    config_data = _get_config_data(
                        potential_config_file, CONFIG_SECTIONS[config_file_name]
                    )
                except Exception:
                    warn(
                        f"Failed to pull configuration information from {potential_config_file}",
                        stacklevel=2,
                    )
                    config_data = {}

                if config_data:
                    trie_root.insert(potential_config_file, config_data)
                    break

    return trie_root


def _get_config_data(file_path: str, sections: Tuple[str, ...]) -> Dict[str, Any]:
    settings: Dict[str, Any] = {}

    if file_path.endswith(".toml"):
        with open(file_path, "rb") as bin_config_file:
            config = tomllib.load(bin_config_file)
        for section in sections:
            config_section = config
            for key in section.split("."):
                config_section = config_section.get(key, {})
            settings.update(config_section)
    else:
        with open(file_path, encoding="utf-8") as config_file:
            if file_path.endswith(".editorconfig"):
                line = "\n"
                last_position = config_file.tell()
                while line:
                    line = config_file.readline()
                    if "[" in line:
                        config_file.seek(last_position)
                        break
                    last_position = config_file.tell()

            config = configparser.ConfigParser(strict=False)
            config.read_file(config_file)
        for section in sections:
            if section.startswith("*.{") and section.endswith("}"):
                extension = section[len("*.{") : -1]
                for config_key in config:
                    if (
                        config_key.startswith("*.{")
                        and config_key.endswith("}")
                        and extension
                        in (text.strip() for text in config_key[len("*.{") : -1].split(","))
                    ):
                        settings.update(config.items(config_key))

            elif config.has_section(section):
                settings.update(config.items(section))

    if settings:
        settings["source"] = file_path

        if file_path.endswith(".editorconfig"):
            indent_style = settings.pop("indent_style", "").strip()
            indent_size = settings.pop("indent_size", "").strip()
            if indent_size == "tab":
                indent_size = settings.pop("tab_width", "").strip()

            if indent_style == "space":
                settings["indent"] = " " * ((indent_size and int(indent_size)) or 4)

            elif indent_style == "tab":
                settings["indent"] = "\t" * ((indent_size and int(indent_size)) or 1)

            max_line_length = settings.pop("max_line_length", "").strip()
            if max_line_length and (max_line_length == "off" or max_line_length.isdigit()):
                settings["line_length"] = (
                    float("inf") if max_line_length == "off" else int(max_line_length)
                )
            settings = {
                key: value
                for key, value in settings.items()
                if key in _DEFAULT_SETTINGS or key.startswith(KNOWN_PREFIX)
            }

        for key, value in settings.items():
            existing_value_type = _get_str_to_type_converter(key)
            if existing_value_type is tuple:
                settings[key] = tuple(_as_list(value))
            elif existing_value_type is frozenset:
                settings[key] = frozenset(_as_list(settings.get(key)))  # type: ignore
            elif existing_value_type is bool:
                # Only some configuration formats support native boolean values.
                if not isinstance(value, bool):
                    value = _as_bool(value)
                settings[key] = value
            elif key.startswith(KNOWN_PREFIX):
                settings[key] = _abspaths(os.path.dirname(file_path), _as_list(value))
            elif key == "force_grid_wrap":
                try:
                    result = existing_value_type(value)
                except ValueError:  # backwards compatibility for true / false force grid wrap
                    result = 0 if value.lower().strip() == "false" else 2
                settings[key] = result
            elif key == "comment_prefix":
                settings[key] = str(value).strip("'").strip('"')
            else:
                settings[key] = existing_value_type(value)

    return settings


def _as_bool(value: str) -> bool:
    """Given a string value that represents True or False, returns the Boolean equivalent.
    Heavily inspired from distutils strtobool.
    """
    try:
        return _STR_BOOLEAN_MAPPING[value.lower()]
    except KeyError:
        raise ValueError(f"invalid truth value {value}")


DEFAULT_CONFIG = Config()



## Diretórios de Templates Encontrados

- templates
  Arquivos:
  - base.html
  - includes\form_errors.html
  - includes\form_field.html
- alunos\templates
  Arquivos:
  - alunos\confirmar_remocao_instrutoria.html
  - alunos\criar_aluno.html
  - alunos\dashboard.html
  - alunos\detalhar_aluno.html
  - alunos\diagnostico_instrutores.html
  - alunos\editar_aluno.html
  - alunos\excluir_aluno.html
  - alunos\formulario_aluno.html
  - alunos\importar_alunos.html
  - alunos\listar_alunos.html
  - alunos\registro.html
  - alunos\relatorio_alunos.html
- atividades\templates
  Arquivos:
  - atividades\calendario_atividades.html
  - atividades\confirmar_copia_academica.html
  - atividades\confirmar_copia_ritualistica.html
  - atividades\confirmar_exclusao_academica.html
  - atividades\confirmar_exclusao_ritualistica.html
  - atividades\copiar_atividade_academica.html
  - atividades\copiar_atividade_ritualistica.html
  - atividades\criar_atividade_academica.html
  - atividades\criar_atividade_ritualistica.html
  - atividades\dashboard.html
  - atividades\dashboard_atividades.html
  - atividades\detalhar_atividade_academica.html
  - atividades\detalhar_atividade_ritualistica.html
  - atividades\editar_atividade_academica.html
  - atividades\editar_atividade_ritualistica.html
  - atividades\excluir_atividade_academica.html
  - atividades\excluir_atividade_ritualistica.html
  - atividades\formulario_atividade_academica.html
  - atividades\formulario_atividade_ritualistica.html
  - atividades\index.html
  - atividades\listar_atividades.html
  - atividades\listar_atividades_academicas.html
  - atividades\listar_atividades_ritualisticas.html
  - atividades\registrar_frequencia.html
  - atividades\relatorio_atividades.html
  - atividades\visualizar_frequencia.html
- cargos\templates
  Arquivos:
  - cargos\atribuir_cargo.html
  - cargos\confirmar_exclusao.html
  - cargos\criar_cargo.html
  - cargos\detalhar_cargo.html
  - cargos\detalhes_cargo.html
  - cargos\detalhe_cargo.html
  - cargos\editar_cargo.html
  - cargos\excluir_cargo.html
  - cargos\formulario_cargo.html
  - cargos\form_cargo.html
  - cargos\listar_cargos.html
  - cargos\remover_atribuicao.html
- core\templates
  Arquivos:
- cursos\templates
  Arquivos:
  - cursos\criar_curso.html
  - cursos\detalhar_curso.html
  - cursos\editar_curso.html
  - cursos\excluir_curso.html
  - cursos\listar_cursos.html
- frequencias\templates
  Arquivos:
  - frequencias\criar_notificacao.html
  - frequencias\dashboard.html
  - frequencias\detalhar_carencia.html
  - frequencias\detalhar_frequencia.html
  - frequencias\detalhar_frequencia_mensal.html
  - frequencias\detalhar_notificacao.html
  - frequencias\editar_carencia.html
  - frequencias\editar_frequencia.html
  - frequencias\editar_notificacao.html
  - frequencias\enviar_notificacao.html
  - frequencias\estatisticas_frequencia.html
  - frequencias\excluir_frequencia.html
  - frequencias\excluir_frequencia_mensal.html
  - frequencias\filtro_painel_frequencias.html
  - frequencias\formulario_frequencia_mensal.html
  - frequencias\gerar_frequencia_mensal.html
  - frequencias\gerenciar_carencias.html
  - frequencias\historico_frequencia.html
  - frequencias\iniciar_acompanhamento.html
  - frequencias\listar_carencias.html
  - frequencias\listar_frequencias.html
  - frequencias\notificacoes_carencia.html
  - frequencias\painel_frequencias.html
  - frequencias\registrar_frequencia.html
  - frequencias\registrar_frequencia_turma.html
  - frequencias\relatorio_carencias.html
  - frequencias\relatorio_frequencias.html
  - frequencias\resolver_carencia.html
  - frequencias\responder_notificacao.html
  - frequencias\visualizar_resposta.html
- iniciacoes\templates
  Arquivos:
  - iniciacoes\criar_grau.html
  - iniciacoes\criar_iniciacao.html
  - iniciacoes\detalhar_iniciacao.html
  - iniciacoes\editar_grau.html
  - iniciacoes\editar_iniciacao.html
  - iniciacoes\excluir_grau.html
  - iniciacoes\excluir_iniciacao.html
  - iniciacoes\listar_graus.html
  - iniciacoes\listar_iniciacoes.html
- matriculas\templates
  Arquivos:
  - matriculas\cancelar_matricula.html
  - matriculas\detalhes_matricula.html
  - matriculas\listar_matriculas.html
  - matriculas\realizar_matricula.html
- notas\templates
  Arquivos:
  - notas\listar_notas.html
- omaum\templates
  Arquivos:
  - 403.html
  - 404.html
  - 500.html
  - atualizar_configuracao.html
  - base.html
  - csrf_test.html
  - home.html
  - home_old.html
  - listar_alunos.html
  - lista_categorias.html
  - manutencao.html
  - painel_controle.html
  - includes\form_error.html
  - includes\form_errors.html
  - includes\form_field.html
  - registration\login.html
  - registration\registro.html
- pagamentos\templates
  Arquivos:
  - pagamentos\listar_pagamentos.html
- presencas\templates
  Arquivos:
  - presencas\detalhar_presenca.html
  - presencas\editar_presenca.html
  - presencas\excluir_presenca.html
  - presencas\formulario_presenca.html
  - presencas\formulario_presencas_multiplas.html
  - presencas\formulario_presencas_multiplas_passo1.html
  - presencas\formulario_presencas_multiplas_passo2.html
  - presencas\listar_presencas.html
  - presencas\registrar_presenca.html
  - presencas\registrar_presenca_multipla.html
  - presencas\relatorio_presencas.html
- punicoes\templates
  Arquivos:
  - punicoes\criar_punicao.html
  - punicoes\criar_tipo_punicao.html
  - punicoes\detalhar_punicao.html
  - punicoes\detalhe_punicao.html
  - punicoes\editar_punicao.html
  - punicoes\editar_tipo_punicao.html
  - punicoes\excluir_punicao.html
  - punicoes\excluir_tipo_punicao.html
  - punicoes\listar_punicoes.html
  - punicoes\listar_tipos_punicao.html
- relatorios\templates
  Arquivos:
  - relatorios\gerar_relatorio.html
  - relatorios\listar_relatorios.html
  - relatorios\relatorio_alunos.html
  - relatorios\relatorio_presencas.html
  - relatorios\relatorio_punicoes.html
- turmas\templates
  Arquivos:
  - turmas\adicionar_aluno.html
  - turmas\cancelar_matricula.html
  - turmas\confirmar_cancelamento_matricula.html
  - turmas\criar_turma.html
  - turmas\dashboard.html
  - turmas\dashboard_turmas.html
  - turmas\detalhar_turma.html
  - turmas\editar_turma.html
  - turmas\excluir_turma.html
  - turmas\formulario_instrutoria.html
  - turmas\listar_alunos_matriculados.html
  - turmas\listar_turmas.html
  - turmas\matricular_aluno.html
  - turmas\registrar_frequencia_turma.html
  - turmas\relatorio_frequencia_turma.html
  - turmas\relatorio_turmas.html
  - turmas\turma_form.html
- venv\Lib\site-packages\debug_toolbar\templates
  Arquivos:
  - debug_toolbar\base.html
  - debug_toolbar\redirect.html
  - debug_toolbar\includes\panel_button.html
  - debug_toolbar\includes\panel_content.html
  - debug_toolbar\includes\theme_selector.html
  - debug_toolbar\panels\alerts.html
  - debug_toolbar\panels\cache.html
  - debug_toolbar\panels\headers.html
  - debug_toolbar\panels\history.html
  - debug_toolbar\panels\history_tr.html
  - debug_toolbar\panels\profiling.html
  - debug_toolbar\panels\request.html
  - debug_toolbar\panels\request_variables.html
  - debug_toolbar\panels\settings.html
  - debug_toolbar\panels\signals.html
  - debug_toolbar\panels\sql.html
  - debug_toolbar\panels\sql_explain.html
  - debug_toolbar\panels\sql_profile.html
  - debug_toolbar\panels\sql_select.html
  - debug_toolbar\panels\staticfiles.html
  - debug_toolbar\panels\templates.html
  - debug_toolbar\panels\template_source.html
  - debug_toolbar\panels\timer.html
  - debug_toolbar\panels\versions.html
- venv\Lib\site-packages\debug_toolbar\panels\templates
  Arquivos:
  - jinja2.py
  - panel.py
  - views.py
  - __init__.py
  - __pycache__\panel.cpython-312.pyc
  - __pycache__\views.cpython-312.pyc
  - __pycache__\__init__.cpython-312.pyc
- venv\Lib\site-packages\django\contrib\admin\templates
  Arquivos:
  - admin\404.html
  - admin\500.html
  - admin\actions.html
  - admin\app_index.html
  - admin\app_list.html
  - admin\base.html
  - admin\base_site.html
  - admin\change_form.html
  - admin\change_form_object_tools.html
  - admin\change_list.html
  - admin\change_list_object_tools.html
  - admin\change_list_results.html
  - admin\color_theme_toggle.html
  - admin\date_hierarchy.html
  - admin\delete_confirmation.html
  - admin\delete_selected_confirmation.html
  - admin\filter.html
  - admin\index.html
  - admin\invalid_setup.html
  - admin\login.html
  - admin\nav_sidebar.html
  - admin\object_history.html
  - admin\pagination.html
  - admin\popup_response.html
  - admin\prepopulated_fields_js.html
  - admin\search_form.html
  - admin\submit_line.html
  - admin\auth\user\add_form.html
  - admin\auth\user\change_password.html
  - admin\edit_inline\stacked.html
  - admin\edit_inline\tabular.html
  - admin\includes\fieldset.html
  - admin\includes\object_delete_summary.html
  - admin\widgets\clearable_file_input.html
  - admin\widgets\date.html
  - admin\widgets\foreign_key_raw_id.html
  - admin\widgets\many_to_many_raw_id.html
  - admin\widgets\radio.html
  - admin\widgets\related_widget_wrapper.html
  - admin\widgets\split_datetime.html
  - admin\widgets\time.html
  - admin\widgets\url.html
  - registration\logged_out.html
  - registration\password_change_done.html
  - registration\password_change_form.html
  - registration\password_reset_complete.html
  - registration\password_reset_confirm.html
  - registration\password_reset_done.html
  - registration\password_reset_email.html
  - registration\password_reset_form.html
- venv\Lib\site-packages\django\contrib\admindocs\templates
  Arquivos:
  - admin_doc\bookmarklets.html
  - admin_doc\index.html
  - admin_doc\missing_docutils.html
  - admin_doc\model_detail.html
  - admin_doc\model_index.html
  - admin_doc\template_detail.html
  - admin_doc\template_filter_index.html
  - admin_doc\template_tag_index.html
  - admin_doc\view_detail.html
  - admin_doc\view_index.html
- venv\Lib\site-packages\django\contrib\auth\templates
  Arquivos:
  - auth\widgets\read_only_password_hash.html
  - registration\password_reset_subject.txt
- venv\Lib\site-packages\django\contrib\gis\templates
  Arquivos:
  - gis\openlayers-osm.html
  - gis\openlayers.html
  - gis\kml\base.kml
  - gis\kml\placemarks.kml
- venv\Lib\site-packages\django\contrib\postgres\templates
  Arquivos:
  - postgres\widgets\split_array.html
- venv\Lib\site-packages\django\contrib\sitemaps\templates
  Arquivos:
  - sitemap.xml
  - sitemap_index.xml
- venv\Lib\site-packages\django\forms\templates
  Arquivos:
  - django\forms\attrs.html
  - django\forms\div.html
  - django\forms\field.html
  - django\forms\label.html
  - django\forms\p.html
  - django\forms\table.html
  - django\forms\ul.html
  - django\forms\errors\dict\default.html
  - django\forms\errors\dict\text.txt
  - django\forms\errors\dict\ul.html
  - django\forms\errors\list\default.html
  - django\forms\errors\list\text.txt
  - django\forms\errors\list\ul.html
  - django\forms\formsets\div.html
  - django\forms\formsets\p.html
  - django\forms\formsets\table.html
  - django\forms\formsets\ul.html
  - django\forms\widgets\attrs.html
  - django\forms\widgets\checkbox.html
  - django\forms\widgets\checkbox_option.html
  - django\forms\widgets\checkbox_select.html
  - django\forms\widgets\clearable_file_input.html
  - django\forms\widgets\date.html
  - django\forms\widgets\datetime.html
  - django\forms\widgets\email.html
  - django\forms\widgets\file.html
  - django\forms\widgets\hidden.html
  - django\forms\widgets\input.html
  - django\forms\widgets\input_option.html
  - django\forms\widgets\multiple_hidden.html
  - django\forms\widgets\multiple_input.html
  - django\forms\widgets\multiwidget.html
  - django\forms\widgets\number.html
  - django\forms\widgets\password.html
  - django\forms\widgets\radio.html
  - django\forms\widgets\radio_option.html
  - django\forms\widgets\select.html
  - django\forms\widgets\select_date.html
  - django\forms\widgets\select_option.html
  - django\forms\widgets\splitdatetime.html
  - django\forms\widgets\splithiddendatetime.html
  - django\forms\widgets\text.html
  - django\forms\widgets\textarea.html
  - django\forms\widgets\time.html
  - django\forms\widgets\url.html
- venv\Lib\site-packages\django\views\templates
  Arquivos:
  - csrf_403.html
  - default_urlconf.html
  - directory_index.html
  - i18n_catalog.js
  - technical_404.html
  - technical_500.html
  - technical_500.txt
- venv\Lib\site-packages\django_extensions\templates
  Arquivos:
  - django_extensions\graph_models\django2018\digraph.dot
  - django_extensions\graph_models\django2018\label.dot
  - django_extensions\graph_models\django2018\relation.dot
  - django_extensions\graph_models\original\digraph.dot
  - django_extensions\graph_models\original\label.dot
  - django_extensions\graph_models\original\relation.dot
  - django_extensions\widgets\foreignkey_searchinput.html

## Busca pelo template listar_alunos.html

Encontrado em: alunos\templates\alunos\listar_alunos.html
Encontrado em: omaum\templates\listar_alunos.html
