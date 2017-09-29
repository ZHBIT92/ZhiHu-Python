function get_data(data,city){
var map = new BMap.Map("container");
map.centerAndZoom(new BMap.Point(121.461165,31.234095), 11);

var myAddress = data;
var City = city;
var list={ };
var myGeo = new BMap.Geocoder();

myGeo.getPoint(myAddress, function(point){
if (point) {
    map.centerAndZoom(point, 16);
    map.addOverlay(new BMap.Marker(point));

    myGeo.getLocation(point, function(rs){
            var addComp = rs.addressComponents;
            list =addComp.province + ", " + addComp.city + ", " + addComp.district + ", " + addComp.street + ", " + addComp.streetNumber
    });
}
}, City);
return list;
}
window.onload = myfun;

