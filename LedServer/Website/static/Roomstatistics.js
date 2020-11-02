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
        NewDataObj={"Room":Room, "Data":[]}
        for (key in NewData){
            if (typeof(NewData[key][0]) !=="undefined"){
                Exists = true;
                DataObj = {"Key":key, "Value":NewData[key][0]};
                NewDataObj["Data"].push(DataObj);
            }
        }
        if (Exists){Data[Room] = NewDataObj}
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
            <div class="card flexbox">
                <div class="card-header" style="background-color:AntiqueWhite;">
                    <h2>{{Room}}</h2>
            `
    HTMLData=`
                    <div class="row">
                        <div class="col">
                            Temperatuur
                        </div>
                        <div class="col">
                            16&deg;C
                        </div>
                    </div>
            `
    HTMLEnd =`
                </div>
            </div>
        </div>
    </div>`;
    HTMLT = Handlebars.compile(HTML);
    HTMLDT = Handlebars.compile(HTMLData);
    console.log(HTMLC);
}

