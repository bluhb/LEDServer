function ColorChanged(color, ID){
    Room = ID.split("-")[0];
    Light = ID.split("-")[1];
    HSV = color.hsv;
    Data = {
        "Room":Room,
        "Lights":[Light],
        "HSV": [HSV.h, HSV.s, HSV.v]
    }
    console.log(Data);
    Url = BaseUrl.concat('/api/light/setHSV');
    $.ajax({
        dataType:'json',
        type: "post",
        url:Url,
        data:JSON.stringify(Data)
    });
}

function SwitchAllClicked(ID, Value){
    ID = ID.split("-").slice(0,-1).join("-");
    SearchString = '[id^='.concat(ID).concat(']');
    Lights = document.querySelectorAll(SearchString);
    for(x=1; x<Lights.length; x++){
        Lights[x].checked= Value;
    }
    OnOff = ((Value) ? 'on' : 'off');
    Url = window.BaseUrl.concat('/api/light/switchAll');
    Data = {
        "Room":ID.split("-")[1],
        "Function": OnOff
    }
    console.log(Data);
    $.ajax({
        dataType:'json',
        type: "post",
        url:Url,
        data:JSON.stringify(Data)
    });
    setTimeout(UpdateLightsStatus, 500)
}

function SwitchLightClicked(ID, Value){
    Light = ID.split("-").slice(-1).pop();
    IDAll = ID.split("-").slice(0,-1).join("-").concat("-all");
    LightAll=document.getElementById(IDAll);
    ValueAll = Value;
    if (!Value){
        Lights = $("input[id^='".concat(IDAll.slice(0,IDAll.length - 3)).concat("']"));
        for(x=1; x<Lights.length; x++){
            if (Lights[x].checked){
                ValueAll = true;
            }
        }
    }
    LightAll.checked = ValueAll;
    OnOff = ((Value) ? 'on' : 'off');
    Url = window.BaseUrl.concat('/api/light/setAttr');
    Data = {
        "Room":ID.split("-")[1],
        "Lights":[Light],
        "AttrKey":["function", OnOff]
    }
    $.ajax({
        dataType:'json',
        type: "post",
        url:Url,
        data:JSON.stringify(Data)
    });
    setTimeout(UpdateLightsStatus, 500)
}
