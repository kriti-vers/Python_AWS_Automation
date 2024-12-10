import boto3
import datetime

# Create the Cost Explorer client
ce = boto3.client('ce')

# Set parameters for cost analysis (e.g., cost for the last month)
start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).date().strftime('%Y-%m-%d')
end_date = datetime.datetime.utcnow().date().strftime('%Y-%m-%d')

# Fetch cost data from AWS Cost Explorer
response = ce.get_cost_and_usage(
    TimePeriod={'Start': start_date, 'End': end_date},
    Granularity='MONTHLY',
    Metrics=['AmortizedCost']
)

# Process and print cost data
for result in response['ResultsByTime']:
    print(f"Cost for {result['TimePeriod']['Start']} - {result['TimePeriod']['End']}:")
    for group in result['Groups']:
        print(f"  {group['Keys'][0]}: {group['Metrics']['AmortizedCost']['Amount']} USD")

