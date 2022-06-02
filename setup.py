from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='vyro',
    version='1.2.3',
    description='It is a mathematical repo to deal with Linear algebra stuff like Matrices and Vectors.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author="AhmedSamyElGammal",
    author_email='elgammala80@gmail.com',
    # packages=find_packages('src'),
    # package_dir={'': 'src'},
    url='https://github.com/AhmedSamyElGammal/vyro',
    keywords=['math', 'matrix', 'vector', 'linear algebra', 'machine learning'],
    install_requires=[]
)
