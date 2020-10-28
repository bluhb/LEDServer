function InitColorWheel(){
    var ColorPicker1 = iro.ColorPicker("#livingroom_lamp_1_colorpicker", {
            width:250,
            id:"Livingroom_light_1"
    });

    var ColorPicker2 = iro.ColorPicker("#livingroom_lamp_2_colorpicker", {
            width:250,
            id:"Livingroom_light_2"
    });
    var ColorPicker3 = iro.ColorPicker("#livingroom_lamp_3_colorpicker", {
            width:250,
            id:"Livingroom_light_3"
    });
    ColorPicker1.on('color:change', function (color, change){ColorChanged(color, this.id)});

    ColorPicker2.on('color:change', function (color, change){ColorChanged(color, this.id)});
    
    ColorPicker3.on('color:change', function (color, change){ColorChanged(color, this.id)});
}

function ColorChanged(color, ID){
    console.log(color);
    console.log(ID);
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


}

function SetLights(){

}
