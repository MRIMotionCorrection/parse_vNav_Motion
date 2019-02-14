from setuptools import setup

setup(name='vnav',
    version='0.1',
    description='Script to parse DICOM files from a vNav series and convert them into motion scores',
    url='https://github.com/MRIMotionCorrection/parse_vNav_Motion',
    author='Dylan Tisdall',
    author_email='mtisdall@mail.med.upenn.edu',
    license='MIT',
    packages=['vnav'],
    install_requires=['pydicom', 'numpy'])
