from setuptools import setup, find_packages

setup(name='whitelabel_automator',
      version='0.1',
      description='Automatically pull new Whitelabel Release and upload to buffer',
      classifiers=[
        'Programming Language :: Python :: 2.7'
      ],
      author='Andy Gu',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'console_scripts': ['whitelabel_automator=whitelabel_automator.whitelabel_automator:main'],
      }
)

