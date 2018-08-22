init()
function init(){
    $.ajax({
        url:"data/data.json",
        type:"GET",
        dataType:"json",
        error: function(xhr,error){
            alert(xhr);
            alert(error)
        },
        complete:function(response){
            console.log('Got Data');
            mydata = response.responseJSON;
            var components = {};
            var app = createApp(mydata,components);
            subscribe(listenToBattery,"BatteryChargeChanged",'Battery')
        }
    });
};
function listenToBattery(value){
    app.__vue__._data.battery=value+'%';
    return value
};
function createApp(mydata,components){
    return new Vue({
        el: '#app',
        data: {
            instantSpeech:"",
            language:'',
            volume:'100%',
            battery:'',
            poses:mydata.poses,
            speech:mydata.speech,
            moves:mydata.moves,
            robotapps:mydata.apps,
            media:mydata.media,
            auto:mydata.automaton,
            moveX:0,
            moveY:0,
            moveTheta:0,
            speechSpeed:0
        },
        components: createComponents(mydata, components),
        mounted:function(){
            var getBattery = function(value){app.__vue__._data.battery=value+'%'}
            var getLang = function(value){app.__vue__._data.language=value}
            var getSpeechSpeed = function(value){app.__vue__._data.speechSpeed=value}
            var getVolume = function(value){app.__vue__._data.volume=value+'%'}
            getData("initBattery",getBattery)
            getData("setLang",getLang)
            getParameter('ALTextToSpeech','defaultVoiceSpeed',getSpeechSpeed)
            getData('volumeLevel',getVolume)
        },
        computed:{
            ifChn:function(){
                return this.language=='CHN'
            },
            speechDisplay:function(){
                result = []
                this._data.speech.forEach(function(el){
                    result.push(el.length<30?el:el.substr(0,30)+'...('+el.length+')')
                })
                return result
            }  
        },
        methods: {
            runApp:function(){
                console.log('switch')
                sendSignal('switchFocus',event.target.getAttribute('path'))
            },
            changeSpeechSpeed:function(){
                sendSignal('speechSpeed',parseFloat(app.__vue__._data.speechSpeed))
                //setParameter('ALTextToSpeech','defaultVoiceSpeed',parseFloat(app.__vue__._data.speechSpeed))
            },
            stopSpeech:function(){
                sendSignal('stopAuto',1)
                stopRobotSpeech()
            },
            changeLang:function(){
                this.language = this.language=='CHN'?'ENG':'CHN';
                sendSignal('setLang',this.language)
            },
            volUp:function(){
                vol = parseFloat(this.volume);
                vol = vol>=95?100:vol+5;
                this.volume = (vol).toString()+"%";
                sendSignal('volumeLevel',vol)
            },
            volDown:function(){
                vol = parseFloat(this.volume);
                vol = vol<=5?0:vol-5;
                this.volume = (vol).toString()+"%";
                sendSignal('volumeLevel',vol)
            },
            makeMove:function(){
                console.log(event.target.getAttribute('path'))
                sendSignal('makeMove',event.target.getAttribute('path'))
            },
            moveTo:function(){
                var result = []
                var param = event.target.getAttribute('param')
                var l = param.split(',')
                l.forEach(function(el){
                    result.push(parseFloat(el))
                })
                sendSignal('moveTo',result)
            },
            customMove:function(){
                var x = parseFloat(this._data.moveX);
                var y = parseFloat(this._data.moveY);
                var th = parseFloat(this._data.moveTheta);
                sendSignal('moveTo',[x,y,th])
            },
            sayInstantSpeech:function(){
                sendSignal('speechFromHouston',this._data.instantSpeech)
            },
            sayTag:function(){
                var i = this.speechDisplay.indexOf(event.target.innerHTML)
                sendSignal('speechFromHouston',this._data.speech[i])
            },
            playMedia:function(){
                //type,path,if_auto
                sendSignal('displayMedia',[event.target.getAttribute('type'),event.target.getAttribute('path'),false])
            },
            autoPlay:function(){
                var autoName = event.target.getAttribute('name')
                for(i=0;i<this._data.auto.length;i++){
                    if(this._data.auto[i]['name']==autoName){
                        auto = this._data.auto[i]
                        break
                    }
                }
                var content = auto['content']
                sendSignal('setLang',auto['language'])
                this._data.language=auto['language']
                sendSignal('speechSpeed',parseFloat(auto['speechSpeed']))
                //setParameter('ALTextToSpeech','defaultVoiceSpeed',parseFloat(auto['speechSpeed']))
                this._data.speechSpeed=auto['speechSpeed']

                var pulse = function(value){
                    var i = value;
                    if (i < content.length){
                        var item = content[i]
                        sendSignal('displayMedia',[item['media']['type'],item['media']['path'],true])
                        sendSignal('speechFromHouston',item['speech'])
                        item.hasOwnProperty('pose')?sendSignal('makeMove',item['pose']['path']):null;
                    }
                    else{
                        sendSignal('stopAuto',1)
                        //unsubscribe('gotoNext')
                    }
                }
                sendSignal('gotoNext',0)
                subscribe(pulse,'gotoNext')
                pulse(0)
            },
            search:function(type,key){
                datamap={
                    'poses':mydata.poses,
                    'speech':mydata.speech
                }
                searchSet = datamap[type];
                result = [];
                if(key!=''){
                    searchSet.forEach(function(el){
                        if (el.indexOf(key)!=-1){result.push(el)}
                    });
                }else{
                    result = searchSet
                }
                this._data[type]=result
            }
        }
    });
};
function createGroup(){
    group = {
        template:'#group',
        computed:{
            foldButton:function(){
                return this._data.iffold?'+':'-'
            },
            foldClass:function(){
                return this._data.iffold?'to-expand':'to-collapse'
            }
        },
        methods:{
            filter:function(){
                this.$emit('search',this._data.name,this._data.searchKey)
            },
            fold:function(){
                this._data.iffold = this._data.iffold?false:true
            }
        }
    }
    return group
}
function createAutomaton(){
    auto = createGroup()
    auto.data = function(){
        return{
            header:'Automaton',
            banSearch:true,
            searchKey:'',
            iffold:false
        }
    };
    return auto;
}
function createMotion(){
    motion = createGroup()
    motion.data = function(){
        return{
            header:'Motion',
            banSearch:true,
            searchKey:'',
            iffold:false
        }
    };
    return motion;
}
function createRobotApps(){
    robotapps = createGroup()
    robotapps.data = function(){
        return{
            header:'Applications',
            banSearch:true,
            searchKey:'',
            iffold:false
        }
    };
    return robotapps;
}
function createPoses(){
    poses = createGroup()
    poses.data = function(){
        return {
            name:'poses',
            header:'Animation',
            banSearch:false,
            searchKey:'',
            iffold:false
        }
    };
    return poses;
}
function createSpeech(){
    speech = createGroup()
    speech.data = function(){
        return {
            name:'speech',
            header:'Speech',
            banSearch:false,
            searchKey:'',
            iffold:false
        }
    };
    return speech;
}
function createMedia(){
    media = createGroup()
    media.data = function() {
        return {
            name:'media',
            header:'media',
            banSearch:false,
            searchKey:'',
            iffold:false
        }
    };
    return media;
}
function createComponents(data,components){
    components['motion']=createMotion();
    components['poses']=createPoses();
    components['speech']=createSpeech();
    components['robotapps']=createRobotApps();
    components['media']=createMedia()
    components['auto']=createAutomaton()
    return components
}

function jumpToView(key){
    app.__vue__.selfChangeView(key)
};
function callGoBack(){
    app.__vue__.goBack()
};
function hideLinks(){
    app.__vue__.hideLinks()
};
function showLinks(){
    app.__vue__.showLinks()
}