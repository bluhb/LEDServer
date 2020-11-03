function Init(){
    GetCurrentData();

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
            if (typeof(NewData[key]) !=="undefined" & key != "room" & NewData[key] !== -1){
                Exists = true;
                DataObj = {"Key":key, "Value":NewData[key]};
                NewDataObj["Data"].push(DataObj);
            }
        }
        if (Exists){Data[Room] = NewDataObj}

    }
    console.log(Data);
    //document.getElementById("Container").innerHTML = "";
    HTML = CompileTemplates(Data);
    document.getElementById("Container").insertAdjacentHTML("afterbegin", HTML);
    for (Room in Data){
        CreateGraph(Room, 500);
        await new Promise(r=>setTimeout(r, 1000));
    }
    setTimeout(GetCurrentData, 120000);
}

function CompileTemplates(Data){
    HTML = `
        <div id = "{{Room}}-Card" class="card roomstatsCards"">
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
    ReplaceAll = false;
    for (Room in Data){
        New = HTMLT(Data[Room])
        if (document.getElementById(Room+"-Graph0") == null & document.getElementById(Room+"-Graph1") == null || ReplaceAll){ 
            ReplaceAll = true;
            HTMLTotal += New;
        }else{
            Elem = document.getElementById(Room+"-Card");
            Elem.parentNode.removeChild(Elem);
            document.getElementById("Container").insertAdjacentHTML("afterbegin", New);
        }
    }
    HTMLTotal += "</div>";
    if (ReplaceAll){
        for (Room in Data){
                HTMLTotal += "<div id="+Room+"-Graph0></div><div id="+Room+"-Graph1></div>";
        }
        document.getElementById("Container").innerHTML = "";
        document.getElementById("Container").insertAdjacentHTML("afterbegin", HTMLTotal);
    }
    return (HTMLTotal);
}

function CreateGraph(Room, DataPoints){
    console.log("Updating Graph: ".concat(Room));
    request = {"RoomID": Room, "Items": DataPoints};
    url = "/api/roomstatistics/graphData";
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(request)
    })
    .done(
        function(response){
            for (i=0; i < response.length; i++){
                try{
                    var Data = response[i].data;
                    var Layout = response[i].layout || {};
                    var Id = Room.concat("-Graph").concat(i);
                    Plotly.react(Id,
                                Data,
                                Layout || {});
                }
                catch(err){
                    console.log(err)
                }
            }
        }
   )
}
