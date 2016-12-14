from setuptools import find_packages, setup

install_requires = [
    'Django>=1.8',
    'attrs',
    'djangorestframework>=3,<4',
    'requests>=2.7',
    'six>=1.1',
]

docs_require = [
    'sphinx>=1.4.0',
]

tests_require = [
    'freezegun==0.3.8',
    'pretend==1.0.8',
    'pytest-cov==2.4.0',
    'pytest-django==3.1.2',
    'pytest==3.0.5',
    'requests-mock==1.1.0',

    # Linting
    'isort==4.2.5',
    'flake8==3.0.3',
    'flake8-blind-except==0.1.1',
    'flake8-debugger==1.4.0',
]

setup(
    name='django-postcode-lookup',
    version='0.2.0',
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
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
)
