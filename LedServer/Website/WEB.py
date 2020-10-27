from flask import Flask, render_template, redirect, request, jsonify
import time
import sys
import logging
#from scipy import signal
import __main__ as main
import Alarm

app = Flask(__name__, static_url_path='/static')
rooms = []

#initialize global variables
def init():
    global rooms
    for key in main.rooms:
        if 'lights' in main.rooms[key]:
            rooms.append(key)
    return None

#Make sure the browser does not cache any of the images.
#Prevents non updating measurement graphs
@app.after_request
def add_header(response):
    response.cache_control.max_age = 1
    return response

@app.route('/')
def homePage():
    global rooms
    return render_template('index.html',
            rooms=rooms,
            page="home")


#Here are the handles for alarms
@app.route('/alarm')
def alarm():
    global rooms
    Alarms = [key for key in Alarm.AlarmDict.keys()]
    return render_template('index.html',
                rooms = rooms,
                alarms = Alarms,
                page = 'alarm')


#From here on all the light handles begin
@app.route('/lights')
def ledPage():
    return render_template('index.html',
                page='led')

@app.route('/car')
def ritRegistration():
    global rooms
    return render_template('index.html',
            rooms = rooms,
            page='ritRegistration')

@app.route('/api/light/setAttr', methods=["POST"])
def ApiLightSetattr():
    JSON = request.get_json(force=True)
    if "Room" in JSON\
            and "Lights" in JSON\
            and "AttrKey" in JSON:
        RoomID = JSON["Room"]
        Key = JSON["AttrKey"][0]
        Value = JSON["AttrKey"][1]
        for Light in JSON["Lights"]:
            if hasattr(main.rooms[RoomID]["lights"][Light], Key):
                setattr(main.rooms[RoomID]["lights"][Light], Key, Value)
            else:
                continue
        return("Attribute set", 200)
    else:
        return("Bad Json", 400)

@app.route('/api/light/setHSV', methods=["POST"])
def ApiLightSetHSV():
    JSON = request.get_json(force=True)
    if "Room" in JSON\
            and "Lights" in JSON\
            and "HSV" in JSON:
        RoomID = JSON["Room"]
        for Light in JSON["Lights"]:
            main.rooms[RoomID]["lights"][Light].HSV.SetHSV(*JSON["HSV"])
        return("HSV set", 200)
    else:
        return("Bad Json", 400)

@app.route('/api/light/getAttr', methods=["POST"])
def ApiLightGetattr():
    JSON = request.get_json(force=True)
    if "Room" in JSON\
            and "Light" in JSON\
            and "Attr" in JSON:
        RoomID = JSON["Room"]
        Key = JSON["Attr"]
        Value = getattr(main.rooms[RoomID]["lights"][Light], Key)
        return(jsonify({"Key": Key, "Value": Value}), 200)
    else:
        return("Bad Json", 400)


@app.route('/api/room/alarm', methods=["POST"])

@app.route('/api/room/data', methods=["POST"])
def returnData():
    # expect json with only the room ID in it, return with the data in json
    json = request.get_json(force=True)
    try:
        roomID = json['roomID']
        if roomID in main.rooms:
            response = {}
            response.update(main.rooms[roomID]["room"].json)
            if "lightID" in json:
                response.update({"color": main.rooms[roomID]["lights"][json["lightID"]].color_rgb})
            return(jsonify(response), 200)
        else:
            return("",418) #I'm a teapot
    except:
        return(jsonify({'error': 'invalid'}), 200)

@app.route('/api/car/graphData', methods=["POST"])
def returnGraphData():
    # expect json with roomID
    JSON = request.get_json(force = True)
    RoomID = JSON["RoomID"]
    Items = int(JSON.get("Items", 1000))
    print("Items: {}".format(Items))
    print("RoomID: {}".format(RoomID))
    Data, Time = main.rooms[RoomID]["room"].getDataFromDB(Items = Items)
    # Temperature = signal.savgol_filter(Data["temperature"], 25, 3)
    # Humidity = signal.savgol_filter(Data["humidity"], 25, 3)
    # LDR = signal.savgol_filter(Data["ldr"], 25, 3)
    Temperature = Data["temperature"]
    Humidity = Data["humidity"]
    LDR = Data["ldr"]
    Graphs = [
        dict(
            data=[
                dict(
                    x = Time,
                    y = Temperature,
                    name = "Temperature",
                    yaxis = "Temperature",
                    type = "lines"
                    ),
                dict(
                    x = Time,
                    y = Humidity,
                    name = "Humidity",
                    yaxis = "y2",
                    type = "lines"
                    )
                ],
            layout = dict(
                title = "Temperature and Humidity",
                yaxis = {"title": "Degree Celsius"},
                xaxis = {"automargin": True},
                yaxis2 = dict(
                    title = "Relative Humidity",
                    overlaying = "y",
                    side = "right"
                    )
                )
            ),
        dict(
            data=[
                dict(
                    x = Time,
                    y = LDR,
                    name = "LDR",
                    yaxis = "LDR",
                    type = "lines"
                    )
                ],
            layout = dict(
                title = "LDR",
                xaxis = {"automargin": True},
                yaxis = {"title": "Relative light strength"},
                showlegend = True
                )
            )
        ]

    GraphsJSON = jsonify(Graphs)
    return(GraphsJSON)



@app.route('/api/car/addNew', methods=["POST"])
def addNewMileage():
    #expects json with "KMStand", "BeginEindPunt", "Getankt"
    json = request.get_json(force=True)
    try:
        KMStand = json["KMStand"]
        BeginEndPoint = json["BeginEindPunt"]
        Tanked = json["Getankt"]
        main.RitReg.insertMileage(KMStand, BeginEndPoint, Tanked)
        return("",418)
    except Exception as e:
        return(e,400)

@app.route('/api/car/getData')
def returnRitData():
    DataList = main.RitReg.getAllData()
    DataList.reverse()
    return(jsonify(DataList), 200)

@app.route('/api/car/getMileage')
def returnMileAge():
    MileAges, MileAge = main.RitReg.averageMileage()
    return(jsonify({"Mileage": MileAge, "Mileages": MileAges}), 200)
