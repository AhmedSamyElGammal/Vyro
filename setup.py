from setuptools import setup, find_packages


setup(
    name='vyro',
    version='0.6.0',
    license='MIT',
    author="AhmedSamyElGammal",
    author_email='elgammala80@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/AhmedSamyElGammal/vyro',
    keywords='math matrix vector linear-algebra',
    install_requires=[]
)