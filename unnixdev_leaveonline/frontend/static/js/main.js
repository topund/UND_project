// const main_url = "http://127.0.0.1:3200"

function findDuplicate(data) {
    var temp = {}
    temp[data[0][0][1]] = {}
    temp[data[0][0][1]]["total"] = 1
    temp[data[0][0][1]]["data"] = [data[0]]

    temp[data[0][0][1]]["dep"] = {}
    temp[data[0][0][1]]["dep"] = [data[0][1][1]]
    temp[data[0][0][1]]["dep"][data[0][1][1]] = [data[0][1][1], 1]


    // temp[data[0][0][1]]["dep"][data[0][1][1]] = {}

    temp[data[0][0][1]]["dep"]["pos"] = {}
    temp[data[0][0][1]]["dep"]["pos"][data[0][2][1]] = [data[0][2][1], 1]
    // temp[data[0][0][1]]["dep"]["pos"][data[0][1][1]][data[0][2][1]] = {}
    // temp[data[0][0][1]]["dep"][data[0][1][1]]["pos"][data[0][2][1]]["result"] =  [data[0][2][1] ,1]


    for (var i = 1; i < data.length; i += 1) {
        if (data[i][0][1] in temp) {
            temp[data[i][0][1]]["total"] += 1
            temp[data[i][0][1]]["data"].push(data[i])

            if (data[i][1][1] in temp[data[i][0][1]]["dep"]) {
                temp[data[i][0][1]]["dep"][data[i][1][1]][1] += 1
            } else {
                temp[data[i][0][1]]["dep"][data[i][1][1]] = [data[i][1][1], 1]
            }
            // debugger
            // debugger
        } else {
            temp[data[i][0][1]] = {}
            temp[data[i][0][1]]["total"] = 1
            temp[data[i][0][1]]["data"] = [data[i]]
            // debugger
            temp[data[i][0][1]]["dep"] = {}
            temp[data[0][0][1]]["dep"] = [data[i][1][1]]
            temp[data[i][0][1]]["dep"][data[i][1][1]] = [data[i][1][1], 1]

            temp[data[i][0][1]]["dep"]["pos"] = {}
            temp[data[i][0][1]]["dep"]["pos"][data[i][2][1]] = [data[i][2][1], 1]
        }
        // if(data[i][0][1] in temp){
        //     temp[data[i][0][1]]["total"] += 1
        //     temp[data[i][0][1]]["data"].push(data[i]) 

        // }
    }

    return temp

}

