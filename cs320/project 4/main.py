import pandas as pd
from flask import Flask, request, jsonify
import time
import flask
import re
import edgar_utils
import zipfile
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely import box
import io

app = Flask(__name__)

counter = 0
v_a = 0
v_b = 0
ip_dict = {}
data = pd.read_csv("server_log.zip") 

@app.route('/')
def home():
    global counter, v_a, v_b
    with open("index.html") as f:
        html = f.read()
    if counter > 9:
        if v_a > v_b:
            html = re.sub(r"Donate", "<b>Donate</b>", html)
            html = re.sub(r"donate.html","donate.html?from=a" , html)
            return html
        else:
            html = re.sub(r"donate.html","donate.html?from=b" , html)
            return html
    if counter <= 10:
        if counter % 2 == 0:
            counter +=1
            html = re.sub(r"Donate", "<b>Donate</b>", html)
            html = re.sub(r"donate.html","donate.html?from=a" , html)
            return html
        else:
            counter +=1
            html = re.sub(r"donate.html","donate.html?from=b" , html)
            return html
 
@app.route("/browse.html")
def browse():
    with open("browse.html") as f:
        html = str(f.read())
    data = pd.read_csv("server_log.zip")[:500]
    html_data = data.to_html()
    return html + html_data
    
@app.route("/browse.json")  
def browse_json():
    global ip_dict
    ip_addrs = request.remote_addr
    data = pd.read_csv("server_log.zip")[:500]
    if ip_addrs not in ip_dict.keys():
        ip_dict[ip_addrs] = time.time()
        return data.to_json()

        
    if time.time() - ip_dict[ip_addrs]  >= 60:
        ip_dict[ip_addrs] = time.time()
        return data.to_json() 
    
    else:
        html = "Too many request!"
        return flask.Response(html, status = 429, headers = {"Retry-After" : 60})

@app.route("/visitors.json")
def visitors_json():
    global ip_dict
    return list(ip_dict.keys())

@app.route("/donate.html")
def donate():
    with open("donate.html") as f:
        html = str(f.read())
    global v_a, v_b
    try:
        if request.args["from"] == 'a':
            v_a +=1
        else:
            v_b +=1
    except:
        pass
        
    return html

    
top10ips = data['ip'].value_counts().head(10).to_dict()

filings = {}

with zipfile.ZipFile('docs.zip', 'r') as z:
        for filename in z.namelist():
            if filename.endswith(".htm") | filename.endswith(".html"):
                with z.open(filename) as f:
                    html_i = f.read().decode("utf-8")
                    filing_i = edgar_utils.Filing(html_i)
                    filings[filename] = filing_i
sic_number = {}   
for key in filings.keys():
    number = filings[key].sic
    if number == None:
        continue
    if number not in sic_number.keys():
        sic_number[number] = 1
    else:
        sic_number[number] +=1
sorted_items = sorted(sic_number.items(), key=lambda x: (-x[1], -x[0]))[:10]
sorted_sics = {k: v for k, v in sorted_items}


addresses = {}
for idx, row in data.iterrows():
    filename = str(int(row['cik'])) + "/" + str(row['accession']) + "/" + str(row['extention'])
    if filename in filings.keys():
        for address in filings[filename].addresses:
            if address not in addresses.keys():
                addresses[address] = 1
            else:
                addresses[address] +=1
top_300_addresses = {address: count for address, count in addresses.items() if count > 300}

@app.route("/analysis.html")
def analysis():
    with open("analysis.html") as f:
        html = str(f.read())
        html = html.replace("q1_???", str(top10ips))
        html = html.replace("q2_???", str(sorted_sics))
        html = html.replace("q3_???", str(top_300_addresses))
        #html = html + 
        
    return html

@app.route("/dashboard.svg")
def plot():
    zipcodes = []
    gdf_points = gpd.read_file("locations.geojson")#points
    gdf_background = gpd.read_file("shapes/cb_2018_us_state_20m.shp")#background
    fig, ax = plt.subplots(figsize = (3,3))
    plt.axis("off")
    for i in range(len(gdf_points)):
        zipcode = re.findall(r" \d{5}|\d{5}-\d{4}", gdf_points.iloc[i]["address"])
        if zipcode:
            zipcode = int(zipcode[0])
        else:
            zipcode = 0
        zipcodes.append(zipcode)
    gdf_points["zipcode"] = zipcodes
    gdf_cropped_zipcodes = gdf_points[(25000<= gdf_points["zipcode"]) & (gdf_points["zipcode"] <= 65000)]
    ne_box = box(-95,25,-60,50)
    in_bounds = ~gdf_cropped_zipcodes.intersection(ne_box).is_empty
    gdf_cropped_zipcodes = gdf_cropped_zipcodes[in_bounds]
    gdf_background.intersection(ne_box).to_crs("epsg:2022").plot(color = "lightgray", ax = ax)
    gdf_cropped_zipcodes.to_crs("epsg:2022").plot(column = "zipcode", ax = ax, cmap = "RdBu", legend = True)
    f = io.StringIO()
    fig.savefig("dashboard.svg", format="svg")
    plt.close()
    
    return flask.Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.

