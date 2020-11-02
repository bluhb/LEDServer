function Init(){
    GetCurrentData()    
}

async function GetCurrentData(){
    Url = BaseUrl.concat('/api/roomstatistics/getRooms');
    Rooms = await $.ajax({
        dataType:'json',
        type: "post",
        url:Url,
        data:JSON.stringify("")
    });
    
    Data = {}
    Url = BaseUrl.concat('/api/roomstatistics/data')
    for (Room in Rooms){
        Room = Rooms[Room]
        NewData = await $.ajax({
            dataType:'json',
            type: "post",
            url:Url,
            data:JSON.stringify({"RoomID": Room})
        });
        Exists=false;
        for (key in NewData){
            if (typeof(NewData[key][0]) !=="undefined"){
                Exists = true;
                NewData[key] = NewData[key][0];
            }
        }
        if (Exists){Data[Room] = Object.entries(NewData)}
    }
    console.log(Data);
    document.getElementById("Container").innerHTML = "";
    for (Room in Data){
        HTML = "<div><p><h3>" + Room + "</h3></p>"
        for(Key in Data[Room]){
            Value = Data[Room][Key];
            HTML += "<p>" + Key + " : " + Value[0] + "</p>";
            }
        HTML += "</div>"
        document.getElementById("Container").insertAdjacentHTML("afterbegin", HTML);
    }
}

function CompileTemplates(Data){
    HTML = `
    <div class="row">
        <div class="col">
            {{#Data}}
            <div class="card flexbox">
                <div class="card-header" style="background-color:AntiqueWhite;">
                    <h2>{{this}}</h2>
                    <div class="row">
                        <div class="col">
                            Temperatuur
                        </div>
                        <div class="col">
                            16&deg;C
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Humidity
                        </div>
                        <div class="col">
                            16%
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            LDR
                        </div>
                        <div class="col">
                            878
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
    HTMLT = Handlebars.compile(HTML);
    HTMLC = HTMLT(Data);
    console.log(HTMLC);
}

