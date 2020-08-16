/*
 * Motor Car Control Panel
 * by --
 * create: June 27 2018
 * last modify: June 28 2018
 */


// xhr
function forward(action){
    // step 1 create xhr object
    var xhr;
    if(window.XMLHttpRequest){    // Mozilla, safari, chrome, IE7+..
        xhr = new XMLHttpRequest();
    }
    else if(window.ActiveXObject){    // IE6 and older
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }

    // step 3 callback
    xhr.onreadystatechange = function(){
        if(xhr.readyState === XMLHttpRequest.DONE){
            if(xhr.status === 200){
                // show the response msg
                var resp = JSON.parse(xhr.responseText);
                rcode = resp.code;
                rmsg = resp.msg;
                console.log(rcode + rmsg)
            }
        }
    }

    // step 2 make request
    xhr.open("POST", "http://192.168.96.168:8080/api/action", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    //xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.send(JSON.stringify({"command": action}));
}


window.onload = function(){
    // 前进
    var forwardObj = document.getElementById("btn-f");
    forwardObj.addEventListener("click", function(){forward("N");});

    // 暂停
    var stopObj = document.getElementById("btn-p");
    stopObj.addEventListener("click", function(){forward("P");});
    
    // 左转
    var leftObj = document.getElementById("btn-l");
    leftObj.addEventListener("click", function(){forward("W");});
    
    // 右转
    var rightObj = document.getElementById("btn-r");
    rightObj.addEventListener("click", function(){forward("E");});
    
    // 后退
    var backObj = document.getElementById("btn-b");
    backObj.addEventListener("click", function(){forward("S");});
    
    // 自动模式
    var autoObj = document.getElementById("btn-auto");
    autoObj.addEventListener("click", function(){forward("AUTO");});
}

