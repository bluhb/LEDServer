BaseUrl = window.location.origin;
async function CreateRoomCards(){
    var RoomCard = `
    <div id="{{Room}}">
        <div class="card">
            <div class="card-header">
                <h3><a class="card-link" data-toggle="collapse" href="#light{{Room}}">
                        {{Room}}
                    </a></h3>
                    <form>
                        <div class="custom-control custom-switch">
                            <input type="checkbox" class="custom-control-input" id="switch_{{Room}}_all" value="" onclick="SwitchAllClicked(this.id, this.checked)">
                            <label class="custom-control-label" for="switch_livingroom_all">ON / OFF</label> 
                        </div>
                            <label class="text-info">Intensity</label>
                            <input type="range" class="custom-range" id="{{Room}}-Intensity" > <!-- style=width:100px> -->
                    </form> 
            </div>

            <div id="light{{Room}}" class="collapse" data-parent="#{{Room}}">
                
                <div id="accordion">
    `
    var LightCard = `
                    <div class="card">

                        <div class="card-header">
                            <a class="collapsed card-link" data-toggle="collapse" href="#{{Room}}collapse{{Light}}">
                                <div>
                                    <p>{{Light}}</p>
                                </div>
                            </a>
                            <form>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="{{Room}}-{{Light}}" onclick="SwitchLightClicked(this.id, this.checked)">
                                    <label class="custom-control-label" for="{{Room}}-{{Light}}">ON / OFF</label> 
                                </div>
                                    <label class="text-info">Intensity</label>
                                    <input type="range" class="custom-range" id="{{Room}}-{{Light}}"> <!-- style=width:100px> -->
                            </form> 
                        </div>
                        <div id="{{Room}}collapse{{Light}}" class="collapse" data-parent="#accordion">
                            <div class="card-body">
                                <p style="text-decoration:underline"><strong>Settings {{Light}}</strong><p>
                                <div class="wheel" id="{{Room}}-{{Light}}-colorpicker"></div>
                            </div>
                        </div>
                    </div>
    `
    var EndRoomCard = `
                </div>
            </div>
        </div>
    </div>
    `
    RoomCardT = Handlebars.compile(RoomCard);
    LightCardT = Handlebars.compile(LightCard);
    var RoomsLights = await $.ajax({
        url: BaseUrl.concat("/api/light/getLights"),
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(""),
    });
    for (Room in RoomsLights){
        Lights = RoomsLights[Room];
        RoomHTML = RoomCardT({"Room":Room});
        LightHTML = "";
        for(L in Lights){
            Light = Lights[L]
            LightHTML.concat(LightCardT({"Light":Light}));
            LightHTML.concat("/n");
        }
        TotalHTML = RoomHTML.concat(LightHTML).concat(EndRoomCard);
        console.log(TotalHTML);
    }
}