function testSSS(data) {
    var d = []
    for(i in data){
        var temp = []
        for(j in data[i]){
            temp.push(data[i][j][1])
        }
        d.push(temp)
    }
    debugger
    var x = [{
        namePolicy: "ลากิจ",
        total_policy: "5",
        department: [
            {
                name: "programmer",
                total: "3",
                position: [
                    {
                        name: "junior",
                        total: "1",
                        data: [
                            ["ลากิจ", "programmer", "junior", "3"]
                        ]
                    },
                    {
                        name: "senior",
                        total: "1",
                        data: [
                            ["ลากิจ", "programmer", "senior", "3"]
                        ]
                    },
                    {
                        name: "all",
                        total: "1",
                        data: [
                            ["ลากิจ", "programmer", "all", "3"]
                        ]
                    }
                ]
            }
        ]
    }
    ]

    // for( da of d){
    //     if(x["name"]){}
    // }
            
    //     }
    // }
    // var y = [
    //     {
    //         namePolicy: "ลากิจ",
    //         total_policy: "9",
    //         department: {
    //             total : 3
    //                 {}
    //         }
    //     }
    // ]    
    var x = [{
        namePolicy: "ลากิจ",
        total_policy: "5",
        department: [
            {
                name: "programmer",
                total: "3",
                position: [
                    {
                        name: "junior",
                        total: "1",
                        data: [
                            ["ลากิจ", "programmer", "junior", "3"]
                        ]
                    },
                    {
                        name: "senior",
                        total: "1",
                        data: [
                            ["ลากิจ", "programmer", "senior", "3"]
                        ]
                    },
                    {
                        name: "all",
                        total: "1",
                        data: [
                            ["ลากิจ", "programmer", "all", "3"]
                        ]
                    }
                ]
            },
            {
                name: "network",
                total: "2",
                position: [
                    {
                        name: "junior",
                        total: "1",
                        data: [
                            ["ลากิจ", "network", "junior", "3"]
                        ]
                    },
                    {
                        name: "senior",
                        total: "1",
                        data: [
                            ["ลากิจ", "network", "senior", "3"]
                        ]
                    }
                ]
            }
        ]
    },
    {
        namePolicy: "ลาป่วย",
        total_policy: "5",
        department: [
            {
                name: "programmer",
                total: "3",
                position: [
                    {
                        name: "junior",
                        total: "1",
                        data: [
                            ["ลาป่วย", "programmer", "junior", "3"]
                        ]
                    },
                    {
                        name: "senior",
                        total: "1",
                        data: [
                            ["ลาป่วย", "programmer", "senior", "3"]
                        ]
                    },
                    {
                        name: "all",
                        total: "1",
                        data: [
                            ["ลาป่วย", "programmer", "all", "3"]
                        ]
                    }
                ]
            },
            {
                name: "network",
                total: "2",
                position: [
                    {
                        name: "junior",
                        total: "1",
                        data: [
                            ["ลาป่วย", "network", "junior", "3"]
                        ]
                    },
                    {
                        name: "all",
                        total: "1",
                        data: [
                            ["ลาป่วย", "network", "senior", "3"]
                        ]
                    }
                ]
            }
        ]
    }
    ]

    var test = []
    var strTest = `<table border=1><tr><th>Policy</th><th>Department</th><th>ตำแหน่ง</th><th>ระยะเวลา</th></tr>`
    for (i in x) {
        var checkP = 0
        for (j in x[i]["department"]) {
            // debugger
            var checkdep = 0
            for (k in x[i]["department"][j]["position"]) {
                var checkpos = 0
                //     // debugger
                for (f in x[i]["department"][j]["position"][k]["data"]) {
                    // test.push("ss")
                    test.push(x[i]["department"][j]["position"][k]["data"][f])
                    //         // debugger
                    strTest += `<tr>`
                    for (t in x[i]["department"][j]["position"][k]["data"][f]) {
                        if(t == 0){
                            if(checkP == 0){
                                checkP += 1
                                strTest += `<td rowspan=${x[i]["total_policy"]}>${x[i]["department"][j]["position"][k]["data"][f][t]}</td>`    
                            }
                            continue
                        }else if(t == 1){
                            if(checkdep == 0){
                                checkdep += 1
                                strTest += `<td rowspan=${x[i]["department"][j]["total"]}>${x[i]["department"][j]["position"][k]["data"][f][t]}</td>`    
                            }
                            continue
                            
                        }
                        else if(t == 2){
                            if(checkpos == 0){
                                checkpos += 1
                                strTest += `<td rowspan=${x[i]["department"][j]["position"][k]["total"]}>${x[i]["department"][j]["position"][k]["data"][f][t]}</td>`
                            }
                            
                            continue
                                
                        }else{
                            strTest += `<td>${x[i]["department"][j]["position"][k]["data"][f][t]}</td>`    
                        }
                        
                    }
                    strTest += `</tr>`
                }
            }
        }
    }
    // testRecur()
    strTest += `</table>`
    return strTest
}
function firstCharUppercase(letter) {
    return `${letter[0].toUpperCase()}${letter.slice(1)}`
}

