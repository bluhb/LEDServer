function Init(){
    GetCurrentData();
    setTimeout(GetCurrentData, 5000);
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
    HTML = CompileTemplates(Data);
    document.getElementById("Container").insertAdjacentHTML("afterbegin", HTML);
}

function CompileTemplates(Data){
    HTML = `
        <div class="card roomstatsCards"">
            <h2>{{Room}}</h2>
            {{#each Data}}
            <div class="row">
                <div class="col-sm">
                    {{this.Key}}
                </div>
                <div class="col-sm">
                    {{this.Value}}
                </div>
            </div>
            {{/each}}
        </div>`;
    HTMLTotal = `<div class="justify-content-center card-deck">`
    HTMLT = Handlebars.compile(HTML);
    for (Room in Data){
        HTMLTotal += HTMLT(Data[Room]);
    }
    HTMLTotal += "</div>";
    return (HTMLTotal);
}

