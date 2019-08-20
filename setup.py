from distutils.core import setup

NAME = 'elasticsearch-nvidia-metrics'

setup(
    name=NAME,
    version='1.0.7',
    packages=[NAME,],
    license='apache2',
    long_description=open('README').read(),
    install_requires=[
        'elasticsearch>=7.0.0,<8.0.0',
    ],
    url='https://github.com/wesparish/' + NAME,
    author='Wes Parish',
    author_email='wes@elastiscale.net',
    scripts=['elasticsearch-nvidia-metrics/elasticsearch-nvidia-metrics.py'],
)
