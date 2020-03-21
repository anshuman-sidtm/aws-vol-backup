from setuptools import setup

setup(
	name='snapshotanalyzer-3000',
	version='0.1',
	author="Anshuman",
	author_email="anshumansen.sitm@gmail.com",
	description="snapshotanalyzer-3000 is a tool that automates snapshot on aws",
	license="GNU 3.0",
	packages=['shotty'],
	url='https://github.com/anshuman-sidtm/aws-vol-backup',
	install_requires=[
		'click',
		'boto3',
	],
	entry_points='''
		[console_scripts]
		shotty=shotty.shotty:cli
	''',

	)