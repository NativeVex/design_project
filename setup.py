import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flaskr",
    version="0.0.1",
    author="Artur Janik, Chloe Atchabahian",
    author_email="aj2614@nyu.edu",
    description="Submission for design project, group b23",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NativeVex/design_project",
    project_urls={
        "Production Deployment": "https://design-project-b23.herokuapp.com/",
        "Develop Deployment": "https://design-project-b23-dev.herokuapp.com/",
        "Bug Tracker": "https://github.com/NativeVex/design_project/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src/webapp"},
    package=setuptools.find_packages(where="src/webapp"),
    python_requires=">=3.9",
)
