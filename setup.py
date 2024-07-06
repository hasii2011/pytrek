"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['pytrek/PyTrekView.py']

README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()
VERSION = (HERE / 'pytrek/resources/version.txt').read_text()

DATA_FILES = [
    ('pytrek/resources/fonts', ['pytrek/resources/fonts/FuturistFixedWidth.ttf']),
    ('pytrek/resources/fonts', ['pytrek/resources/fonts/MonoFonto.ttf']),
    ('pytrek/resources/fonts', ['pytrek/resources/fonts/UniverseCondensed.ttf']),

    ('pytrek/resources/images', ['pytrek/resources/images/CancelButton.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/CancelButtonPressed.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/Commander.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/CommanderTorpedo.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/CommanderTorpedoExplosionSpriteSheet.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/CommanderTorpedoFollower.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/CommanderTorpedoMiss.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/EmptySpace.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/EnterpriseD.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/GalaxyScanBackground.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonD7.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonTorpedo.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonTorpedoExplosionBlue.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonTorpedoExplosionGrey.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonTorpedoExplosionRed.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonTorpedoExplosionWhite.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonTorpedoFollower.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/KlingonTorpedoMiss.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/LongRangeSensorBackground.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/Mars.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/Mercury.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/OkButton.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/OkButtonPressed.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/PhaserSpriteSheet.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/PhotonTorpedo.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/PhotonTorpedoExplosionSprites-license.txt']),
    ('pytrek/resources/images', ['pytrek/resources/images/PhotonTorpedoMiss.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/PhotonTorpedoExplosionSpriteSheet.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/Pluto.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/QuadrantBackground.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/StarBase.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/SuperCommander.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/SuperCommanderTorpedo.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/SuperCommanderTorpedoExplosionSpriteSheet.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/SuperCommanderTorpedoFollower.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/SuperCommanderTorpedoMiss.png']),
    ('pytrek/resources/images', ['pytrek/resources/images/WarpEffectSpriteSheet.png']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/CommanderCannotFire.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/CommanderMove.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/CommanderTorpedo.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/Docked.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/EnterpriseBlocked.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/Impulse.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/Inaccurate.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/KlingonCannotFire.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/KlingonMove.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/KlingonTorpedo.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/PhaserFired.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/PhotonTorpedoFired.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/PhotonTorpedoExploded.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/PhotonTorpedoMisfire.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/PhotonTorpedoMiss.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/PleaseRepeatRequest.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/ShieldHit.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/SuperCommanderCannotFire.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/SuperCommanderMove.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/SuperCommanderTorpedo.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/UnableToComply.wav']),
    ('pytrek/resources/sounds', ['pytrek/resources/sounds/Warp.wav']),

    ('pytrek/resources', ['pytrek/resources/loggingConfiguration.json']),
]
OPTIONS = {}

setup(
    name='PyTrek',
    version=VERSION,
    app=APP,
    data_files=DATA_FILES,
    packages=[
        'pytrek',
        'pytrek.engine',
        'pytrek.engine.devices', 'pytrek.engine.futures',
        'pytrek.exceptions',
        'pytrek.gui',
        'pytrek.gui.gamepieces',
        'pytrek.gui.gamepieces.base', 'pytrek.gui.gamepieces.commander', 'pytrek.gui.gamepieces.klingon', 'pytrek.gui.gamepieces.supercommander',
        'pytrek.mediators',
        'pytrek.mediators.base',
        'pytrek.model',
        'pytrek.resources',
        'pytrek.resources.fonts', 'pytrek.resources.images', 'pytrek.resources.sounds',
        'pytrek.settings'
    ],
    include_package_data=True,

    url='https://github.com/hasii2011/pytrek',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Yet another classic Star Trek game re-written in Python and Arcade',
    long_description=README,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'arcade~=2.6.17',
        'shapely~=2.0.4',
        'codeallybasic~=1.3.2',
        'dataclass-wizard==0.22.3',
    ]
)
