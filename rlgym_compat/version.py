# From https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/version.py
# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module module
# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '1.0.3'

release_notes = {
    '1.0.3': """
    - Updated to include all utils from RLGym
    """,
    '1.0.2': """
    - Fixed car_id
    """,
    '1.0.1': """
    - Fixed on_ground bug
    """,
    '1.0.0': """
    Initial Release
    - Tested with RLGym 0.4.1
    """
}


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def print_current_release_notes():
    print(f"Version {__version__}")
    print(get_current_release_notes())
    print("")
