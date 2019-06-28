// var mainurl = "http://127.0.0.1:3200"
$(document).ready(function(){
    debugger
    $(".register_form").on("submit",function(e){
        e.preventDefault()
        var url = new URL(window.location.href) 
        var token = url.searchParams.get("token")

        if( !($("#regis_password").val() == $("#regis_againpassword").val()) ){
            alert("Fail")
            return 
        }
        
        var datasend = {
            "password" : $("#regis_password").val(),
            "username" : $("#regis_username").val(),
            "email" : $("#regis_email").val(),
            "token": token
        }
        debugger
        
        fetch(`${main_url}/account/signupLine/`,{
                method: 'POST',
                body: JSON.stringify(datasend)
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if(data["status"]){
                    alert(data["message"])
                    window.location.href=`${main_url}/user/`
                }else{
                    alert(data["message"])
                    // window.location.href=`${main_url}/account/signupPage/`
                }
            })
    })
})
