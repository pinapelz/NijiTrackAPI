"""
Flask app for serving the static files
"""
from flask import Flask, jsonify, abort, request

from sql_handler import SQLHandler
import fileutil as fs
import response as res
import datetime
app = Flask(__name__)

"""
API endpoint for querying the database for a specific channel_id and iso_date
Returns the subcount closest to the iso_date
"""

from flask import Flask, jsonify, abort
from sql_handler import SQLHandler
import fileutil as fs
import response as res

app = Flask(__name__)

@app.route('/subs/<channel_id>')
def hist_subs(channel_id):
    iso_date = request.args.get('date')
    if iso_date is None:
        iso_date = datetime.datetime.now().isoformat()
    hostname, username, password, database = fs.get_login()
    server = SQLHandler(hostname, username, password, database)
    try:
        data = server.get_subcount("channel_"+channel_id+"_subscriber_data", iso_date)
        response = res.subs_historical_response(channel_id, data)
    except TypeError:
        abort(404, description="No data found for your query")
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

@app.route('/rank/list')
def rank_list():
    hostname, username, password, database = fs.get_login()
    server = SQLHandler(hostname, username, password, database)
    rank_data = server.get_rank_list()
    if rank_data is None:
        abort(404, description="No data found for the given channel.")
    response = res.rank_list_response(rank_data)
    return jsonify(response)

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404

if __name__ == '__main__':
    app.run(debug=True)
