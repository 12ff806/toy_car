/*
 * Motor Car Control Panel
 * by --
 * create: June 27 2018
 * last modify: June 28 2018
 */
function recording(blob){
    var uphttp = new XMLHttpRequest();
    var formData = new FormData();//注意和上面的input标签中onclick对比你发现了什么
    formData.append('audio', blob);
    uphttp.open('POST', 'https://*.*.*.*/voiceapi/stt', true);
    uphttp.onreadystatechange=function(){
        if(uphttp.readyState==4&&uphttp.status==200){
            var responseText = JSON.parse(uphttp.responseText);
            if(responseText.code == 0 && responseText.text !=null){
                forward(responseText.text);
            }else{
                forward(responseText.text);
            }

        }
    }
//          uphttp.setRequestHeader('Content-type', 'multipart/form-data;charset=utf-8');
    //这里不需要再填写，默认就行
    uphttp.send(formData);
    //发送数据
}

function __log(e, data) {
    log.innerHTML += "\n" + e + " " + (data || '');
}

var audio_context;
var recorder;

function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    __log('Media stream created.');
    recorder = new Recorder(input);
    __log('Recorder initialised.');
}

function startRecording(button) {
    document.getElementById("audioGoD").style.display = "block"
    recorder && recorder.record();
//    button.disabled = true;
//    button.nextElementSibling.disabled = false;
    __log('Recording...');
}
function stopRecording(button) {
    recorder && recorder.stop();
//    button.disabled = true;
//    button.previousElementSibling.disabled = false;
//    button.nextElementSibling.disabled = false;
    __log('Stopped recording.');
    // create WAV download link using audio data blob
    createDownloadLink();
    recorder.clear();
    document.getElementById("audioGoD").style.display = "none"
}
var blobSudio;
function createDownloadLink() {
    recorder && recorder.exportWAV(function(blob) {
        var url = URL.createObjectURL(blob);
        var li = document.createElement('li');
        var au = document.createElement('audio');
        var hf = document.createElement('a');
        au.controls = true;
        au.src = url;
        hf.href = url;
        hf.download = new Date().toISOString() + '.wav';
        hf.innerHTML = hf.download;
        li.appendChild(au);
        li.appendChild(hf);
        recordingslist.appendChild(li);
        blobSudio =blob;
        recording(blob)
    });
}

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
    xhr.open("POST", "http://192.168.96.130:8080/api/action", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    //xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.send(JSON.stringify({"command": action}));
}


window.onload = function(){
    // 录音
    $("#audioGo").on("touchstart", function(){
        startRecording(this)
    });
    $("#audioGo").on("touchend", function(){
        stopRecording()
    });

    // 前进
    var forwardObj = document.getElementById("btn-n");
    forwardObj.addEventListener("click", function(){forward("N");});

    // 暂停
    var stopObj = document.getElementById("btn-stop");
    stopObj.addEventListener("click", function(){forward("STOP");});

    // 向左走
    var leftObj = document.getElementById("btn-w");
    leftObj.addEventListener("click", function(){forward("W");});

    // 向右走
    var rightObj = document.getElementById("btn-e");
    rightObj.addEventListener("click", function(){forward("E");});

    // 后退
    var backObj = document.getElementById("btn-s");
    backObj.addEventListener("click", function(){forward("S");});

    // 向右前方走
    var neObj = document.getElementById("btn-ne");
    neObj.addEventListener("click", function(){forward("NE");});

    // 向左前方走
    var nwObj = document.getElementById("btn-nw");
    nwObj.addEventListener("click", function(){forward("NW");});

    // 向右后方走
    var seObj = document.getElementById("btn-se");
    seObj.addEventListener("click", function(){forward("SE");});

    // 向左后方走
    var swObj = document.getElementById("btn-sw");
    swObj.addEventListener("click", function(){forward("SW");});

    // 逆时针旋转
    var acwrObj = document.getElementById("btn-acwr");
    acwrObj.addEventListener("click", function(){forward("ACWR");});

    // 顺时针旋转
    var cwrObj = document.getElementById("btn-cwr");
    cwrObj.addEventListener("click", function(){forward("CWR");});

    // 向左前方转向
    var tnwObj = document.getElementById("btn-tnw");
    tnwObj.addEventListener("click", function(){forward("TNW");});

    // 向右前方转向
    var tneObj = document.getElementById("btn-tne");
    tneObj.addEventListener("click", function(){forward("TNE");});

    // 向左后方转向
    var tswObj = document.getElementById("btn-tsw");
    tswObj.addEventListener("click", function(){forward("TSW");});

    // 向右后方转向
    var tseObj = document.getElementById("btn-tse");
    tseObj.addEventListener("click", function(){forward("TSE");});

    // 头部逆时针转
    var tnrlObj = document.getElementById("btn-tnrl");
    tnrlObj.addEventListener("click", function(){forward("TSRL");});

    // 头部顺时针转
    var tnrrObj = document.getElementById("btn-tnrr");
    tnrrObj.addEventListener("click", function(){forward("TSRR");});

    // 尾部逆时针转
    var tsrlObj = document.getElementById("btn-tsrl");
    tsrlObj.addEventListener("click", function(){forward("TNRL");});

    // 尾部顺时针转
    var tsrrObj = document.getElementById("btn-tsrr");
    tsrrObj.addEventListener("click", function(){forward("TNRR");});

    // 自动模式
    var autoObj = document.getElementById("btn-auto");
    autoObj.addEventListener("click", function(){forward("AUTO");});



    try {
        // webkit shim
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
        window.URL = window.URL || window.webkitURL;

        audio_context = new AudioContext;
        __log('Audio context set up.');
        __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
        alert('No web audio support in this browser!');
    }

    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
        __log('No live audio input: ' + e);
    });

}
