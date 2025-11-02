import json

def search_rain_data(json_file, region=None, start_date=None, end_date=None, season=None):
    with open(json_file, "r") as file:
        data = json.load(file)
    results = []
    if region == '': region = None
    if start_date == '': start_date = None
    if end_date == '': end_date = None
    if season == '': season = None
    for i in data:
        cond_start = (start_date is None or start_date <= i.get("date", ""))
        cond_end = (end_date is None or end_date >= i.get("date", ""))
        cond_season = (season is None or season == i.get("season", ""))
        cond_region = (region is None or region == i.get("region", ""))
        if cond_start and cond_end and cond_season and cond_region:
            results.append(i)
    return results

def search_water_data(json_file, region=None, res_type=None, status=None):
    with open(json_file, "r") as file:
        data = json.load(file)
    results = []
    if region == '': region = None
    if res_type == '': res_type = None
    if status == '': status = None
    for i in data:
        cond_region = (region is None or region == i.get("region", ""))
        cond_res_type = (res_type is None or res_type == i.get("type", ""))
        cond_status = (status is None or status == i.get("status", ""))
        if cond_region and cond_res_type and cond_status:
            results.append(i)
    print(results)
    return results

'''
from datetime import datetime
start_date =input("Enter the start date: ")or None
end_date =input("Enter the end date: ")or None
season=input("Enter the season: ") or None
region=input("Enter the reg ion: ")or None
if start_date is not None:
    date_start = datetime.strptime(start_date, "%Y-%m-%d")
else:
    date_start = start_date
if end_date is not None:
    date_end=datetime.strptime(end_date, "%Y-%m-%d")
else:
    date_end = end_date
with open(os.getcwd()+'\\'+'weather_data.json', 'r') as f:
    b=json.load(f)
    if start_date is None and end_date is None and season is None and region is None:
        print(f)
    else:
        for i in range(len(dates)):
            cond_start = (date_start is None or date_start <= datetime.strptime(dates[i], "%Y-%m-%d"))
            cond_end = (date_end is None or date_end >= datetime.strptime(dates[i], "%Y-%m-%d"))
            cond_season = (season is None or season == season_[i])
            cond_region = (region is None or region == region_[i])

            if cond_start and cond_end and cond_season and cond_region:
                print(record_id[i], dates[i], season_[i], region_[i], rainfall_[i])
f.close()'''

'''def search_rain_data(json_file, region=None, start_date=None, end_date=None, season=None):
    with open(json_file, "r") as file:
        data = json.load(file)
    results = []
    for i in data:
        cond_start = (start_date is None or start_date <= i.get("date", ""))
        cond_end = (end_date is None or end_date >= i.get("date", ""))
        cond_season = (season is None or season == i.get("season", ""))
        cond_region = (region is None or region == i.get("region", ""))
        if cond_start and cond_end and cond_season and cond_region:
            results.append(i)
    return results'''

'''
def search_rain_data(json_file, region=None, start_date=None, end_date=None, season=None):
    with open(json_file, "r") as file:
        data = json.load(file)
    results = []
    for record in data:
        if region and region.lower() not in record.get("region", "").lower():
            continue
        if season and season.lower() not in record.get("season", "").lower():
            continue
        if start_date and record.get("date") < start_date:
            continue
        if end_date and record.get("date") > end_date:
            continue
        results.append(record)
    return results
'''