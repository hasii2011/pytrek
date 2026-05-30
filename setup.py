"""

Usage:
    python setup.py py2app
"""
from typing import Any
from typing import Dict


from sys import path

from pathlib import Path

from setuptools import setup
from setuptools import find_packages
# The directory containing this file
HERE = Path(__file__).parent

# Add src to sys.path so we can import pytrek for the version
# without requiring PYTHONPATH to be set externally
path.insert(0, str(HERE / "src"))

# noinspection PyPep8
from pytrek import __version__

APP = ['src/pytrek/PyTrek.py']

README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

DATA_FILES = [
    ('pytrek/resources/fonts', ['src/pytrek/resources/fonts/FuturistFixedWidth.ttf']),
    ('pytrek/resources/fonts', ['src/pytrek/resources/fonts/MonoFonto.ttf']),
    ('pytrek/resources/fonts', ['src/pytrek/resources/fonts/UniverseCondensed.ttf']),

    ('pytrek/resources/images', ['src/pytrek/resources/images/ArrowDown.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/ArrowDownHovered.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/ArrowDownPressed.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/ArrowUpPressed.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/ArrowUp.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/ArrowUpHovered.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/CancelButton.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/CancelButtonPressed.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/Commander.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/CommanderTorpedo.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/CommanderTorpedoExplosionSpriteSheet.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/CommanderTorpedoFollower.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/CommanderTorpedoMiss.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/EmptySpace.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/EnterpriseD.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/GalaxyScanBackground.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/GreyPanel.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/HelpOkButton.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/HelpOkButtonHovered.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/HelpOkButtonPressed.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonD7.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonTorpedo.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonTorpedoExplosionBlue.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonTorpedoExplosionGrey.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonTorpedoExplosionRed.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonTorpedoExplosionWhite.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonTorpedoFollower.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/KlingonTorpedoMiss.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/LongRangeSensorBackground.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/Mars.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/MediumDarkGrayPanel.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/Mercury.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/OkButton.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/OkButtonPressed.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/PhaserSpriteSheet.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/PhotonTorpedo.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/PhotonTorpedoExplosionSprites-license.txt']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/PhotonTorpedoMiss.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/PhotonTorpedoExplosionSpriteSheet.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/Pluto.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/QuadrantBackground.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/StarBase.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/SuperCommander.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/SuperCommanderTorpedo.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/SuperCommanderTorpedoExplosionSpriteSheet.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/SuperCommanderTorpedoFollower.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/SuperCommanderTorpedoMiss.png']),
    ('pytrek/resources/images', ['src/pytrek/resources/images/WarpEffectSpriteSheet.png']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/CommanderCannotFire.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/CommanderMove.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/CommanderTorpedo.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/Docked.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/EnterpriseBlocked.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/Impulse.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/Inaccurate.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/KlingonCannotFire.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/KlingonMove.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/KlingonTorpedo.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/PhaserFired.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/PhotonTorpedoFired.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/PhotonTorpedoExploded.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/PhotonTorpedoMisfire.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/PhotonTorpedoMiss.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/PleaseRepeatRequest.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/ShieldHit.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/SuperCommanderCannotFire.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/SuperCommanderMove.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/SuperCommanderTorpedo.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/UnableToComply.wav']),
    ('pytrek/resources/sounds', ['src/pytrek/resources/sounds/Warp.wav']),

    ('pytrek/resources', ['src/pytrek/resources/loggingConfiguration.json']),
    ('pytrek/resources', ['src/pytrek/resources/Help.txt']),
    ('pytrek/resources', ['src/pytrek/resources/Help.txt']),
]
PY2APP_OPTIONS: Dict[str, Any] = {
    'plist': {
        'NSRequiresAquaSystemAppearance': 'False',
        'CFBundleGetInfoString': 'Plays Star Trek 1975',
        'CFBundleIdentifier': 'game',
        'CFBundleShortVersionString': __version__,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'pytrek',
                'CFBundleTypeRole': 'Game'
            }
        ],
        'LSMinimumSystemVersion': '26.5',
        'LSEnvironment': {
            'APP_MODE': 'True',
            'PYTHONOPTIMIZE': '1',
        },
        'LSMultipleInstancesProhibited': 'True',
    }

}

setup(
    name='PyTrek',
    version=__version__,
    app=APP,
    data_files=DATA_FILES,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,

    url='https://github.com/hasii2011/pytrek',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Yet another classic Star Trek game re-written in Python and Arcade',
    long_description=README,
    options={'py2app': PY2APP_OPTIONS},
    setup_requires=['py2app'],
)
