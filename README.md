# Notification_system
# Mail Notifictaion system for jobSeeker and recruiter
 
Prerequisites:
1. Install flask, python, virtualenv and requests before running notifications_worker.py:

On Mac:

sudo easy_install flask python virtualenv requests

On Linux:

sudo apt-get update

sudo apt-get upgrade -y

sudo apt-get install flask python virtualenv requests

2. Check versions to see if everything is installed properly:

python --version

virtualenv --version

flask --version

requests --version

3. Download the repo, unzip it and cd into Notification_system directory:

github link [] 

4. Make the notifications_worker_start as executable:

sudo chmod 777 notifications_worker_start

5. Run the script(notifications_worker_start):
    ./notifications_worker_start

6. run the server.py(for sending mails)


7. The script will start 4 nodes on following ports:
 
   5000, 4000, 3000, 2000

7. Supported app routes:

    a. http://localhost:5000/jobSeeker/jobSeeker_name?value=job_name
    
    b. http://localhost:5000/recruiter/recruiter_name?value=job_name
    
    c. http://localhost:5000/change_status/job?value=status
    
    d. http://localhost:5000/getRecruiter/
    
    e. http://localhost:5000/getAllJobs/
    
    f. http://localhost:5000/getJobSeeker/

8. The data will be returned in Json format:

[["data",{"recruiter2":{"time":1538916779.058705,"value":"job2"},
    "recruiter3":{"time":1538916787.281017,"value":"job3"}}]]

9. The time represent the exact time when the job is being added to the system, if in future same job is vacant by hitting the api job opening time will get changed.


11. Run "pkill python" on cmd before restarting.

Assumptions:

- Assuming recruiter can change only one job.
- job change api is manual no validation is being done currently.

TODO:

- Need to add functionality where a recruiter can add multiple jobs
- Need to add the validation for the recruiter can change only it's added job status.






