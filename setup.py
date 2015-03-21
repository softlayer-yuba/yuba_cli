from setuptools import setup

setup(
    name='yuba_cli',
    version='0.1.0',
    py_modules=['yuba'],
    install_requires = [
        'Click',
        'SoftLayer',
        'pyYAML',
    ],
    entry_points = '''
        [console_scripts]
        yuba=yuba:cli
    '''
)
