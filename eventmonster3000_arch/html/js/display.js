subscribe(listenToMedia,'displayMedia','Media')
function listenToMedia(value){
    var type = value[0]
    var path = value[1]
    var ifauto = value[2]
    var videoWrap = document.getElementById('video-display-wrap')
    var video = document.getElementById('thevideo')
    var source = document.getElementById('thevideosource')
    var imgWrap = document.getElementById('image-display-wrap')
    var img = document.getElementById('theimg')
    if(type=='video'){
        imgWrap.style.display= 'none'
        videoWrap.style.display = 'block'
        source.setAttribute('src',path)
        video.load()
        video.oncanplay = function(){
            console.log('playing')
            video.play()
        }
        video.onended = function(){
            videoWrap.style.display = 'none'
            imgWrap.style.display = 'block'
            if(ifauto){
                getData('gotoNext',function(value){
                    console.log(value)
                    sendSignal('gotoNext',value+1)
                })
            }
        }
    }else{
        imgWrap.style.display= 'block'
        videoWrap.style.display = 'none'
        img.setAttribute('src',path)
        video.pause()
    }
}