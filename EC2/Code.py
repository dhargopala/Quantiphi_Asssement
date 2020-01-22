import boto3
from time import sleep
region = 'us-east-1'
instances = 'i-01f0853da7100b211'

ec2 = boto3.client('ec2', region_name=region)
ec2res = boto3.resource('ec2', region_name=region)

#---------------------To Start--------------------
ec2.start_instances(InstanceIds=[instances])
print('started your instances: ' + str(instances))

#time.sleep(300)

#---------------------To Create Snapshot--------------------
instance = ec2res.Instance(instances)
volumes = instance.volumes.all()



for v in volumes:
    print("Your volume-id is: " + v.id)
    volumes_dict = {
                  'gopala-snap-1' : v.id,                      
          }

print(volumes_dict)
successful_snapshots = dict()

for snapshot in volumes_dict:
    try:
        response = ec2.create_snapshot(
            Description= snapshot,
            VolumeId= volumes_dict[snapshot],
            DryRun= False
        )
        # response is a dictionary containing ResponseMetadata and SnapshotId
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        snapshot_id = response['SnapshotId']
        # check if status_code was 200 or not to ensure the snapshot was created successfully
        if status_code == 200:
            successful_snapshots[snapshot] = snapshot_id
    except Exception as e:
        exception_message = "There was error in creating snapshot " + snapshot + " with volume id "+volumes_dict[snapshot]+" and error is: \n"\
                            + str(e)
# print the snapshots which were created successfully
print(successful_snapshots)          

#time.sleep(300)

#---------------------To Stop---------------------
ec2.stop_instances(InstanceIds=[instances])
print('stopped your instances: ' + str(instances))

#time.sleep(300)

#---------------------To Terminate----------------

'''ec2.terminate_instances(InstanceIds=instances)
print('terminated your instances: ' + str(instances))'''

