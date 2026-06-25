from typing import Dict, Any
import sys

REQUIRED_KEYS = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'}


def parse(filepath: str) -> Dict[str, Any]:
    """Read and parse a config file, returning a dictionary of settings."""
    config: Dict[str, Any] = {}
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: config file '{filepath}' not found")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        if line == '':
            continue
        try:
            key, value = line.split('=')
        except ValueError:
            raise ValueError(f"Invalid line format: {line}")

        if not value:
            raise ValueError(f"Empty value for key: {key}")

        if key in ('WIDTH', 'HEIGHT'):
            config[key] = int(value)
        elif key in ('ENTRY', 'EXIT'):
            x, y = value.split(',')
            config[key] = (int(x), int(y))
        elif key == 'PERFECT':
            config[key] = value == 'True'
        else:
            config[key] = value

    missing = REQUIRED_KEYS - config.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    return config
