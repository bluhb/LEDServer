//At the backend the Num and Bool types are handled different. That is why it is needed to have seperate functions and urls for them

//Inputs nummer to the server.
function InputServerNum(ID, value){
    data = {roomID: window.roomID, lightIDs: window.lights, [ID]:value};
    PostToUrl(data, "attrNum");
}

//Input bool to the server
function InputServerBool(ID, value){
    data = {roomID: window.roomID, lightIDs: window.lights, [ID]:value}
    PostToUrl(data, "attrBool")
}

//Input colors to the server. Color is an object send from the colorwheel.
function InputColor(color, changes){
    var temp = color.rgb
    var data = {roomID: window.roomID, lightIDs: window.lights, 'r':temp['r'],'g':temp['g'],'b':temp['b']};
    PostToUrl(data,"color");
    console.log(data)
    }

//Input the function name, this is directly set in the lights given in the window.lights array.
function InputFunction(functID){
    var data = {roomID: window.roomID, lightIDs: window.lights , function: functID};
    PostToUrl(data,"function");
}

//Post the data to a given url, just a wrapper for the ajax function
function PostToUrl(data, url){
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(data),
        processData: false
    });
}

//Data function to get temp and humid data from the server for the current room.
function data(roomID){
    request = {"roomID": roomID, "lightID": window.lights[0]};
    url = "data";
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(request)
    })
    .done(
        function(response){
            if (response.hasOwnProperty("error")){
                alert("Data request gone wrong");
            } else{
                setDataOnSite(response);
            }
        }
    );
}

//Get pi data from server and put it on the site.
function setPiDataOnSite(){
    request = {"roomID": 'pi'};
    url = "data";
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(request)
    })
    .done(
        function(response){
            if (response.hasOwnProperty('error')){
                alert("dirk");
            } else{
                document.getElementById('temperature').value = response["temperature"];
                document.getElementById('cpu_load').value = response["load"];
            }
        }
    )
}

//Set the data on the site. 
function setDataOnSite(data){
    if ( "color" in data ){
        colorPicker.color.set(data["color"]);
    }
    document.getElementById('roomTemp').value = data["temperature"];
    document.getElementById('roomHumid').value = data["humidity"];
    document.getElementById('roomLight').value = data["ldr"];
}

//Submit alarm time to the server
function submitAlarm(){
    Hour = String(document.getElementById('Hour').value)
    Minute = String(document.getElementById('Minute').value)
    Json = {"Hour":Hour, "Minute": Minute}
    console.log(Json)
    
    PostToUrl(Json, 'alarm/setAlarm')
}

function disableAlarm(Alarm){
    Json = {"AlarmName": Alarm}
    PostToUrl(Json, 'alarm/disableAlarm')
}

function updateGraphs(Rooms){
    DataPoints = parseInt(document.getElementById('DataPoints').value) || 1000
    console.log(Rooms)
    Rooms.forEach(Room => createGraph(Room, DataPoints))
}

function createGraph(Room, DataPoints){
    console.log("Updating Graph: ".concat(Room));
    request = {"RoomID": Room, "Items": DataPoints};
    url = "graphData";
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(request)
    })
    .done(
        function(response){
            for (i=0; i < response.length; i++){
                try{
                    var Data = response[i].data;
                    var Layout = response[i].layout || {};
                    var Id = Room.concat("-Graph").concat(i);
                    Plotly.react(Id,
                                Data,
                                Layout || {});
                }
                catch(err){
                    document.getElementById(Room.concat("-Error")).innerHTML = err.message;
                }
            }
        }
   )
}

function getData(){
    $.getJSON('ritregistration/getData').then(Data =>{
        for (i=0; i < Data.length; i++){
            var Paragraph = document.createElement("p")
            var D = Data[i]
            var TextString = "ID:".concat(D.id).concat(" |KM stand: ").concat(D.KMStand).concat(" |Begin/eind punt: ").concat(D.BeginEindPunt).concat(" |Getankt: ").concat(D.Getankt).concat(" |Tijd: ").concat(D.Time)
            var Node = document.createTextNode(TextString)
            Paragraph.appendChild(Node)
            document.getElementById("Data").appendChild(Paragraph)
        }
    })
}

function submitMilage(){
    KM = parseInt(document.getElementById('KM').value)
    BeginEndPoint = String(document.getElementById('BeginEndPoint').value)
    Tanked = parseInt(document.getElementById('Tanked').value)
    json = {"KMStand":KM, "BeginEindPunt":BeginEndPoint, "Getankt":Tanked}
    PostToUrl(json, "ritregistration/addNew")
}
