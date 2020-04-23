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

#handle to show the graphs of every room and the pi
@app.route('/graphs')
def graphs():
    global rooms
    return render_template('index.html',
            rooms = rooms,
            page='graphs')

#Here are the handles for alarms
@app.route('/alarm')
def alarm():
    global rooms
    Alarms = [key for key in Alarm.AlarmDict.keys()]
    return render_template('index.html',
                rooms = rooms,
                alarms = Alarms,
                page = 'alarm')

@app.route('/alarm/setAlarm', methods=["POST"])
def setAlarm():
    JSON = request.get_json(force=True)
    if not ( ("Hour" in JSON) and ("Minute" in JSON) ):
        return ("", 204)
    Hour = JSON["Hour"]
    Minute = JSON["Minute"]
    PreWakeUp = JSON.get("PreWakeUp", None)
    Alarm.setupAlarm(Hour, Minute, PreWakeUp=PreWakeUp)
    return("", 418)

@app.route('/alarm/disableAlarm', methods=["POST"])
def disableAlarm():
    JSON = request.get_json(force=True)
    if not "AlarmName" in JSON:
        return("",204)
    Alarm.AlarmDict[JSON["AlarmName"]]["Stop"] = True
    return("",204)

#From here on all the light handles begin
@app.route('/rooms/<string:roomID>')
def ledPage(roomID):
    global rooms
    if (roomID in rooms):
        return render_template('index.html',
                rooms = rooms,
                roomID = roomID,
                lights = [*main.rooms[roomID]['lights']],
                functdict = main.rooms[roomID]['lights']['LedStrip'].functdict,
                color_rgb = main.rooms[roomID]['lights']['LedStrip'].color_rgb,
                wait = main.rooms[roomID]['lights']['LedStrip'].wait,
                page='led')
    else:
        return('404 not found, you have not installed this light')



@app.route('/rooms/color', methods=["POST"])
# expect JSON in the following format:
# {'roomID':A rooms defined in main
#  'lightIDs':A list of lightIDs defined in main,
#  'r': 0, 'g':0, 'b':0}
def colorControl():
    color = {'r':0,'g':0,'b':0}
    json = request.get_json(force=True)
    for key in color:
        color[key] = int(json[key])
    lightIDs = json['lightIDs']
    roomID = json['roomID']
    for lightID in lightIDs:
        main.rooms[roomID]['lights'][lightID].color_rgb = color
    return("",204)

@app.route('/rooms/function', methods=["POST"])
def functionControl():
    #expect JSON with following format
    #{'roomID': A room defined in main.
    # 'lightIDs': A list of lightIDs defined in main.
    # 'function': An accepted function for the light}
    function = ""
    json = request.get_json(force=True)
    roomID = json['roomID']
    lightIDs = json['lightIDs']
    function = json['function']
    for lights in lightIDs:
        main.rooms[roomID]['lights'][lights].function = function
    return("",204)

@app.route('/rooms/attrNum', methods=["POST"])
def attributeControlNum():
    #expect JSON with following format
    # {'roomID': A room defined in main,
     # 'lightIDs': A list of lightIDs defined in main.
     # 'key':value -> key is the variable that needs to be set to value
     # }
    json = request.get_json(force=True)
    roomID = json['roomID']
    lightIDs = json['lightIDs']
    json.pop('roomID', None)
    json.pop('lightIDs', None)
    attributes={}
    for key,value in json.items():
        attributes[key] = value
    #try:
    for lights in lightIDs:
        for key,value in attributes.items():
            setattr(main.rooms[roomID]['lights'][lights],
                    key,
                    float(value))
    #except:
    #    pass
    return("",204)

@app.route('/rooms/attrBool', methods=["POST"])
def attributeControlBool():
    #expect JSON with following format
    # {'roomID': A room defined in main,
     # 'lightIDs': A list of lightIDs defined in main.
     # 'key':value -> key is the variable that needs to be set to value
     # }

    json = request.get_json(force=True)
    roomID = json['roomID']
    lightIDs = json['lightIDs']
    json.pop('roomID', None)
    json.pop('lightIDs', None)
    attributes={}
    for key,value in json.items():
            attributes[key] = value
    try:
        for lights in lightIDs:
            for key,value in attributes.items():
                setattr(main.rooms[roomID]['lights'][lights],
                        key,
                        bool(value))
    except:
        pass
    return("",204)

@app.route('/rooms/data', methods=["POST"])
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

@app.route('/rooms/graphData', methods=["POST"])
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

@app.route('/ritregistration')
def ritRegistration():
    global rooms
    return render_template('index.html',
            rooms = rooms,
            page='ritRegistration')

@app.route('/ritregistration/addNew', methods=["POST"])
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

@app.route('/ritregistration/getData')
def returnRitData():
    DataList = main.RitReg.getAllData()
    DataList.reverse()
    return(jsonify(DataList), 200)
