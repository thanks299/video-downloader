#!/usr/bin/env python3

import os
from flask import Flask, render_template, request, send_file, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from tasks import download_video_task
from celery.result import AsyncResult
from datetime import datetime
from celery import Celery

app = Flask(__name__)
# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://thanks_user:SUqAdiGsyBeWKxBqAp5XUa7YQm5TyGi3@dpg-cs2game8ii6s739hq440-a.oregon-postgres.render.com/thanks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = 'rediss://red-crtcjbm8ii6s73eklv9g:nmPZdC7Q687jOBftyHMVtezZX7PLWNCh@oregon-redis.render.com:6379'
app.config['CELERY_RESULT_BACKEND'] = 'postgresql://thanks_user:SUqAdiGsyBeWKxBqAp5XUa7YQm5TyGi3@dpg-cs2game8ii6s739hq440-a.oregon-postgres.render.com/thanks'

db = SQLAlchemy(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery

# Define a model for download history


celery = make_celery(app)


class DownloadHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    format_choice = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Initialize the database
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     url = request.form.get('url')
    #     format_choice = request.form.get('format')
    #     if url and format_choice:
    #         # Call the background task
    #         task = download_video_task.delay(url, format_choice)
    #         return
    return render_template('index.html')


@app.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    print(task_id)
    task = download_video_task.AsyncResult(task_id)

    try:
        # timeout is optional, here it's 300 seconds
        result = task.get(timeout=300)
        print(f"Task completed! File name: {result}")

    except Exception as e:
        print(f"Task failed with error: {e}")

    return send_file(f"{result}", as_attachment=True)
    # return {"status": "downloaded"}


@app.route('/history', methods=['GET'])
def history():
    # Fetch the download history from the database
    downloads = DownloadHistory.query.order_by(
        DownloadHistory.timestamp.desc()).all()
    return render_template('history.html', downloads=downloads)


@app.route('/download-video', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')
    format_url = data.get("format")

    print(data)
    if not video_url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400

    # Initiate Celery task to download the video
    task = download_video_task.apply_async(args=(video_url, format_url))

    print(task)

    return jsonify({'success': True, 'task_id': task.id})


if __name__ == '__main__':
    app.run(debug=True, port=7000)