$(document).ready(function () {
    $(".policy").on("click", function (e) {

        $("#report").hide()
        deletecontent("policy")
        // console.log(`${main_url}/api/get_policys`)
        fetch(`${main_url}/api/get_policys`)
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                data = data["policys"]
                var div_policy = ""
                // console.log(data)
                var totalD = findDuplicate(data)
                var temp = testSSS(data)
                var strTable = `<table class="" border=1>
                    <tr>
                    <th>ประเภทการลา</th><th>แผนก</th><th>ตำแหน่ง</th><th>ระยะเวลา</th>
                    </tr>`

                // for(i in data){
                //     if()
                // }
                x = 0
                for (key in totalD) {
                    for (i in totalD[key]["data"]) {

                        strTable += `<tr>`
                        for (j in totalD[key]["data"][i]) {

                            if (j == 0 && x == 0) {
                                x = 1
                                strTable += `<td rowspan=${totalD[key]["total"]}>${firstCharUppercase(totalD[key]["data"][i][j][1])}</td>`
                                // debugger
                                continue
                            } else if (j == 0) {
                                continue
                            }
                            strTable += `<td>${firstCharUppercase(totalD[key]["data"][i][j][1])}</td>`
                            // totalD[key]["total"] 

                        }
                        strTable += `</tr>`
                    }
                    x = 0
                }
                strTable += `</table>`


                // for (i in data) {
                //     div_policy += `
                //     <div>
                //         <p>
                //             <span class="poliName_${data[i][0][2]}">${data[i][0][1]}</span> 
                //             <span class="poliDep_${data[i][1][2]}">${data[i][1][1]}</span> 
                //             <span class="poliPos_${data[i][2][2]}">${data[i][2][1]}</span> 
                //             <span class="poliNum_${data[i][3][2]}">${data[i][3][1]}</span>
                //         </p>
                //     </div>
                //     `
                // }
                $(".con_policy").hide().html(`<h1 style="margin: 20px 0">นโยบายการลางาน</h1>${strTable} <br>`).fadeIn(200)

            });


    })

    $(".side-menu li").on("click", function () {
        $(this).addClass("activate")
        var now = this
        $(".side-menu li").each(function () {
            if (!(this == now)) {
                $(this).removeClass("activate")
            }
        })
    })


    $(".balckground_detail").on("click", function () {
        $(".detailFade").fadeOut(500)
    })

    $(".approvepaper").on("click", function (e) {
        $("#report").hide()
        var username = $("#username_").text()
        deletecontent("approvepaper")


        var staffID = username
        var iframe = `https://docs.google.com/forms/d/e/1FAIpQLSfQYEmVaeE3gCTDyyfkzhEPIR2lZrFqXvAQ4ISyWmQBkmrUdw/viewform?embedded=true&entry.1829276584=${staffID}`

        divC = `<div class="test1 googleS" style=
            "top: 40px;
            z-index : 1;
            position : absolute;
            left: 50%;
            transform: translate(-50%,0);">

            <iframe src=${iframe} width="640" height="1105" frameborder="0" marginheight="0" marginwidth="0">กำลังโหลด...</iframe>
        </div>`

        $(".con_approvepaper").html(`${divC}`)
        $(".googleS").show()
    })
    $(".status").on("click", function (e) {
        $("#report").show()
        deletecontent("status")
        // $(".con_status").html("<h1>STATUS</h1>")
        reportFn(`${main_url}/api/report`, $("#username_").attr("pkid"))
    })
    $(".supermode").on("click", function (e) {
        $("#report").hide()
        deletecontent("supermode")
        // $(".con_supermode").append("<h1>SUPERVISOR MODE</h1>")

        $(".con_supermode").html("<h1>ผู้ควบคุมงาน</h1><div id='waitapprove'></div><div id='cover'></div>")

        if ($("#department_").text() == "human resource") {
            genSuper_HR("get_coverall", "hrApprove")
        } else {
            genSuper_HR("get_coverofsuper", "suppervisorApprove")
        }
        // if()
    })


    $(document).ready(function () {
        $(".balckground_opa").on("click", () => {
            console.log("ssssss")
            $(".googleS").hide()
        })

    })

})

// $(document).on("click", ".side-menu li", function(){
//     debugger
//     alert("ssssssss")

// })

$(document).on('click', '#sss', function () {
    alert("SSSSSSS")
})

function genSuper_HR(linkStaff, linkApprove) {
    fetch(`${main_url}/api/${linkStaff}`, {
        method: "post",
        body: JSON.stringify(
            {
                "get_cover": true,
                "userpk": $("#username_").attr("pkid")
            }
        )
    })
        .then(function (res) {
            return res.json()
        }).then(function (data) {
            if (data["status"] == false) {
                return
            }

            var cover = getCoverStaff(data["result"])
            $("#cover").append(cover)



        })

    fetch(`${main_url}/api/${linkApprove}`, {
        method: "post",
        body: JSON.stringify({
            "get_listApprove": true,
            "userpk": $("#username_").attr("pkid")
        })
    }).then(function (res) {
        return res.json()
    }).then(function (data) {
        if (data["status"] == false) {
            return
        }
        var superApprove = getSuperapprove(data["results"])

        $("#waitapprove").append(superApprove)

        whenApprove()
    })
}

function deletecontent(now) {
    var arr = ["policy", "approvepaper", "status", "supermode"]
    for (val of arr) {
        if (val == now) continue;
        $(`.con_${val}`).empty()
    }
}

