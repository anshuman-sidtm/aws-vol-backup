# aws-vol-backup
AWS management and backup automation tool using Python with boto

#About
Listing AWS EC2 instances using Boto3. Uses AWS IAM users with programatic access

#running
``pipenv run python shotty\shotty.py instances start --project Projectname`` to start
``pipenv run python shotty\shotty.py instances stop --project Projectname `` to stop
``pipenv run python shotty\shotty.py instances list --project Projectname `` to list
``pipenv run python shotty\shotty.py volumes list --project Projectname `` to list volumes
``pipenv run python shotty\shotty.py snapshots list --project Projectname `` to list snapshot
``pipenv run python shotty\shotty.py instances snapshot --project Projectname `` to create snapshot
