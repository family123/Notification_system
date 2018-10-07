#!/usr/bin/env python3
import email
import os
import sys
import time
import smtplib
import email.utils
from email.mime.text import MIMEText

import requests
from flask import Flask, jsonify, request

from config import config

app = Flask(__name__)

# key = job_seeker_id, value = (recruiter_name, applied_job_id)
job_seeker = {}

counter = 0

recruiter_data_storage = {}
recruiter_data_storage['data'] = {}

jobSeeker_data_storage = {}
jobSeeker_data_storage['data'] = {}

job_status = {}
job_status['data'] = {}


port1 = sys.argv[1]


# For only testing, use pkill python and restart notifications_worker_start to clean all instances
@app.route('/clear', methods=['GET'])
def clear():
    jobSeeker_data_storage['data'] = {}
    recruiter_data_storage['data'] = {}
    empty = {}
    return jsonify(empty)


@app.route('/getRecruiter/<name>', methods=['GET'])
def getRecruiter(name):
    print("Process {}".format(os.getpid()))
    return jsonify(recruiter_data_storage['data'].get(name, {}))


@app.route('/getAllJobs/', methods=['GET'])
def getAllJobs():
    print("Process {}".format(os.getpid()))
    return jsonify(recruiter_data_storage.items())


@app.route('/getJobSeeker/<name>', methods=['GET'])
def getJobSeeker(name):
    print("Process {}".format(os.getpid()))
    return jsonify(jobSeeker_data_storage['data'].get(name, {}))


def jobStatus(job,status):
    msg = MIMEText("Hi User status of your " + str(job) + "changed to " + str(status))
    msg['To'] = email.utils.formataddr(('Recipient', 'recipient@example.com'))
    msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
    msg['Subject'] = 'Simple test message'
    return msg


def sendMail(job):
    msg = MIMEText("Hi User you applied to ", str(job))
    msg['To'] = email.utils.formataddr(('Recipient', 'recipient@example.com'))
    msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
    msg['Subject'] = 'Simple test message'
    return msg


@app.route('/applyJob/<name>', methods=['GET', 'POST'])
def applyJob(name):
    global jobSeeker_data_storage
    jobSeeker_data_storage['data'][name] = jobSeeker_data_storage['data'].get(name, {})
    job = request.args.get('value') or float('nan')
    jobSeeker_data_storage['data'][name]['value'] = job
    jobSeeker_data_storage['data'][name]['time'] = time.time()
    # send mail
    # print("job is-------\n", job)
    server = smtplib.SMTP('127.0.0.1', 11000)
    msg = sendMail(job).as_string()
    server.sendmail('author@example.com', ['recipient@example.com'], msg)
    print("---- sent mail-----")
    return jsonify(jobSeeker_data_storage)


@app.route('/change_job_status/<name>', methods=['GET', 'POST'])
def change_job_status(name):
    global job_status
    job = job_status['data'].get(name, {})
    job_status['data'][name] = job
    status = request.args.get('value') or float('nan')
    job_status['data'][name]['value'] = status
    job_status['data'][name]['time'] = time.time()
    # send mail
    # print("job is-------\n", job)
    server = smtplib.SMTP('127.0.0.1', 11000)
    msg = jobStatus(job, status).as_string()
    server.sendmail('author@example.com', ['recipient@example.com'], msg)
    print("---- sent mail-----")
    return jsonify(jobSeeker_data_storage)


# http://localhost:5000/change_status/job?value=status
@app.route('/change_status/<name>', methods=['GET', 'POST'])
def change_status(name):
    global job_status
    job_status['data'][name] = job_status['data'].get(name, {})
    job_status['data'][name]['value'] = request.args.get('value') or float('nan')
    job_status['data'][name]['time'] = time.time()

    for x in range(4):
        ip, port = config['hosts'][x]
        if str(port) == str(port1):
            print("Host ip Address {} and port is {}".format(ip, port))
            continue
        try:
            r = requests.get(
                'http://{}:{}/change_job_status/{}?value={}'.format(ip, port, name, request.args.get('value') or float('nan')))
            print("Sync Status on {} is {}".format(port, r.status_code))
        except Exception as e:
            print(str(e))
    return jsonify(recruiter_data_storage['data'].get(name, {}))


@app.route('/addJob/<name>', methods=['GET', 'POST'])
def addJob(name):
    global recruiter_data_storage
    recruiter_data_storage['data'][name] = recruiter_data_storage['data'].get(name, {})
    recruiter_data_storage['data'][name]['value'] = request.args.get('value') or float('nan')
    recruiter_data_storage['data'][name]['time'] = time.time()
    return jsonify(recruiter_data_storage)


# http://localhost:5000/recruiter/recruiter_name?value=job_name
@app.route('/recruiter/<name>', methods=['GET', 'POST'])
def recruiter(name):
    global recruiter_data_storage
    recruiter_data_storage['data'][name] = recruiter_data_storage['data'].get(name, {})
    recruiter_data_storage['data'][name]['value'] = request.args.get('value') or float('nan')
    recruiter_data_storage['data'][name]['time'] = time.time()
    for x in range(4):
        ip, port = config['hosts'][x]
        if str(port) == str(port1):
            print("Host ip Address {} and port is {}".format(ip, port))
            continue
        try:
            r = requests.get(
                'http://{}:{}/addJob/{}?value={}'.format(ip, port, name, request.args.get('value') or float('nan')))
            print("Sync Status on {} is {}".format(port, r.status_code))
        except Exception as e:
            print(str(e))
    return jsonify(recruiter_data_storage['data'].get(name, {}))


# http://localhost:5000/jobSeeker/jobSeeker_name?value=job_name
@app.route('/jobSeeker/<name>', methods=['GET', 'POST'])
def jobSeeker(name):
    global jobSeeker_data_storage
    jobSeeker_data_storage['data'][name] = jobSeeker_data_storage['data'].get(name, {})
    jobSeeker_data_storage['data'][name]['value'] = request.args.get('value') or float('nan')
    jobSeeker_data_storage['data'][name]['time'] = time.time()

    for x in range(4):
        ip, port = config['hosts'][x]
        if str(port) == str(port1):
            print("Host ip Address {} and port is {}".format(ip, port))
            continue
        try:
            r = requests.get(
                'http://{}:{}/applyJob/{}?value={}'.format(ip, port, name, request.args.get('value') or float('nan')))
            print("Sync Status on {} is {}".format(port, r.status_code))
        except Exception as e:
            print(str(e))
    return jsonify(jobSeeker_data_storage['data'].get(name, {}))


if __name__ == '__main__':
    app.run(port=sys.argv[1])
