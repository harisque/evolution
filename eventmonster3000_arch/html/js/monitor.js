function hexToBase64(str) {
    return btoa(String.fromCharCode.apply(null, str.replace(/\r|\n/g, "").replace(/([\da-fA-F]{2}) ?/g, "0x$1 ").replace(/ +$/, "").split(" ")));
}
function showImg(value){
    //imgHex = value
    //console.log(imgHex)
    var img = document.createElement('img')
    //img.src = value
    var result = "";
    for(var i = 0;i<value.length;i++){
        result += String.fromCharCode(parseInt(value[i],2))
    }
    img.src = 'data:image/jpeg;base64,'+result
    console.log(img.src)
    document.body.appendChild(img)
}

function getRemoteImg(){
    QiSession(function (session) {
        session.service("ALVideoDevice").then(function(video){
            video.subscribeCamera('subscriberID',0,0,0,1).then(function(subscriber){
                video.getImageRemote(subscriber).then(function(img){
                    console.log(img)
                    var imageData = img[6];
                    //var blob = new Blob(imageData,{type:'image/jpeg'});
                    //var url = URL.createObjectURL(blob)
                    showImg(imageData)

                })
            })
        }), function(error){
            console.log('An error occurred', error)
        }
    }, function () {
        console.log('Signal Lost');
    });
}