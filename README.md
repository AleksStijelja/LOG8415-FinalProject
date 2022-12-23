# LOG8415-FinalProject

This is the final project of LOG8415e class of automn 2022 semester.

## Preparation
You just need to make sure you have the following dependencies:
* Python 3
* boto3
* paramiko

Make sure you have AWS CLI installed and that you update your AWS credentials. <br />

Also, take your "labsuser.pem" key and replace the "labsuser.pem" key from the git repo. Obviously don't commit and push the change. We just need your "labsuser.pem" key so we can ssh into instances and scp files as well. Make sure that your "labsuser.pem" key is chmod 400.

## Set up and benchmark standalone
Make sure you are in the directory that has the python files, then run the following command:

```bash
python3 standalone.py "subnet-XXXXXXXXXXXXXXXXX"
```
Make sure to put the (172.31.16.0/20) subnet in double quotes as argument in the command.  <br />
The script will take care of all the set up (security group and standalone instance), then once all is set up and ready it will benchmark the standalone and SCP the benchmark results file to the local machine. Afterwards, the script will end by terminating the standalone and deleting the security group.
## Set up and benchmark cluster
The whole setting up of the MYSQL cluster has been heavily based on the following website: https://www.digitalocean.com/community/tutorials/how-to-create-a-multi-node-mysql-cluster-on-ubuntu-18-04 <br /> <br />
Make sure you are in the directory that has the python files, then run the following command:

```bash
python3 .\cluster.py "subnet-XXXXXXXXXXXXXXXXX"
```
Make sure to put the (172.31.16.0/20) subnet in double quotes as argument in the command since our master and nodes will have private up addresses from this subnet.  <br /> <br />
The script will take care of all the set up (security group and cluster instances), then once all is set up and ready it will benchmark the cluster and SCP the benchmark results file to the local machine. <br /> <br />
Afterwards, you will be presented with the following message on the terminal:
```bash
- Enter 'terminate' to terminate the instances and security group: 
```
Therefore, if you type 'terminate' in the terminal and enter, the script will terminate the cluster instances and then delete the cluster security group. If you type any other words or don't type anything at all the cluster will still be running. This is pertinent for the proxy since we want the cluster still running.

## Proxy

In the process...
