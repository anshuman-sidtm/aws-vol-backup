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

if __name__ == '__main__':
	instances()
	
	