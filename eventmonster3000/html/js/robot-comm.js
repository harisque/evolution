function subscribe(callbackFunc,param){
    QiSession(function (session) {
        console.log(param+' Subscriber Connected')
        session.service("ALMemory").then(function (ALMemory) {
            ALMemory.subscriber(param).then(function (subscriber) {
                subscriber.signal.connect(function (value) {
                    console.log('Parameter '+param+' value changed to:: '+value)
                    callbackFunc(value)
                })
            })
        })
    },function(){
        console.log(param+' Subscriber Disconnected')
    })
};
function unsubscribe(param){
    QiSession(function (session) {
        console.log(param+' Subscriber Disconnected')
        session.service("ALMemory").then(function (ALMemory) {
            ALMemory.removeData(param)
        })
    },function(){
        console.log(param+' Subscriber Disconnected')
    })
};
function sendSignal(eventName,value){
    QiSession(function (session) {
        console.log('Send Signal to '+eventName+':: '+value);
        session.service("ALMemory").then(function(ALMemory){
            ALMemory.raiseEvent(eventName,value)
        }), function(error){
            console.log('An error occurred', error)
        }
    }, function () {
        console.log('Signal Lost');
    });
};
function getParameter(serv,param,func){
    QiSession(function(session){
        session.service(serv).then(function(service){
            service.getParameter(param).then(function(value){
                console.log('Getting Parameter '+param+' from '+serv+' :'+value)
                func(value)
            })
        })
    },function(){
        console.log(serv + ' Disconnected')
    })
};
function setParameter(serv,param,val){
    QiSession(function(session){
        console.log('Setting Parameter '+param+' from '+serv+' to '+val)
        session.service(serv).then(function(s){
            s.setParameter(param,val)
        })
    },function(){
        console.log(serv + ' Disconnected')
    })
};
function getData(eventName,func){
    QiSession(function (session) {
        session.service("ALMemory").then(function(ALMemory){
            ALMemory.getData(eventName).then(function(value){
                console.log('Getting Data From '+eventName+' :'+value);
                func(value)
            })
        }), function(error){
            console.log('An error occurred', error)
        }
    }, function () {
        console.log('disconnected');
    });
};
function stopRobotSpeech(){
    QiSession(function(session){
        console.log('Robot Speech Stop');
        session.service("ALAnimatedSpeech").then(function(aas){
            aas._stopAll(true)
        }, function (error) {
            console.log("An error occurred:", error);
        });
        session.service("ALTextToSpeech").then(function(tts){
            tts.stopAll()
        }, function (error) {
            console.log("An error occurred:", error);
        })
    }, function () {
        console.log('disconnected');
    });
};
function robotSay(text){
    QiSession(function (session) {
        console.log('connected');
        session.service("ALAnimatedSpeech").then(function (ass) {
            ass.say(text)
        }, function (error) {
            console.log("An error occurred:", error);
        });
    }, function () {
        console.log('disconnected');
    });
};