from setuptools import setup

setup(
    name='packages',
    version='0.1',
    description='AI based telegram bot',
    author='Coding Destro',
    author_email='codingdestro@gmail.com',
    packages=['internal', 'models', 'app', 'plugins', 'functions'],
    install_requires=[
        'tortoise-orm',
        'aiogram',
        'requests',
        'python-dotenv',
        'beautifulsoup4',
    ],
)