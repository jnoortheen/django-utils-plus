import codecs
import json
import os
from typing import Tuple, Dict

from django.conf import settings

NODE_PKGS = {}


def get_node_modules_dir() -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__name__)), 'node_modules')


def get_node_pkg_path() -> Tuple[str, str]:
    """return config json file paths"""
    root = getattr(settings, 'NODE_PKG_DIR', os.path.abspath(os.path.dirname(__name__)))
    return os.path.join(root, 'package.json'), os.path.join(root, 'package-lock.json')


def normalize_dict(deps) -> Dict[str, str]:
    deps = deps or {}
    for k, val in deps.items():
        if k in {'dependencies', 'devDependencies'}:
            return normalize_dict(val)
        deps[k] = val['version'] if isinstance(val, dict) and 'version' in val else val
    return deps


def parse_pkgs_dict(json_path) -> Dict[str, str]:
    pkgs = {}
    if os.path.exists(json_path):
        with codecs.open(json_path, 'r', 'utf-8') as reader:
            pkg_json = json.loads(reader.read())
            pkgs.update(normalize_dict(pkg_json))
    return pkgs


def load_node_pkgs() -> None:
    """read and parse package.json"""
    pkg_json, pkg_lock_json = get_node_pkg_path()
    if not os.path.exists(pkg_json):
        raise Exception(
            'No package.json found. Update settings.NODE_PKG_DIR to correct location in order to use cdn template tags'
        )
    NODE_PKGS.update(parse_pkgs_dict(pkg_json))
    NODE_PKGS.update(parse_pkgs_dict(pkg_lock_json))


def get_node_pkg_version(pkg) -> str:
    if not NODE_PKGS:
        load_node_pkgs()
    return NODE_PKGS.get(pkg, '')


def get_npm_pkg_path(filepath) -> str:
    filepath = filepath.lstrip('/')
    pkg_name, filepath = filepath.split('/', 1)
    pkg_version = get_node_pkg_version(pkg_name)
    return f'{pkg_name}@{pkg_version}/{filepath}'
