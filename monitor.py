import boto3
import datetime as dt

# Create a CloudWatch client
cloudwatch = boto3.client('cloudwatch',region_name='us-east-1')
sns=boto3.client('sns',region_name='us-east-1')
# Set parameters
instance_id = 'i-02d28626e5906a991'  # Replace with your instance ID
threshold = 2  # CPU utilization threshold in percentage
period = 300  # Period in seconds (5 minutes)
start_time = dt.datetime.now() - dt.timedelta(hours=1)
end_time = dt.datetime.now()
sns_topic_arn ='arn:aws:sns:us-east-1:863518425553:send-alerts-cpu-ec2'
# Fetch CPU utilization data from CloudWatch
response = cloudwatch.get_metric_statistics(
    Period=period,
    StartTime=start_time,
    EndTime=end_time,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistics=['Average'],
    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}]
)

print(response)

# Check the average CPU utilization over the past 1 hour
data_points = response['Datapoints']
print(f"Datapoints object:\n{data_points}")
if data_points:
    avg_cpu_utilization = sum([dp['Average'] for dp in data_points]) / len(data_points)
    print(f"Average CPU Utilization for {instance_id}: {avg_cpu_utilization}%")
   
    # Send an alert if CPU utilization is above the threshold
    if avg_cpu_utilization > threshold:
        print(f"Warning: CPU Utilization is {avg_cpu_utilization}% which exceeds the threshold of {threshold}%.")
        sns.publish(
        TopicArn=sns_topic_arn,
        Message=f"Warning: CPU Utilization is {avg_cpu_utilization}% on instance {instance_id}",
        Subject="EC2 Instance High CPU Utilization Alert"
    )

else:
    print("No data found for the specified instance.")

