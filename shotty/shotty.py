import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_intances(project):
	instances = []
	if project:
		filters = [{'Name':'tag:name', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()
	return instances

@click.group()
def cli():
	"""Shotty managed Snapshot"""

@cli.group('volumes')
def volumes():
	"""commands for volumes"""
@volumes.command('list')
@click.option('--project', default=None,
              help="Only Volumes for project (tag Project:<name>")
def list_instances(project): 
	"List Instances"
	instances = filter_intances(project)

	for i in instances:
		for v in i.volumes.all():
			print(', '.join((
				v.id,
				i.id,
				v.availability_zone,
				v.encrypted and "Encrypted" or "Not Encrypted",
				str(v.state),
				str(v.size) + ' Gigbit',
				)))

	return

@cli.group('snapshot')
def snapshot():
	"""commands for Snapshot"""
@snapshot.command('list')
@click.option('--project', default=None,
              help="Only Volumes for project (tag Project:<name>")
def list_instances(project): 
	"List Instances"
	instances = filter_intances(project)

	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(', '.join((
					s.id,
					v.id,
					i.id,
					s.progress,
					s.description,
					s.encrypted and "Encrypted" or "Not Encrypted",
					s.start_time.strftime("%c")
					)))

	return

@cli.group('instances')
def instances():
	"""commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
              help="Only Instances for project (tag Project:<name>")
def list_instances(project): 
	"List Instances"
	instances = filter_intances(project)

	for i in instances:
		tags = { t['Key']: t['Value'] for t in i.tags or [] }
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('name','<no project>')
			)))

	return
@instances.command('stop')
@click.option('--project', default=None,
              help="Only Instances for project (tag Project:<name>")
def stop_instance(project):
	"Stop Ec2 Instance"
	instances = filter_intances(project)

	for i in instances:
		print('stopping {0}....' .format(i.id))
		i.stop()

@instances.command('start')
@click.option('--project', default=None,
              help="Only Instances for project (tag Project:<name>")
def start_instance(project):
	"Start Ec2 Instance"
	instances = filter_intances(project)

	for i in instances:
		print('starting {0}....' .format(i.id))
		i.start()

@instances.command('snapshot',
	help='create snapshot of all instances')
@click.option('--project', default=None,
              help="Create Snapshot of Instance by tag")
def snapshot_instance(project):
	"Start Ec2 Instance"
	instances = filter_intances(project)

	for i in instances:
		for v in i.volumes.all():
			print('Creating Snapshot {0}....' .format(v.id))
			v.create_snapshot(Description ='Created by Snappy')
	return

if __name__ == '__main__':
	cli()
	
	