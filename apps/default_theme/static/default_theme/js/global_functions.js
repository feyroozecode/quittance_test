
initSelect2 = function(){
    $('.select').select2({
        placeholder: 'Select an option',
        width: "100%",
        allowClear: true
    }).change(function(){
       try {
         $(this).valid();
       } catch (error) {
            console.log(error)
       }
    });
}

function getAge(dateString, from=null) {
    var today = new Date();

    console.log("from ===> ",  from)
    if(from != null){
        today = new Date(from);
    }

    var birthDate = new Date(dateString);
    console.log("birthDate", birthDate, dateString)
    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}



function getGrades(){
    age = getAge($("#id_date_naissance").val())
    gradeCat = "g18";
    if(age < 18){
        gradeCat = "l18"
    }
    $.ajax({
        type: "get",
        url: "/fnt/api/custum_filter?ajax=grades&cat="+gradeCat,
        dataType: "json",
        success: function(data){

            $("#id_grade").html("");
            if(data.length > 1) {
               $("#id_grade").html("<option value='0'>Choisissez</option>");
            }

            data.forEach((d)=>{
               $("#id_grade").append("<option value='"+d["id"]+"'>"+ d["nom"] +"</option>");
            });
        },
        error: function(){
            
        }
    });
}
 
function getLigues(){
    $.ajax({
        type: "get",
        url: "/fnt/api/custum_filter?ajax=ligues",
        dataType: "json",
        success: function(data){

            $("#id_ligue").html("");
            $("#id_club").html("");
            if(data.length > 1) {
               $("#id_ligue").html("<option value='0'>Choisissez</option>");
            }else{
                console.log(data)
                getDistrict(data[0]["id"])
            }

            data.forEach((d)=>{
               $("#id_ligue").append("<option value='"+d["id"]+"'>"+ d["nom"] +"</option>");
            });
        },
        error: function(){
            
        }
    });
}

function getDistrict(ligue){
    $("#id_club").html("");
    $("#id_districte").html("");
    if(ligue > 0){
        $.ajax({
            type: "get",
            url: "/fnt/api/custum_filter?ajax=districtes&ligue="+ligue,
            dataType: "json",
            success: function(data){
                $("#id_districte").html("");
                $("#id_club").html("");

                if(data.length > 1) {
                    $("#id_districte").html("<option value='0'>Choisissez</option>");
                }else{
                    getClubs(data[0]["id"])
                }

                data.forEach((d)=>{
                    $("#id_districte").append("<option value='"+d["id"]+"'>"+ d["nom"] +"</option>");
                });

                initSelect2()
            },
            error: function(){
                
            }
        });
    }
}

function getClubs(districte){
    if(districte > 0){
        $.ajax({
            type: "get",
            url: "/fnt/api/custum_filter?ajax=clubs&districte="+districte,
            dataType: "json",
            success: function(data){
                $("#id_club").html("");
                if(data.length > 1) {
                    $("#id_club").html("<option value='0'>Choisissez</option>");
                }

                data.forEach((d)=>{
                    $("#id_club").append("<option value='"+d["id"]+"'>"+ d["nom"] +"</option>");
                });

                initSelect2()
            },
            error: function(){
                
            }
        });
    }
}




var newBarcode = function() {
    $("#qrCodeImg").JsBarcode(
        $("#cardLicenceId").text(),
        {
          "format": "CODE128",
          "background": "#FFF",
          "lineColor": "#000",
          "height": 20,
          "width": 100,
          "margin": 0,
          "displayValue": false
        }
    );
};