function getCoverStaff(data) {
    if (data.length == 0) {
        var str = `
        <h3>พนักงานในการควบคุม</h>
        <div style="
        text-align: center;
        font-style: italic;
        ">ไม่มีรายการ</div>
        `
        return str
    }
    var keys = Object.keys(data[0])
    
    var str = `
    <div>
    <h3>พนักงานในการควบคุม</h3>
    <table border="1">
        <tr>
        `
    for (var i = 0; i < keys.length - 1; i ++){
        str += `<th>${changeCharactor(keys[i])}</th>`
    }
    debugger
    for (var i = 0; i < data[0][keys[keys.length-1]].length ; i ++){
        str += `<th>${data[0][keys[keys.length-1]][i][0]}</th>`
    }
    str += `</tr>`
    for(d of data){
        str += `<tr>`
        for( i_k in keys){
            if(keys[i_k] == "remain"){
                
                debugger
                for(var i = 0; i < d[keys[keys.length-1]].length ; i ++){
                    str += `<td>${d[keys[keys.length-1]][i][1]}</td>`
                }
                continue
            }
            str += `<td>${d[keys[i_k]]}</td>`
        }
        str += `</tr>`
        
    }
    // for (val of data) {
    //     str += `
    //             <tr>
    //                 <td>${val.id}</td>
    //                 <td>${val.username}</td>
    //                 <td>${val.email}</td>
    //                 <td>${val.dep}</td>
    //                 <td>${val.pos}</td>
    //                 <td>${val["remain"][0][1]}</td>
    //                 <td>${val["remain"][1][1]}</td>
    //                 <td>${val["remain"][2][1]}</td>
    //             </tr>
    //     `
    // }
    str += `
        </table>
        <div/>
    `
    return str
}

function getSuperapprove(data) {
    if (data["result"].length == 0) {
        var str = `
        <h3>รอการอนุมัติ</h3>
        <div style="
        text-align: center;
        font-style: italic;
        ">ไม่มีรายการ</div>
        `
        return str
    }
    var str = `
    <h3>รอการอนุมัติ</h3>
    <table border="1"><tr>
    `
    for (d of data["keys"]) {
        str += `<th>${changeCharactor(d)}</th>`
    }

    str += `<th>ระยะเวลา</th><th></th></tr>`
    debugger
    for (d of data["result"]) {
        str += `<tr>`
        for (i in d) {
            try{
                str += `<td>${d[i].split(" ")[0]}</td>`
            }
            catch(err) {
                str += `<td>${d[i]}</td>`
              }
        }
        str += `
            <td>${remainDate(d[4], d[5])}</td>
            <td>
                <input style="width: 40%;background: #90EE90;" class="approve_but" type="button" idhist="${d[0]}" value="อนุมัติ">
                <input style="width: 40%;background: #F08080;" class="reject_but" type="button" idhist="${d[0]}" value="ไม่อนุมัติ">
            </td></tr>`
    }
    str += `</table>`
    return str
}

function remainDate(start, end) {
    var date1 = new Date(start)
    var date2 = new Date(end)
    var result = date2 - date1
    return parseInt(result / 1000 / 60 / 60 / 24) + 1
}

function whenApprove() {
    $(`.approve_but`).on("click", function () {
        // debugger
        // alert("ssss")
        var idhist = $(this).attr("idhist")
        var iduser = $("#username_").attr("pkid")

        approve_reject(true, idhist, iduser)
    })
    $(`.reject_but`).on("click", function () {
        // debugger
        // alert("xxxxxx")
        var idhist = $(this).attr("idhist")
        var iduser = $("#username_").attr("pkid")
        approve_reject(false, idhist, iduser)
    })
}
function approve_reject(isApprove, idhist, iduser) {
    $(".balckground_approve").fadeIn(300)
    $(".balckground_approve img").fadeIn(300)

    fetch(`${main_url}/api/approve_reject`, {
        method: "post",
        body: JSON.stringify({
            "isApprove": isApprove,
            "id_hist": idhist,
            "id_user": iduser
        })
    }).then((res) => res.json()).then(function (data) {

        $(".con_supermode").empty()
        $(".con_supermode").html("<h1>ผู้ควบคุมงาน</h1><div id='waitapprove'></div><div id='cover'></div>")

        if ($("#department_").text() == "human resource") {
            genSuper_HR("get_coverall", "hrApprove")
        } else {
            genSuper_HR("get_coverofsuper", "suppervisorApprove")
        }
        $(".balckground_approve").fadeOut(300)
        $(".balckground_approve img").fadeOut(300)
    })
}

