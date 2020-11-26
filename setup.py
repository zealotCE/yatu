import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    lines = [line.strip() for line in f]
    requirements = [line for line in lines if line and not line.startswith('#')]

setup(
    name = 'yatu',
    version = '0.0.1',
    description = 'compress png image with ffmpeg',
    url = 'http://github.com/zealotCE/yatu',
    author = 'cec_ce',
    author_email = 'zealotce@gmail.com',
    license = 'MIT',
    keywords = ('yatu', 'yatu, image compression'),
    packages = find_packages(),
    platforms = 'any',
    zip_safe = False,
    python_requires = '!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, >=3.4.*',
    install_requires = requirements,
    entry_points = {
        'console_scripts': [
            'yatu=image_compres\palette_ffmpeg:main'
        ]
    }
)

