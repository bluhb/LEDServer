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

@app.route('/roomstatistics')
def roomstatisticsPage():
    return render_template('index.html',
                page='roomstatistics')

@app.route('/car')
def ritRegistration():
    global rooms
    return render_template('index.html',
            rooms = rooms,
            page='ritRegistration')

@app.route('/thermostat')
def Thermostat():
    global rooms
    return render_template('index.html',
            rooms = rooms,
            page='Thermostat')

@app.route('/api/light/getLights', methods=["POST"])
def ApiGetLights():
    Data = {}
    for room in sorted(main.rooms):
        if "lights" in main.rooms[room]:
            Data[room] = list(main.rooms[room]["lights"].keys())
            Data[room].sort()
    return (jsonify(Data), 200)

@app.route('/api/light/getLightsFunctions', methods=["POST"])
def ApiGetLightsFunctions():
    Data = {}
    for room in main.rooms:
        if "lights" in main.rooms[room]:
            Data[room] = {}
            for light in main.rooms[room]["lights"].keys():
                Data[room][light] = list(main.rooms[room]["lights"][light].functdict.keys())
                Data[room][light].remove("on")
                Data[room][light].remove("off")
    return (jsonify(Data), 200)

@app.route('/api/light/switchAll', methods=["POST"])
def ApiSwitchAllLights():
    JSON = request.get_json(force=True)

    if "Room" in JSON\
            and "Function" in JSON:
        RoomID = [x.replace(" ", "") for x in JSON["Room"]]
        if RoomID[0] == "all":
            RoomID = main.rooms.keys()
        Function = JSON["Function"]
        for Room in RoomID:
            if "lights" in main.rooms[Room]:
                for light in main.rooms[Room]["lights"]:
                    main.rooms[Room]["lights"][light].function=Function
        return("Turned on", 200)
    else:
        return("BadJson",400)

@app.route('/api/light/setAttr', methods=["POST"])
def ApiLightSetattr():
    print(request)
    JSON = request.get_json(force=True)
    print(JSON)
    if "Room" in JSON\
            and "Lights" in JSON\
            and "AttrKey" in JSON:
        RoomID = JSON["Room"].replace(" ","")
        Key = JSON["AttrKey"][0]
        Value = JSON["AttrKey"][1]
        for Light in JSON["Lights"]:
            if hasattr(main.rooms[RoomID]["lights"][Light], Key):
                setattr(main.rooms[RoomID]["lights"][Light], Key, Value)
            else:
                continue
        return("Attribute set", 200)
    else:
        return("Bad Json", 418)

@app.route('/api/light/setHS', methods=["POST"])
def ApiLightSetHS():
    JSON = request.get_json(force=True)
    if "Room" in JSON\
            and "Lights" in JSON\
            and "H" in JSON\
            and "S" in JSON:
        RoomID = JSON["Room"].replace(" ","")
        if JSON["Lights"][0] == "all":
            Lights = main.rooms[RoomID]["lights"].keys()
        else:
            Lights = JSON["Lights"]
        for Light in Lights:
            Lobj = main.rooms[RoomID]["lights"][Light]
            HSV = {"H": JSON["H"],
                    "S": JSON["S"],
                    "V": Lobj.HSV.V}
            print(HSV)
            main.rooms[RoomID]["lights"][Light].HSV.SetHSV(**HSV)
        return("HSV set", 200)
    else:
        return("Bad Json", 400)

@app.route('/api/light/setV', methods=["POST"])
def ApiLightSetV():
    JSON = request.get_json(force=True)
    if "Room" in JSON\
            and "Lights" in JSON\
            and "V" in JSON:
        RoomID = JSON["Room"].replace(" ","")
        if JSON["Lights"][0] == "all":
            Lights = main.rooms[RoomID]["lights"].keys()
        else:
            Lights = JSON["Lights"]
        for Light in Lights:
            Lobj = main.rooms[RoomID]["lights"][Light]
            HSV = {"H": Lobj.HSV.H,
                    "S": Lobj.HSV.S,
                    "V": JSON["V"]}
            if not Lobj.function == "off":
                Lobj.HSV.SetHSV(**HSV)
        return("HSV set", 200)
    else:
        return("Bad Json", 400)

@app.route('/api/light/getAttr', methods=["POST"])
def ApiLightGetattr():
    JSON = request.get_json(force=True)
    if "Room" in JSON\
            and "Light" in JSON\
            and "Attr" in JSON:
        RoomID = JSON["Room"].replace(" ","")
        Key = JSON["Attr"]
        Value = getattr(main.rooms[RoomID]["lights"][Light], Key)
        return(jsonify({"Key": Key, "Value": Value}), 200)
    else:
        return("Bad Json", 400)

@app.route('/api/light/getStatus', methods=["POST"])
def ApiLightGetStatus():
    RoomsLights = {}
    for room in main.rooms:
        if "lights" in main.rooms[room]:
            RoomsLights[room] = {}
            for Light in list(main.rooms[room]["lights"].keys()):
                RoomsLights[room][Light] = {"HSV":{
                    "h": main.rooms[room]["lights"][Light].HSV.H,
                    "s": main.rooms[room]["lights"][Light].HSV.S,
                    "v":main.rooms[room]["lights"][Light].HSV.V
                    },
                    "Function":main.rooms[room]["lights"][Light].function,
                    "Speed":main.rooms[room]["lights"][Light].Speed,
                }
    return (jsonify(RoomsLights), 200)


@app.route('/api/room/alarm', methods=["POST"])

@app.route('/api/roomstatistics/getRooms', methods=["POST"])
def ApiRoomstatisticsGetRooms():
    Rooms = list(main.rooms.keys())
    Rooms.sort()
    return (jsonify(Rooms), 200)

@app.route('/api/roomstatistics/data', methods=["POST"])
def returnData():
    # expect json with only the room ID in it, return with the data in json
    json = request.get_json(force=True)
    try:
        roomID = json['RoomID'].replace(" ","")
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

@app.route('/api/roomstatistics/graphData', methods=["POST"])
def returnGraphData():
    # expect json with roomID
    JSON = request.get_json(force = True)
    RoomID = JSON["RoomID"].replace(" ","")
    Items = int(JSON.get("Items", 1000))
    print("Items: {}".format(Items))
    print("RoomID: {}".format(RoomID))
    Data = main.rooms[RoomID]["room"].getDataFromDB(Items = Items)
    # Temperature = signal.savgol_filter(Data["temperature"], 25, 3)
    # Humidity = signal.savgol_filter(Data["humidity"], 25, 3)
    # LDR = signal.savgol_filter(Data["ldr"], 25, 3)
    try:
        Temperature = Data["temperature"]
        Humidity = Data["humidity"]
        LDR = Data["ldr"]
        Time = Data["time"]
    except Exception as E:
        return ("No Graph available", 400)
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
                    ),
                dict(
                    x = Time,
                    y = LDR,
                    name = "LDR",
                    yaxis = "y3",
                    type = "lines"
                    )
                ],
            layout = dict(
                title = RoomID + " Temperature and Humidity",
                yaxis = {"title": "Degree Celsius"},
                xaxis = {"automargin": True},
                yaxis2 = dict(
                    title = "Relative Humidity",
                    overlaying = "y",
                    side = "left",
                    anchor= "free",
                    position = 0.15
                    ),
                yaxis3 = dict(
                    title = "Relative light strenght",
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
                title = RoomID + " LDR",
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
