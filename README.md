# LOG8415-FinalProject

This is the final project of LOG8415e class of automn 2022 semester.

## Installation
You just need to make sure you have the following dependencies:
* Python 3
* boto3
* paramiko

Also make sure you have AWS CLI installed and that you update your AWS credentials.

## Set up and benchmark standalone
Make sure you are in the directory that has the python files, then run the following command:

```bash
python3 standalone.py
```
The script will take care of all the set up (security group and standalone instance), then once all is set up and ready it will benchmark the standalone and SCP the benchmark results file to the local machine. Afterwards, the script will end by terminating the standalone and deleting the security group.
## Set up and benchmark cluster

In the process...

## Proxy

In the process...
