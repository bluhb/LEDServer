BaseUrl = window.location.origin;
ColorPickers = {};
async function CreateRoomCards(){
    var RoomCard = `
    <div class="col-sm-4">
        <div id="{{Room}}">
            <div class="card" id="Card-{{Room}}-all">
                <div class="card-header">
                    <h3><a class="card-link" data-toggle="collapse" href="#light{{Room}}">
                            {{Room}}
                        </a></h3>
                        <form>
                            <div class="custom-control custom-switch">
                                <input type="checkbox" class="custom-control-input" id="Switch-{{Room}}-all" value="" onclick="SwitchAllClicked(this.id, this.checked)">
                                <label class="custom-control-label" for="Switch-{{Room}}-all">ON / OFF</label> 
                            </div>
                            <label class="text-info">Intensity</label><br>
                            <input type="range" class="slider intensityslider" id="Intensity-{{Room}}-all" oninput="VChanged(this.value, this.id)"> <!-- style=width:100px> -->
                        </form> 
                </div>

                <div id="light{{Room}}" class="collapse" data-parent="#{{Room}}">
                    
                    <div id="accordion">
                        <div class="card" id="Card-Colorpicker-all">
                            <div class="card-header">
                                <div>
                                    <p>
                                        <a>Whole room</a>
                                    </p>
                                    <div class="wheel center" id="colorpicker-{{Room}}-all"></div>
                                </div>
                            </div>
                        </div>
                        {{#each Lights}}
                        <div class="card" id="Card-{{../Room}}-{{this}}">

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
                                        <label class="text-info">Intensity</label><br>
                                        <input type="range" class="slider intensityslider" id="Intensity-{{../Room}}-{{this}}" oninput="VChanged(this.value, this.id)"> <!-- style=width:100px> -->
                                </form> 
                            </div>
                            <div id="{{../Room}}collapse{{this}}" class="collapse" data-parent="#accordion">
                                <div class="card-body">
                                    <p style="text-decoration:underline"><strong>Settings {{this}}</strong><p>
                                    <div class="wheel center" id="colorpicker-{{../Room}}-{{this}}"></div>

                                    <div id="Functions-{{../Room}}-{{this}}"></div>

                                    <div id="Speed-{{../Room}}-{{this}}">
                                        <label class="text-info">Speed</label><br>
                                        <input type="range" class="slider speedadjust" id="Speed-{{../Room}}-{{this}}" oninput="SpeedChanged(this.value, this.id)"> <!-- style=width:100px> -->
                                    </div>
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
    AddFunctionKeys()
    UpdateLightsStatus()
}

async function AddFunctionKeys(){
    var FunctionsRooms = await $.ajax({
        url: BaseUrl.concat("/api/light/getLightsFunctions"),
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(""),
    });
    ButtonHtml = `
        <button type="button" class="btn btn-secondary functionbutton" id="{{Room}}-{{Light}}-{{Function}}" onclick=FunctionButtonClicked(this.id)>
        {{Function}}
        </button><br>
    `
    ButtonT = Handlebars.compile(ButtonHtml)
    for (Room in FunctionsRooms){
        for (Light in FunctionsRooms[Room]){
            for (Func in FunctionsRooms[Room][Light]){
                HTML = ButtonT({
                    "Room":Room,
                    "Light":Light,
                    "Function":FunctionsRooms[Room][Light][Func]
                })
                document.getElementById("Functions-" + Room + "-" + Light).insertAdjacentHTML('afterbegin', HTML);
            }
        }
    }

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
            id:ID,
            layout:[{
                component:iro.ui.Wheel,
                options:{}
            }]
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
            setTimeout(UpdateLightsStatus, 2000);
        }
    )
    window.ColorPickers[ID] = ColorPicker
}
