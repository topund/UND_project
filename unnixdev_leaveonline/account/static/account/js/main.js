var mainurl = "http://127.0.0.1:3200"
var departmentTemp = 1
var positionTemp = 1
var dataDeandPos = undefined
$(document).ready(function(){
    fetch(`${mainurl}/account/signup/`)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            dataDeandPos = data
            var dep = `<div>Department</div><select class="deparment">`
            for(val of data["department"]){
                dep += `<option id_pk="${val["id"]}">${val["dep_name"]}</option>`
            }
            dep += `</select>`
            $(".regis_department").html(dep)


            var pos = `<div>Position</div><select class="position">`
            for(val of data["position"]){
                pos += `<option id_pk="${val["id"]}">${val["pos_name"]}</option>`
            }
            pos += `</select>`

            $(".regis_position").html(pos)

            
            $(".deparment").on("change", function(){
                for( i of dataDeandPos["department"]){
                    if(i["dep_name"] == $(this).val()){
                        departmentTemp = i["id"]
                    }
                }
                // departmentTemp = $(this).val()
            })
            
            $(".position").on("change", function(){
                for( i of dataDeandPos["position"]){
                    if(i["pos_name"] == $(this).val()){
                        positionTemp = i["id"]
                    }
                }
            })

        });

    $(".register_form").on("submit",function(e){
        e.preventDefault()

        if( !($("#regis_password").val() == $("#regis_againpassword").val()) )
            return 
        
        datasend = {
            "password" : $("#regis_password").val(),
            "nameuser" : $("#regis_username").val(),
            "email" : $("#regis_email").val(),
            "department" : departmentTemp,
            "position" : positionTemp
        }
        
        fetch(`${mainurl}/account/signup/`,{
                method: 'POST',
                body: JSON.stringify(datasend)
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if(data["status"] == "finish"){
                    alert("Register Success")
                    window.location.href=`${mainurl}/user/`
                }else{
                    alert("Register Fail")
                    window.location.href=`${mainurl}/account/signupPage/`
                }
            })
    })
})
