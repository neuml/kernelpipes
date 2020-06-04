# pylint: disable = C0111
from setuptools import find_packages, setup

with open("README.md", "r") as f:
    DESCRIPTION = f.read()

setup(name="kernelpipes",
      version="1.0.0",
      author="NeuML",
      description="Kaggle Kernel Pipelines",
      long_description=DESCRIPTION,
      long_description_content_type="text/markdown",
      url="https://github.com/neuml/kernelpipes",
      project_urls={
          "Documentation": "https://github.com/neuml/kernelpipes",
          "Issue Tracker": "https://github.com/neuml/kernelpipes/issues",
          "Source Code": "https://github.com/neuml/kernelpipes",
      },
      license="MIT License: http://opensource.org/licenses/MIT",
      packages=find_packages(where="src/python/"),
      package_dir={"": "src/python/"},
      keywords="python machine-learning kaggle",
      python_requires=">=3.6",
      entry_points={
          "console_scripts": [
              "kernelpipes = kernelpipes.execute:main",
          ],
      },
      install_requires=[
          "kaggle>=1.5.6",
          "PyYAML>=5.3"
      ],
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development",
          "Topic :: Utilities"
      ])
