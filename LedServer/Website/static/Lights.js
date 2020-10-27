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
                                    <input type="checkbox" class="custom-control-input" id="{{../Room}}-{{this}}-Switch" onclick="SwitchLightClicked(this.id, this.checked)">
                                    <label class="custom-control-label" for="{{../Room}}-{{this}}">ON / OFF</label> 
                                </div>
                                    <label class="text-info">Intensity</label>
                                    <input type="range" class="custom-range" id="{{../Room}}-{{this}}-Intensity"> <!-- style=width:100px> -->
                            </form> 
                        </div>
                        <div id="{{../Room}}collapse{{this}}" class="collapse" data-parent="#accordion">
                            <div class="card-body">
                                <p style="text-decoration:underline"><strong>Settings {{this}}</strong><p>
                                <div class="wheel" id="{{../Room}}-{{this}}-colorpicker"></div>
                            </div>
                        </div>
                    </div>
                    {{/each}}
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
    for (Room in RoomsLights){
        RoomHTML = RoomCardT({"Room":Room, "Lights":RoomsLights[Room]});
        console.log(RoomHTML);
        document.getElementById("RoomContainer").innerHTML = RoomHTML;
    }
}
