# from setuptools import setup, find_packages
#
# setup(
#     # Basic project info
#     name="kitsunari-cli",  # Name when installed
#     version="0.1.0",  # Current version
#     description="Project Kitsunari - A command-line anime streaming tool",
#     author="Xeon",  # Your name
#     author_email="XeonXE1@proton.me",  # Your email
#
#     # Package structure
#     packages=find_packages(where="src"),  # Find all packages in src/
#     package_dir={"": "src"},  # Root package directory
#
#     # Dependencies (same as requirements.txt)
#     install_requires=[
#         "requests>=2.31.0",
#         "beautifulsoup4>=4.12.0",
#         "click>=8.1.0",
#         "rich>=13.0.0",
#         "fuzzywuzzy>=0.18.0",
#         "python-levenshtein>=0.21.0",
#         "lxml>=4.9.0",
#     ],
#
#     # Command-line scripts
#     entry_points={
#         "console_scripts": [
#             "kitsunari=kitsunari_cli.main:main",  # Creates 'kitsunari' command
#         ],
#     },
#
#     # Python version requirement
#     python_requires=">=3.8",
#
#     # Project metadata
#     classifiers=[
#         "Development Status :: 3 - Alpha",
#         "Intended Audience :: End Users/Desktop",
#         "Programming Language :: Python :: 3",
#         "Topic :: Multimedia :: Video",
#     ],
# )