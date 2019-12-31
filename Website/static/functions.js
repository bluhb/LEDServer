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
    }

//Input the function name, this is directly set in the lights given in the window.lights array.
function InputFunction(functID){
    var data = {roomID: window.roomID, lightIDs: window.lights , function: functID};
    PostToUrl(data,"function");
}

//Post the data to an given url, just a wrapper for the ajax function
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
                document.getElementById('temperature').value = response["temp"];
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
    document.getElementById('roomTemp').value = data["temp"];
    document.getElementById('roomHumid').value = data["humid"];
    document.getElementById('roomLight').value = data["LDR"];
}
