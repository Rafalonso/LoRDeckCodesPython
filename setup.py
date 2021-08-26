from setuptools import setup, find_packages


setup(
    name='lor_deckcodes',
    version='4.0.0',
    url='https://github.com/Rafalonso/LoRDeckCodesPython',
    description='Legends of Runeterra deck coder and decoder',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Rafael Alonso',
    maintainer='Rafael Alonso',
    maintainer_email='rafalonso.almeida@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.5',
    install_requires=[
    ],
)
