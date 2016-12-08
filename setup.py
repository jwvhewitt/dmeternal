from setuptools import setup, find_packages


setup(  name='dmeternal',
        version='0.5.0',
        py_modules=['main',],
        packages=find_packages(),
        package_data={
            '': ['*.txt','*.png','*.cfg','*.ttf'],
            'game': ['data/*.txt','data/*.cfg','image/*.png','image/*.ttf',
                'image/*.otf']
        },
        entry_points={
            'gui_scripts': [
                'dmeternal = main:play_the_game',
            ]
        },
        install_requires= [
            'Pygame',
        ],

      )
