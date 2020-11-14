        TempPoints = {};
        
        function TempInit(){
            for (var i = 0; i<24; i++){
                i = ( (i<10) ? "0".concat(String(i)) : String(i) )
                TempPoints[String(i).concat(":00")] = String(20);
            }
            CreatePlot();
        }
        
        function AddTemp(){
            Time = document.getElementById("Time").value;
            Temp = document.getElementById("Temp").value;
            TempPoints[Time] = Temp;
            CreatePlot()
            T = parseInt(Time.slice(0,2)) + 1;
            T = ( (T<10) ? "0".concat(String(T)) : String(T) );
            T = ( (T>23) ? "00" : T );
            document.getElementById("Time").value = String(T).concat(":00");
        }
        
        function CreatePlot(){
            X = []
            Y = []
            for (TempPoint in TempPoints){
                X.push(TempPoint);
                X.sort()
                Y.splice(X.indexOf(TempPoint), 0, TempPoints[TempPoint]);
            }
            var Trace = {x:X, y:Y, type:'scatter'}
            var Data = [Trace];
            Plotly.newPlot("Plot", Data);
            console.log(X)
            console.log(Y)
        }
