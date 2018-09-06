from setuptools import setup, find_packages


develop = {
    "cachetools",
    "colorama",
    "flake8",
    "jinja2",
    "ipython",
    "mysqlclient",
    "pytest",
    "requests",
}

if __name__ == "__main__":
    setup(
        name="insights_examples",
        version="0.0.1",
        description="Examples using Insights Core as a framework",
        author_email="csams@redhat.com",
        license="Apache 2",
        packages=find_packages(),
        install_requires=list(develop),
        include_package_data=True,
    )
