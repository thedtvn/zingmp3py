from setuptools import setup

setup(
   name='zingmp3',
   version="0.1.0",
   description='Raw JSON ZingMp3 API Client Support for Sync and Async',
   author='The DT',
   author_email='duongtuan30306@gmail.com',
   packages=["zingmp3"],
   install_requires=["aiohttp", "requests"]
)