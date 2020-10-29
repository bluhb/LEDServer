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
    
}

