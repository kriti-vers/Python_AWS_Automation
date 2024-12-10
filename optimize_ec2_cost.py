import boto3
import datetime

# Create EC2 and CloudWatch clients
ec2 = boto3.client('ec2',region_name='us-east-1')
cloudwatch = boto3.client('cloudwatch',region_name='us-east-1')

# Set parameters
cpu_threshold = 10  # CPU utilization threshold
start_time = datetime.datetime.now() - datetime.timedelta(days=7)
end_time = datetime.datetime.now()

# Describe EC2 instances
response = ec2.describe_instances()

# Iterate through instances and check their CPU utilization
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        print(f"Checking CPU utilization for instance {instance_id}")

        # Fetch CPU utilization from CloudWatch
        cpu_response = cloudwatch.get_metric_statistics(
            Period=86400,  # 1-day period
            StartTime=start_time,
            EndTime=end_time,
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Statistics=['Average'],
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}]
        )

        data_points = cpu_response['Datapoints']
        if data_points:
            avg_cpu_utilization = sum([dp['Average'] for dp in data_points]) / len(data_points)
            print(f"Average CPU Utilization for {instance_id}: {avg_cpu_utilization}%")

            # Flag underutilized instances
            if avg_cpu_utilization < cpu_threshold:
                print(f"Instance {instance_id} is underutilized (CPU: {avg_cpu_utilization}%)")
        else:
            print(f"No CPU data available for instance {instance_id}")

