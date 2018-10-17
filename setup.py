from setuptools import setup

# Use README for the PyPI page
with open('README.md') as f:
    long_description = f.read()

# https://setuptools.readthedocs.io/en/latest/setuptools.html
setup(name='collision',
      author='qwertyquerty',
      url='https://github.com/QwekoDev/collision/',
      version='1.1.2',
      packages=['collision'],
      python_requires='>=2.7',
      platforms=['Windows', 'Linux', 'OSX'],
      zip_safe=True,
      license='MIT',
      description='Collision is a python library meant for collision detection between convex and concave polygons, circles, and points.',
      long_description=long_description,

      long_description_content_type='text/markdown',
      keywords='python collision detection polygon concave convex circle physics game',

)
