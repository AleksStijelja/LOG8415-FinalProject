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

To test the proxy, you should run the cluster first with the command above, and not type the 'terminate' in the terminate once the message comes up. That way we will have the master and its 3 slaves running. Once that done, run the following command to set up the proxy instance:
```bash
python3 .\proxy_setup.py "subnet-XXXXXXXXXXXXXXXXX"
```
Again, make sure to put the (172.31.16.0/20) subnet in double quotes as argument in the command as we want the proxy to be in same subnet as the cluster.  <br /> <br />

Regarding the strategies that were tasked to implement, unfortunately I was only able to make the direct hit work, as the other two were riddled with connection problems to the nodes. Due to time constraints (I started this project on the 16th of december after the final exam), I wasn't able to debug the problems. <br />

Direct hit is very straightfoward. It simply means the proxy will always target the master node to send queries. <br />

After the proxy instance is all set up, the script will scp your "labsuser.pem" file into the proxy. Once you get the 'Ready!' message on the terminal, you can SSH into the proxy. Once in the proxy, git clone this git repo, then copy the proxy.py script from the repo into ~, where the labsuser.pem key is, such as this:
```bash
cp LOG8415-FinalProject/proxy.py ~
```
Make sure to chmod 400 labuser.pem <br /> 

The you can run the proxy. Make sure to put in the command the SQL query in double quotes, like this:
```bash
python3 proxy.py "SQL QUERY" >> results.txt 
```
All prints from the proxy will be sent to the results.txt file for cleanliness. To test that we can actually get and write into the sakila db you can run the following commands:

```bash
python3 proxy.py "SELECT * FROM actor" >> results.txt 
python3 proxy.py "INSERT INTO actor VALUES (999,'DOE','JOHN','1999-06-30 09:09:09')" >> results.txt 
python3 proxy.py "SELECT * FROM actor" >> results.txt 
```
After running these 3 commands, you can ```nano results.txt```, you will see at first see a list of 200 values of actors, then the 2nd command will write a new John Doe actor at key 999, and you will see a 2nd list in results.txt where at the bottom you will see the newly added 201th element.

