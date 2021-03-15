from setuptools import setup

setup(
    name='task-tracker-api',
    packages=['api'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask_SQLAlchemy'
    ],
)