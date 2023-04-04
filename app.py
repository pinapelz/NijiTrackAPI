"""
API endpoint for querying the database for a specific channel_id and iso_date
Returns the subcount closest to the iso_date
"""

from flask import Flask, jsonify, send_from_directory, abort, request
from flask_cors import CORS
from sql_handler import SQLHandler
import fileutil as fs
import response as res

app = Flask(__name__)
CORS(app)


@app.route('/subs/<channel_id>')
def current_subs(channel_id):
    timestamp = request.args.get('date', 'now')
    hostname, username, password, database = fs.get_login()
    server = SQLHandler(hostname, username, password, database)
    if timestamp == "now":
        data = server.get_current_subscriber_count(channel_id)
        response = res.subs_current_response(channel_id, data)
    else:
        table_key = "channel_"+channel_id.lower()+"_subscriber_data"
        table_key = table_key.replace("-", "$")
        data = server.get_subcount(table_key, timestamp)
        response = res. subs_historical_response(channel_id, data)
    if data is None:
        abort(404, description="No data found for the given channel.")
    return jsonify(response)

@app.route('/rank/<channel_id>')
def rank(channel_id):
    hostname, username, password, database = fs.get_login()
    server = SQLHandler(hostname, username, password, database)
    rank_data = server.get_current_rank(channel_id)
    if rank_data is None:
        abort(404, description="No data found for the given channel.")
    response = res.rank_current_response(channel_id, rank_data.rank, rank_data.member_count)
    return jsonify(response)

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404
