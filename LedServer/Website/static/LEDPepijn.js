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
    console.log(ID);
    console.log(Value);
    ID = ID.slice(0, ID.length - 3);
    Lights = $("input[id^='".concat(ID).concat("']"));
    for(x=1; x<Lights.length; x++){
        Lights[x].checked= Value;
    }
}

function SwitchLightClicked(ID, Value){
    x = ID.search("[0-9]");
    ID = ID.slice(0,x).concat("all");
    LightAll=document.getElementById(ID);
    if (!Value){
        Lights = $("input[id^='".concat(ID.slice(0,ID.length - 3)).concat("']"));
        for(x=1; x<Lights.length; x++){
            if (Lights[x].checked){
                Value = true;
            }
        }
    }
    LightAll.checked = Value;
}

function SetLights(){

}
