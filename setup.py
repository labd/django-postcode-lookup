from setuptools import find_packages, setup

install_requires = [
    'Django>=3.2,<4',
    'attrs',
    'djangorestframework>=3,<4',
    'requests>=2.7',
]

docs_require = [
    'sphinx>=1.5.2',
]

tests_require = [
    'freezegun==1.1.0',
    'pretend==1.0.9',
    "pytest-cov==2.11.1",
    "pytest-django==4.1.0",
    "pytest==6.1.2",
    "requests-mock==1.8.0",
    "coverage==5.3",

    # Linting
    "isort<5",
    "flake8==3.8.4",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==3.2.1",
]

setup(
    name='django-postcode-lookup',
    version='1.0',
    description="Pluggable postcode lookup endpoint",
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/labd/django-postcode-lookup',
    author="Michael van Tellingen",
    author_email="michaelvantellingen@gmail.com",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'docs': docs_require,
        'test': tests_require,
    },
    entry_points={},
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    zip_safe=False,
)
