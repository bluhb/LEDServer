function Init(){
    GetCurrentTemps()    
}

async function GetCurrentTemps(){
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
            json:JSON.stringify({"RoomID": Room})
        });
    }
    console.log(Data)
    
}

