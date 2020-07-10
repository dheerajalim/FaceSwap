function hand_detection(){

    eel.hand_detection()
        
    }

function gesture_generation(){

    eel.gesture_generation()

    }

function gesture_flips(){

    eel.gesture_flips()

    }

function dump_model(){
    document.getElementById("dumpButton").innerHTML =
        '<i class="fas fa-microchip"></i><span>Processing... Please wait</span>';
    eel.dump_model()(function()
    {document.getElementById("dumpButton").innerHTML = '<i class="fas fa-check"></i><span>Train, Test, Validation Split created</span>';})

    }

function train_model(){
    document.getElementById("trainButton").innerHTML =
        '<i class="fas fa-microchip"></i><span>Processing... Please wait</span>';
    document.getElementById("trainButton").disabled = true;
    document.getElementById('trainButton').style.background = '#696969';
    eel.train_model()(function(accuracy)
    {document.getElementById("trainButton").innerHTML = '<i class="fas fa-check"></i><span>Model Trained</span>';
    const result = `Validation Model Accuracy : ${accuracy} %`
    document.getElementById('val_result').innerHTML = result;
    document.getElementById("trainButton").disabled = false;
    document.getElementById('trainButton').style.background = '#DAA520';
    })

    }

 function test_model(){
    document.getElementById("testButton").innerHTML =
        '<i class="fas fa-microchip"></i><span>Processing... Please wait</span>';
    document.getElementById("testButton").disabled = true;
    document.getElementById('testButton').style.background = '#696969';
    eel.test_model()(function(accuracy)
    {document.getElementById("testButton").innerHTML = '<i class="fas fa-check"></i><span>Model Tested</span>';
    const result = `Test Model Accuracy : ${accuracy} %`
    document.getElementById('test_result').innerHTML = result;
    document.getElementById("testButton").disabled = false;
    document.getElementById('testButton').style.background = '#d34836';
    })

    }

 function predict_gesture(){

    eel.predict_gesture()
 }