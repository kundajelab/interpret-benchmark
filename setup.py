from distutils.core import setup

if __name__== '__main__':
    setup(include_package_data=True,
          description='Vaastav',
          long_description="""Simulate genomic sequences based on real data""",
          url='https://github.com/kundajelab/interpret-benchmark',
          version='0.1.0.0',
          packages=['vaastav',
                    'vaastav.util'],
          setup_requires=[],
          install_requires=['numpy>=1.9'],
          scripts=[],
          name='vaastav')
