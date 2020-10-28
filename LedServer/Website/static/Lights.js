BaseUrl = window.location.origin;
ColorPickers = {};
async function CreateRoomCards(){
    var RoomCard = `
    <div class="col-sm-4">
        <div id="{{Room}}">
            <div class="card">
                <div class="card-header">
                    <h3><a class="card-link" data-toggle="collapse" href="#light{{Room}}">
                            {{Room}}
                        </a></h3>
                        <form>
                            <div class="custom-control custom-switch">
                                <input type="checkbox" class="custom-control-input" id="Switch-{{Room}}-all" value="" onclick="SwitchAllClicked(this.id, this.checked)">
                                <label class="custom-control-label" for="Switch-{{Room}}-all">ON / OFF</label> 
                            </div>
                            <label class="text-info">Intensity</label>
                            <input type="range" class="custom-range" id="{{Room}}-Intensity" > <!-- style=width:100px> -->
                            <div class="wheel" id="colorpicker-{{Room}}-all"></div>
                        </form> 
                </div>

                <div id="light{{Room}}" class="collapse" data-parent="#{{Room}}">
                    
                    <div id="accordion">
                        {{#each Lights}}
                        <div class="card">

                            <div class="card-header">
                                <a class="collapsed card-link" data-toggle="collapse" href="#{{../Room}}collapse{{this}}">
                                    <div>
                                        <p>{{this}}</p>
                                    </div>
                                </a>
                                <form>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="custom-control-input" id="Switch-{{../Room}}-{{this}}" onclick="SwitchLightClicked(this.id, this.checked)">
                                        <label class="custom-control-label" for="Switch-{{../Room}}-{{this}}">ON / OFF</label> 
                                    </div>
                                        <label class="text-info">Intensity</label>
                                        <input type="range" class="custom-range" id="Intensity-{{../Room}}-{{this}}"> <!-- style=width:100px> -->
                                </form> 
                            </div>
                            <div id="{{../Room}}collapse{{this}}" class="collapse" data-parent="#accordion">
                                <div class="card-body">
                                    <p style="text-decoration:underline"><strong>Settings {{this}}</strong><p>
                                    <div class="wheel" id="colorpicker-{{../Room}}-{{this}}"></div>
                                </div>
                            </div>
                        </div>
                        {{/each}}
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
    RoomCardT = Handlebars.compile(RoomCard);
    var RoomsLights = await $.ajax({
        url: BaseUrl.concat("/api/light/getLights"),
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(""),
    });
    TotalHTML = ""
    for (Room in RoomsLights){
        RoomHTML = RoomCardT({"Room":Room, "Lights":RoomsLights[Room]});
        TotalHTML = TotalHTML.concat(RoomHTML);
    }
    document.getElementById("RoomContainer").innerHTML = TotalHTML;
    
    for (Room in RoomsLights){
        for(Light in RoomsLights[Room]){
            AddColorWheel(Room, RoomsLights[Room][Light]);
        }
        AddColorWheel(Room, "all");
    }
    UpdateLightsStatus()
}

function AddColorWheel(Room, Light){
    DomID = "#colorpicker-".concat(Room).concat("-").concat(Light);
    console.log(DomID)
    ID = Room.concat("-").concat(Light)
    console.log(ID)
    var ColorPicker = iro.ColorPicker(
        DomID, 
        {
            width:250,
            id:ID
        }
    );
    ColorPicker.on(
        'input:move',
        function (color, change){
            ColorChanged(color, this.id);
        }
    )
    ColorPicker.on(
        'input:end',
        function (color, change){
            ColorChanged(color, this.id);
            console.log("Color End");
            setTimeout(UpdateLightsStatus, 1100);
        }
    )
    window.ColorPickers[ID] = ColorPicker
}

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
            console.log(Func);
            console.log(Color)
            console.log(ID)
            window.ColorPickers[ID].color.set(Color)
            if (!(Func === "off")){
                document.getElementById("Switch-".concat(ID)).checked = true;
            }else{
                document.getElementById("Switch-".concat(ID)).checked = false;
            }
        }
        hAvg = Math.atan2(AvgH.Sin, AvgH.Cos);
        AvgHSV.h = rad2deg(hAvg);
        AvgHSV.s = AvgHSV.s/AvgCount;
        AvgHSV.v = AvgHSV.v/AvgCount;
        console.log(AvgHSV);
        window.ColorPickers[Room.concat("-all")].color.set(AvgHSV);

    }
}

function deg2rad(deg){
    return deg * (Math.PI/180);
}

function rad2deg(rad){
    return rad * (180/Math.PI);
}



