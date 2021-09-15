import setuptools


with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="my-target-api",
    version="1.0.0",
    description="MyTarget API Wrappers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SharafutdinovRuslan/my_target_api",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"my_target_api": "my_target_api"},
    packages=["my_target_api"],
    python_requires=">=3.6",
)