function reportFn(url, user_id) {
    fetch(url, {
        method: "post",
        body: JSON.stringify({
            "getReport": true,
            "user_id": user_id
        })
    }).then((res) => res.json())
        .then((data) => {
            // debugger
            if (data["status"]) {
                // var tablereport_myself = genreport_myself(data["myself"])
                var tablereport = genreport_HR_SUP(data["all"])
                // var heatmap = `<div id="heatmap"></div>`
                // var heatmap_div = $('<div>').appendTo();
                // heat
                $(".report_head").show()
                var heatChart = heatMap(data["heatgraph"], "heatmap_div")
                $(".con_status").html(tablereport)
            }
        })
}

function genreport_HR_SUP(data) {
    var str = `
        <h4 style="display: inline;">รายชื่อ</h4>
        <button val="hide" id="hide_table_report">ซ่อนตาราง</button>
        <table style="margin-top: 10px" id="reportTable" border=1><tr>
    `
    for (k of data["keys"]) {
        str += `<th>${changeCharactor(k)}</th>`
    }
    str += `<th></th></tr>`

    for (d of data["data"]) {
        str += `</tr>`
        for (i in d) {
            if(i == 1){
                str += `<td>${d[i]}</td>`    
                continue
            }
            str += `<td>${firstCharUppercase(d[i])}</td>`
        }
        str += `<td><input class="but_detail" type="button" value="รายละเอียด" val=${d[0]}></td></tr>`
    }

    return str
}

function changeCharactor(text){
    if(text == "username"){
        return "ชื่อผู้ใช้งาน"
    }else if(text == "email"){
        return "อีเมล"
    }else if(text == "depatment" || text == "department"){
        return "แผนก"
    }else if(text == "position"){
        return "ตำแหน่ง"
    }else if(text == "polycy" || text == "policy"){
        return "ประเถท"
    }else if(text == "leave_begin" || text == "leaveday begin"){
        return "วันเริ่มต้น"
    }else if(text == "id_hist"){
        return "เลขประวัติ"
    }else if(text == "leave_end" || text == "leaveday end"){
        return "วันสิ้นสุด"
    }else if(text == "explanation"){
        return "เหตุผล"
    }else if(text == "supervisor"){
        return "หัวหน้างาน"
    }else if(text == "human resource"){
        return "HR"
    }else if(text == "status"){
        return "สถานะการลา"
    }else if(text == "duration"){
        return "ระยะเวลา"
    }else if(text == "id histrory"){
        return "id"
    }else if(text == "approve"){
        return "อนุญาติ"
    }else if(text == "reject"){
        return "ไม่อนุญาติ"
    }else if(text == "wait"){
        return "กำลังดำเนินการ"
    }
    else{
        return text
    }
}
$(document).on("click", "#hide_table_report", function () {
    // $("#reportTable").toggle()
    if ($(this).attr("val") == "hide") {
        $(this).attr("val", "show")
        $(this).text("แสดงตาราง")
        $("#reportTable").fadeOut(200);
    } else {
        $(this).attr("val", "hide")
        $(this).text("ซ่อนตาราง")
        $("#reportTable").fadeIn(200)
    }
    // debugger
})

$(document).on("click", ".but_detail", function () {
    var name = $(this).attr("val")
    get_detail_report(name)
})

