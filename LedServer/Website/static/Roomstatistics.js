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
        Data[Room] = await $.ajax({
            dataType:'json',
            type: "post",
            url:Url,
            data:JSON.stringify({"RoomID": Room})
        });
    }
    console.log(Data)
    document.getElementById("Container").innerHTML = "";
    for (Room in Data){
        HTML = "<div><p><h3>" + Room + "</h3></p>"
        for(Key in Data[Room]){
            Value = Data[Room][Key];
            HTML += "<p>" + Key + " : " + Value[0] + "</p>"
        }
        HTML += "</div>"
        document.getElementById("Container").insertAdjacentHTML("afterbegin", HTML);
    }
    
}

