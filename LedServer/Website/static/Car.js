
function getData(){
    $.getJSON(BaseUrl + '/api/car/getData').then(Data =>{
        for (i=0; i < Data.length; i++){
            var Paragraph = document.createElement("p")
            var D = Data[i]
            var TextString = "ID:".concat(D.id).concat(" |KM stand: ").concat(D.KMStand).concat(" |Begin/eind punt: ").concat(D.BeginEindPunt).concat(" |Getankt: ").concat(D.Getankt).concat(" |Tijd: ").concat(D.Time)
            var Node = document.createTextNode(TextString)
            Paragraph.appendChild(Node)
            document.getElementById("Data").appendChild(Paragraph)
        }
    })
    setTimeout(() =>{
    $.getJSON(BaseUrl + '/api/car/getMileage').then(Data =>{
        document.getElementById("Mileage").innerHTML = Data["Mileage"]
        console.log(Data["Mileage"])
    })}, 1000)
}

function submitMilage(){
    KM = parseInt(document.getElementById('KM').value)
    BeginEndPoint = String(document.getElementById('BeginEndPoint').value)
    Tanked = parseInt(document.getElementById('Tanked').value)
    json = {"KMStand":KM, "BeginEindPunt":BeginEndPoint, "Getankt":Tanked}
    PostToUrl(json, BaseUrl + '/api/car/addNew')
}
