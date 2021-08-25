from os import path
from setuptools import Extension, setup

def read_md(file_path):
    with open(file_path, "r") as f:
        return f.read()

setup(name='gen_text_images',
      version='0.0.7',
      description='Generate images of text in different fonts',
      long_description= "" if not path.isfile("README.md") else read_md('README.md'),
      author="Taylor Archibald",
      author_email='taholr@gmail.com',
      url='https://github.com/tahlor/text_generation',
      setup_requires=[],
      tests_require=[],
      install_requires=[
          "numpy", "scipy", "opencv-python", "matplotlib", "pillow"
      ],
      license=['MIT'],
      packages=['gen_text_images'],
      scripts=[],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Operating System :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
     )
