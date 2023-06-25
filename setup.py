from setuptools import setup

with open("./README.md", "r") as f:
   ld = f.read()

setup(
   name='zingmp3py',
   version="0.3.2",
   long_description=ld,
   long_description_content_type='text/markdown',
   description='A light weight Python library for the ZingMp3 API',
   author='The DT',
   author_email='duongtuan30306@gmail.com',
   packages=["zingmp3py"],
   install_requires=["aiohttp", "requests"]
)