from flask import Flask, render_template, request, session, url_for, redirect, abort, jsonify
from werkzeug.utils import secure_filename
import time, os, csv
from database import db_connect
from database import db_control




with open('{{url_for('static', filename='csv/')}}', 'rb') as inFile:
    reader = csv.reader(inFile)

    for row in reader:
        print row