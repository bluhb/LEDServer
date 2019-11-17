from flask import Flask, render_template, redirect, request, jsonify
import time
import sys
import logging
import __main__ as main

app = Flask(__name__)
rooms = []

#initialize global variables
def init():
    global rooms
    for key in main.rooms:
        if 'lights' in main.rooms[key]:
            rooms.append(key)
    return None

@app.route('/')
def homePage():
    global rooms
    return render_template('index.html',
            rooms=rooms,
            page="home")

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

#this route is used in the old app. Can be deleted for new app
@app.route('/color', methods=["POST"])
def colorControlOLD():
#expected json = {'lightID':'livingroom','r':0,'g':0,'b':0}
    json = request.get_json(force=True)
    if not 'lightID' in json:
        for key in main.rooms:
            main.rooms[key]['lights']['LedStrip'].color_rgb = json
        return("",204)
    else:
        return ("",404)

@app.route('/rooms/color', methods=["POST"])
# expect JSON in the following format:
# {'roomID':A room defined in main
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
            return(jsonify(main.rooms[roomID]["room"].json), 200)
        else:
            return("",418) #I'm a teapot
    except:
        return(jsonify({'error': 'invalid'}), 200)
