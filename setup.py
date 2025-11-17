from setuptools import setup, find_packages

with open("README.md", "r") as fh:
      long_description = fh.read()

setup(name='discopy-data-rknaebel',
      version='1.0.2',
      description='Data and Structures for Neural Discourse Parsing',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/rknaebel/discopy-data',
      author='Rene Knaebel',
      author_email='rene.knaebel@uni-potsdam.de',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'joblib==1.1.0',
            'numpy>=1.18.0',
            'nltk>=3.4',
            'pandas==1.3.5',
            'pybtex==0.24.0',
            'supar==1.1.1',
            'trankit @ git+https://github.com/nlp-uoregon/trankit.git'
      ],
      zip_safe=False,
      entry_points={
            'console_scripts': [
                  'discopy-tokenize=discopy_data.cli.tokenize_text:main',
                  'discopy-add-annotations=discopy_data.cli.add_annotations:main',
                  'discopy-extract=discopy_data.cli.extract:main',
                  'discopy-add-parses=discopy_data.cli.update_parses:main',
            ],
      },
      python_requires='>=3.7',
      )