function get_detail_report(name) {
    fetch(`${main_url}/api/get_detail`, {
        method: "post",
        body: JSON.stringify({ "username": name })
    }).then(res => res.json())
        .then(function (data) {
            if (data["status"] != true) {
                alert("Error")
                return
            }
            chart(data["bar_chart"])
            var divdetail = gen_page_detail(data)
            debugger
            $(".content_detail_modal").fadeIn(500)
            // var con_detail = document.querySelector(".content_detail")
            debugger

            $(".content_ddd").html(divdetail)

            // $(".detailFade").fadeOut(500)

            // $(".content_detail").
        })
}
$(document).on("click", ".close-modal", function(){
    $(".content_detail_modal").fadeOut(200)
})
function gen_page_detail(data) {
    // debugger
    var divstr = `
        <div>
            <p>ชื่อผู้ใช้งาน : ${data["myself"]["username"]}</p>
            <p>แผนก : ${firstCharUppercase(data["myself"]["dep_name"])}</p>
            <p>ตำแหน่ง : ${firstCharUppercase(data["myself"]["pos_name"])}</p>
        </div><h2>จำนวนวันลาที่เหลือ</h2>
        <table border="1">
    `
    var th = `<tr>`
    var td = `<tr>`
    for (d of data["myself"]["remain_list"]) {
        th += `<th>${d[0]}</th>`
        td += `<td>${d[1]}</td>`
    }

    divstr += `${th}</tr>${td}</tr></table> <h2>ประวัติการลา</h2>`
    if (data["hist"]["data"].length == 0) {
        divstr += `<div style="
        text-align: center;
        font-style: italic;
        ">ไม่มีรายการ</div>`
        return divstr
    }
    divstr += `<table style="margin-bottom: 20px"  border="1"><tr>`

    for (k of data["hist"]["keys"]) {
        if(k == "username"){
            continue
        }
        divstr += `<th>${changeCharactor(k)}</th>`
    }

    divstr += `<th>ระยะเวลา</th></tr>`
    for (d of data["hist"]["data"]) {
        
        divstr += `<tr>`
        for (i in d) {
            if(i == 1){
                continue
            }
            
            if(i == 4 || i == 3){
                divstr += `<td>${changeCharactor(d[i]).split(" ")[0]}</td>`
                continue
            }
            divstr += `<td>${changeCharactor(d[i])}</td>`
        }
        divstr += `<td>${remainDate(d[3], d[4])}</td></tr>`
    }
    divstr += `</table>`
    debugger

    return divstr
}

function genreport_myself(data) {
    var str = `<h4>report myself</h4>
        <p>Username : ${data["username"]}</p>
        <p>Department : ${data["dep_name"]}</p>
        <p>Position : ${data["pos_name"]}</p>
        <h5>Remain Leaveday<h5>
        <table border=1>
    `
    var th = `<tr>`
    var td = `<tr>`
    for (d of data["remain_list"]) {
        th += `<th>${d[0]}</th>`
        td += `<td>${d[1]}</td>`
    }

    str += `${th}</tr>${td}</tr></table>`


    return str
}

function chart(dataChart) {
    var chart = Highcharts.chart('barchart', {
        chart: {
            type: 'column'
        },
        title: {
            text: dataChart['title']
        },
        xAxis: {
            categories: dataChart['xlegend']
        },
        yAxis: [{
            min: 0,
            title: {
                text: ''
            }
        }, {
            title: {
                text: dataChart['ylegend']
            },
            opposite: false
        }],

        credits: {
            enabled: false
        },
        legend: {
            shadow: false
        },
        tooltip: {
            shared: true
        },
        plotOptions: {
            column: {
                grouping: false,
                shadow: false,
                borderWidth: 0
            }
        },
        series: [{
            name: 'maximum',
            color: 'rgba(248,161,63,1)',
            data: dataChart['series']['maximum'],
            tooltip: {
                valueSuffix: ' ' + dataChart['unit']
            },
            pointPadding: 0.3,
            pointPlacement: 0,
            yAxis: 1
        }, {
            name: 'remaining',
            color: 'rgba(186,60,61,.9)',
            data: dataChart['series']['remain'],
            tooltip: {
                valueSuffix: ' ' + dataChart['unit']
            },
            pointPadding: 0.4,
            pointPlacement: 0,
            yAxis: 1
        }]
    });

    return chart
}

function heatMap(dataChart, container) {
    // debugger
    var chart = Highcharts.chart({

        chart: {
            renderTo: container,
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
            plotBorderWidth: 1
        },
        credits: {
            enabled: false
        },

        title: {
            text: dataChart['title']
        },

        xAxis: {
            categories: dataChart['xlegend']
        },

        yAxis: {
            categories: dataChart['ylegend'],
            title: null
        },

        colorAxis: {
            min: 0,
            max: 100,
            minColor: '#FFFFFF',
            maxColor: '#FF0000'
        },

        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280
        },

        tooltip: {
            formatter: function () {
                // debugger
                return '<b>' + this.series.xAxis.categories[this.point.x] + '<br><b>' + 'user : ' + this.series.yAxis.categories[this.point.y] + '<br></b>leave : ' +
                    this.point.value + '</b> % <br><b>';
            }
        },

        series: [{
            name: dataChart['series']['name'],
            borderWidth: 1,
            data: dataChart['series']['data'],
            dataLabels: {
                enabled: true,
                color: '#000000'
            }
        }]

    });
    return chart
}