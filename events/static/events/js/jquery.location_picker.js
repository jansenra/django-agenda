google.load("maps", "2");

$(document).unload(function(){
    GUnload();
});
//http://maps.google.com/maps?q=Amsterdam,+The+Netherlands&hl=en&sll=37.0625,-95.677068&sspn=,93.076172&oq=Am&hnear=Amsterdam,+Government+of+Amsterdam,+North+Holland,+The+Netherlands&t=m&z=12
$(document).ready(function(){
    $("input.location_picker").each(function (i) {
        var map = document.createElement('div');
        map.className = "location_picker_map";
        this.parentNode.insertBefore(map, this);
        $(this).css('display','none');

        var lat = 52.374004;
        var lng = 4.890359;
        if (this.value.split(',').length == 2) {
            values = this.value.split(',');
            lat = values[0];
            lng = values[1];
        }
        var center = new GLatLng(lat,lng);

        var map = new google.maps.Map2(map);
        map.addControl(new GSmallMapControl());
        map.setCenter(center, 4);

        this.onMapClick = function(overlay, point) {
            this.value = point.lat()+','+point.lng();
            if (this.marker == null) {
                this.marker = new GMarker(point);
                this.map.addOverlay(this.marker);
            } else {
                this.marker.setPoint(point);
            }
        }

        this.marker = new GMarker(center);
        map.addOverlay(this.marker);

        GEvent.bind(map, "click", this, this.onMapClick);
    });
});
