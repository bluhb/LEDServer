TempPoints = {};

function TempInit(){
    for (var i = 0; i<24; i++){
        i = ( (i<10) ? "0".concat(String(i)) : String(i) )
        TempPoints[String(i).concat(":00:00")] = String(20);
        TempPoints[String(i).concat(":30:00")] = String(20);
    }
    CreatePlot();
}

function AddTemp(){
    Time = document.getElementById("Time").value;
    Temp = document.getElementById("Temp").value;
    TempPoints[Time] = Temp;
    CreatePlot()
    H = parseInt(Time.slice(0,2));
    M = parseInt(Time.slice(3,5));
    if (M >= 30){
        H += 1;
        M = ":00";
    }else{
        M = ":30";
    }
    H = ( (H<10) ? "0".concat(String(H)) : String(H) );
    H = ( (H>23) ? "00" : H );
    document.getElementById("Time").value = String(H).concat(String(M)).concat(":00");
}

function CreatePlot(){
    X = []
    Y = []
    for (TempPoint in TempPoints){
        X.push(TempPoint);
        X.sort()
        Y.splice(X.indexOf(TempPoint), 0, TempPoints[TempPoint]);
    }
    var Trace = {x:X, y:Y, type:'scatter', mode:'lines'}
    var Data = [Trace];
    Plotly.newPlot("Plot", Data);
}

async function GetDataFromServer(Room){
    var Data = await $.ajax({
        url: BaseUrl.concat("/api/thermostat/getTemps"),
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({"Room":Room}),
    });
    Temp = {}
    for (x in Data){
        x = Data[x]
        Temp[x["Tijd"]] = x["SetPoint"] 
    }
    TempPoints = Temp
}

function SubmitSettings(){
    Url = BaseUrl.concat("/api/thermostat/setTemps");
    Data = {"Room":"livingroom", "Data":TempPoints};
    PostToUrl(Data, Url);
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
