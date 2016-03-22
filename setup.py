
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '''Implementation of A* path-planning algorithm for
                    Line Segmentation of Manuscript Documents''',
    'author': 'Saverio Meucci',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'My email.',
    'version': '0.1',
    'install_requires': ['none'],
    'packages': ['linesegm'],
    'scripts': [],
    'name': 'LineSegm'
}


setup(**config)
