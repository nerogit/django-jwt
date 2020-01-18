import os.path

from setuptools import find_packages, setup


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
            return f.read()
    except (IOError, OSError):
        pass


version = '0.0.6'

setup(
    name='django-jwt',
    version=version,
    packages=find_packages(exclude=['examples']),
    install_requires=[
        'Django',
        'PyJWT',
    ],
    tests_require=[
        'flake8',
        'pytest',
    ],
    description='Send e-mail, easier',
    long_description=readme(),
    url='https://github.com/dohvis/django-jwt',
    author='Kim Dohyeon',
    author_email='k.dohvis' '@' 'gmail.com',
    license='MIT License',
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Email',
    ]
)
