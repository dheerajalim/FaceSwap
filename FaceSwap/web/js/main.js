
function yesnoCheck(videoradio,videodir,video_output_dir) {
    if (document.getElementById(videoradio).checked) {
        document.getElementById(videodir).style.display = 'block';
        document.getElementById(video_output_dir).required = true;
    }
    else {
        document.getElementById(videodir).style.display = 'none';
        document.getElementById(video_output_dir).required = false;
    }

}

function faceswap_file(source){

    eel.faceswap_file(source)

    }

function start_faceswap(source){
    eel.start_faceswap(source)
        
    }

function settings_page(){
    eel.check_settings()(function (result) {

        if (result){
            window.location.href='settings.html';
        }
    })


}

function load_settings() {
     eel.load_settings()(function(saved_values) {
        console.log(saved_values)
        console.log(`${saved_values}`);
        document.getElementById('face_location_path_value').innerHTML = saved_values[0];
        document.getElementById('image_output_dir_path_value').innerHTML = saved_values[1];
        document.getElementById('dlibmodel').value = saved_values[2];
        document.getElementById('video_output_dir_path_value').innerHTML = saved_values[3];
        if (saved_values[4] == 1){
            document.getElementById('saveimage-1').checked = true;
            document.getElementById('imagedir').style.display = 'block';
            document.getElementById('image_output_dir').required = true;
        }
        else{
            document.getElementById('saveimage-0').checked = true;
        }

        if (saved_values[5] == 1){
            document.getElementById('savevideo-1').checked = true;
            document.getElementById('videodir').style.display = 'block';
            document.getElementById('video_output_dir').required = true;
        }
        else{
            document.getElementById('savevideo-0').checked = true;
        }

    });
}

function save_settings(){

    const face_location_path_value = document.getElementById('face_location_path_value').innerHTML
    const dlibmodel = document.getElementById('dlibmodel').value
    const saveimage = document.querySelector('input[name="saveimage"]:checked').value
    const savevideo = document.querySelector('input[name="savevideo"]:checked').value
    const image_output_dir_path_value = document.getElementById('image_output_dir_path_value').innerHTML
    const video_output_dir_path_value = document.getElementById('video_output_dir_path_value').innerHTML

    console.log(face_location_path_value)
    console.log(dlibmodel)
    console.log(saveimage)
    console.log(savevideo)
    console.log(image_output_dir_path_value)
    console.log(video_output_dir_path_value)

    if (face_location_path_value.length == 0 ){
        document.getElementById('error').innerHTML = " Please select a swap face file";
        document.getElementById('error').style.background= "antiquewhite";
        return
    }
    else {
        document.getElementById('error').innerHTML = "";
        document.getElementById('error').style.background= "";
    }

    if(savevideo == 1){
        if (video_output_dir_path_value.length == 0 ){
        document.getElementById('error').innerHTML = " Please select a Video output directory";
        document.getElementById('error').style.background= "antiquewhite";
        return
        }
        else {
             document.getElementById('error').innerHTML = "";
             document.getElementById('error').style.background= "";
        }
    }

    if(saveimage == 1){
        if (image_output_dir_path_value.length == 0 ){
        document.getElementById('error').innerHTML = " Please select a Image output directory";
        document.getElementById('error').style.background= "antiquewhite";
        return
        }
        else {
             document.getElementById('error').innerHTML = "";
             document.getElementById('error').style.background= "";
    }
    }

    eel.save_settings(face_location_path_value,dlibmodel,image_output_dir_path_value,video_output_dir_path_value, saveimage,savevideo)(
        function(result){
            if (result){
                window.location.href='index.html'
            }
        }
    )

}

function face_location_path(){
    eel.face_location_path()(function(path)
    {
        let result = `${path}`
        console.log(result)
        if (result == ""){
            document.getElementById('face_location_path_value').innerHTML = "";
        }
        else {
            document.getElementById('face_location_path_value').innerHTML = result;
        }
    })
}


function output_dir(path_tag){
    eel.output_dir()(function(path)
    {
        let result = `${path}`
        if (result ==""){
            document.getElementById(path_tag).innerHTML = "";
        }
        else {
            document.getElementById(path_tag).innerHTML = result;
        }
    })
}

