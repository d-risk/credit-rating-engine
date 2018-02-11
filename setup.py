from setuptools import setup, find_packages


def _license():
    with open('LICENSE') as f:
        return f.read()


def _readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='credit-rating-service',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='https://github.com/d-risk/credit-rating-service',
    license=_license(),
    author='Christopher Zhong',
    author_email='christopher.zhong@d-risk.tech',
    description='D-Risk\'s Credit Rating Service',
    long_description=_readme(),
    install_requires=[
        'graphene',
        'django',
        'graphene_django',
        'django-cors-headers'
    ],
    keywords='api graphene credit rating risk graphql',
    # test_suite='nose.collector',
    # tests_require=['nose'], install_requires=['graphene']
)
