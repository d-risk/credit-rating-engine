from setuptools import setup, find_packages


def _license():
    with open('LICENSE') as f:
        return f.read()


def _readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='credit-rating-engine',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='https://github.com/d-risk/credit-rating-engine',
    license=_license(),
    author='Christopher Zhong',
    author_email='1946052+chriszhong@users.noreply.github.com',
    description='D-Risk\'s Credit Rating Engine',
    long_description=_readme(),
    install_requires=['graphene'],
    keywords='api graphene credit rating risk',
    # test_suite='nose.collector',
    # tests_require=['nose'], install_requires=['graphene']
)
