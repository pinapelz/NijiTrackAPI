import datetime
def subs_historical_response(channel_id, data):
    if data.sub_count is  None and data.date is None:
        return {}
    response = {
        "timestamp": data.date,
        "channel_id": channel_id,
        "sub_count": data.sub_count
    }
    return response

def rank_current_response(channel_id, rank, member_count):
    if rank is None:
        return {}
    time_str = datetime.datetime.now().isoformat()
    response = {
        "timestamp": time_str,
        "channel_id": channel_id,
        "rank": rank,
        "member_count": member_count,
    }
    return response

def rank_list_response(rank_data):
    if rank_data is None:
        return {}
    time_str = datetime.datetime.now().isoformat()
    response = {
        "timestamp": time_str,
        "rank_data": rank_data
    }
    return response

