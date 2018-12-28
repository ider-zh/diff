import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# typing library was introduced as a core module in version 3.5.0
if sys.version_info < (3, 5):
    requires = ["typing"]
else:
    requires = []

setup(
    name='deep_diff',
    version='0.0.1',
    packages=['deep_diff'],
    url='http://github.com/hsolbrig/dict_compare',
    license='BSD 3-Clause license',
    author='ider',
    author_email='326737833@qq.com',
    description='a tool to diff dict list set data',
    long_description='a tool to diff dict list set data'
                     'output like the npm package [deep_diff](https://www.npmjs.com/package/deep-diff)',
    requires=requires,
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only']
)