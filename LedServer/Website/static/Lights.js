async function UpdateLightsStatus(){
    var Statusses = await $.ajax({
        url: BaseUrl.concat("/api/light/getStatus"),
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(""),
    });
    UpdateLightFunctionColor(Statusses);
}

function UpdateLightFunctionColor(Statusses){
    for (var Room in Statusses){
        AllSwitch = false;
        AvgH = {"Cos":0, "Sin":0}
        AvgHSV = {"h":0, "s":0, "v":0};
        AvgCount = 0
        for (var Light in Statusses[Room]){
            Func = Statusses[Room][Light]["Function"];
            Color = Statusses[Room][Light]["HSV"];
            AvgCount++;
            AvgH.Sin += Math.sin(deg2rad(Color.h));
            AvgH.Cos += Math.cos(deg2rad(Color.h));
            AvgHSV.s += Color.s;
            AvgHSV.v += Color.v;
            console.log(Color);
            console.log(AvgHSV);
            ID = Room.concat("-").concat(Light)
            if (!(Func === "off") || Color.v > 0){
                AllSwitch = true;
                document.getElementById("Switch-".concat(ID)).checked = true;
            }else{
                document.getElementById("Switch-".concat(ID)).checked = false;
            }
            document.getElementById("Intensity-".concat(ID)).value = Color.v;
            HSL = HSVtoHSL(Color);
            HSLString = CreateCSSColorString(HSL);
            console.log(HSLString);
            document.getElementById("Intensity-".concat(ID)).style.background = HSLString
            Color.v = 100;
            window.ColorPickers[ID].color.set(Color);
        }
        hAvg = Math.atan2(AvgH.Sin, AvgH.Cos);
        AvgHSV.h = rad2deg(hAvg);
        AvgHSV.s = AvgHSV.s/AvgCount;
        AvgHSV.v = AvgHSV.v/AvgCount;
        console.log(AvgHSV);
        document.getElementById("Intensity-".concat(Room).concat("-all")).value = AvgHSV.v;
        document.getElementById("Switch-".concat(Room).concat("-all")).checked = AllSwitch;
        HSL = HSVtoHSL(AvgHSV);
        HSLString = CreateCSSColorString(HSL);
        console.log(HSLString)
        document.getElementById("Intensity-".concat(Room).concat("-all")).style.background = HSLString
        AvgHSV.v = 100;
        window.ColorPickers[Room.concat("-all")].color.set(AvgHSV);

    }
}

function ColorChanged(color, ID){
    Room = ID.split("-")[0];
    Light = ID.split("-")[1];
    HSV = color.hsv;
    Data = {"Room":Room,
        "Lights":[Light],
        "H": HSV.h,
        "S": HSV.s
    };
    console.log(Data);
    Url = BaseUrl.concat('/api/light/setHS');
    $.ajax({
        dataType:'json',
        type: "post",
        url:Url,
        data:JSON.stringify(Data)
    });
    setTimeout(UpdateLightsStatus, 2000)
}

function VChanged(V, ID){
    Room = ID.split("-")[1];
    Light = ID.split("-")[2];
    Data = {"Room":Room,
        "Lights":[Light],
        "V": V,
    };
    console.log(Data);
    Url = BaseUrl.concat('/api/light/setV');
    $.ajax({
        dataType:'json',
        type: "post",
        url:Url,
        data:JSON.stringify(Data)
    });
    setTimeout(UpdateLightsStatus, 2000)
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
    setTimeout(UpdateLightsStatus, 2000)
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
    setTimeout(UpdateLightsStatus, 2000)
}

function deg2rad(deg){
    return deg * (Math.PI/180);
}

function rad2deg(rad){
    return rad * (180/Math.PI);
}

function HSVtoHSL(h,s,v){
    if (arguments.length === 1){
        s=h.s, v=h.v, h=h.h;
    }
    var s = s/100, v=v/100;
    var _h = h,
        _s = s*v,
        _l = (2-s)*v;
    _s /= (_l <= 1) ? (_l === 0 ? 1 : _l) : 2 - _l;
    _l /= 2
    _s = ((isNaN(_s)) ? 0 : _s);
    HSL = {h:_h, s:_s*100, l:_l*100}
    return HSL
}

function CreateCSSColorString(HSL){
    return ("hsl(" + HSL.h + "," + HSL.s + "%," + HSL.l + "%)")
}
