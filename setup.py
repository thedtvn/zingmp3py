from setuptools import setup

setup(
   name='zingmp3py',
   version="0.3.0",
   description='A light weight Python library for the ZingMp3 API',
   author='The DT',
   author_email='duongtuan30306@gmail.com',
   packages=["zingmp3py"],
   install_requires=["aiohttp", "requests"]
)