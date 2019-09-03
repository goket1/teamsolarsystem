
console.log("debug ")

function ConvertKMToMeters(km){
    return km * 1000
}
function ConvertForScale(km, scale){
    console.log(km);
    let meters = ConvertKMToMeters(km);
    console.log(km +  " " + meters);
    if(meters !== 0 && scale !== 0){
        console.log(meters / scale);
        return meters / scale;
    }
    else {
        console.log(km +  " " + meters);
        return 0;
    }
}