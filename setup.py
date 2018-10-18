from setuptools import setup

setup(
    name='get_fshare',
    version='2.1.4',
    description='Python lib to get link Fshare.vn',
    url='http://github.com/tudoanh/get_fshare',
    author='Do Anh Tu',
    author_email='tu0703@gmail.com',
    license='MIT',
    install_requires=['requests>=2.18.1', 'lxml>=3.8.0'],
    packages=['get_fshare'],
    zip_safe=False,
    python_requires='>=3.5',
)
