/**
 * Created by ironeagle on 4/4/18.
 */

jQuery(document).ready(function ($) {
    REQUEST_MONITOR_SERVICE = {
        'HOST': 'http://' + DJANGO_BASEURL,
        'SERVICE': 'request-monitor'
    };

    var get_service_url = function(path){
        return REQUEST_MONITOR_SERVICE['HOST'] + '/'
            + REQUEST_MONITOR_SERVICE['SERVICE'] + '/'
            + path;
    };

    var make_ajax_setting = function(url, method, payload){
        return {
            "async": true,
            "crossDomain": true,
            "url": url,
            "method": method,
            "processData": false,
            "headers": {
                "Content-Type": "application/json"
            },
            "data": JSON.stringify(payload)
        };
    };

    get_request_monitor_data = function(request_id){
        SERVICE_URL = get_service_url('request/api' + request_id);
        PAYLOAD = {};
        SETTINGS = make_ajax_setting(SERVICE_URL, "GET", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            response_data = response.data;
            console.log(response_data);
            for(i in response_data){
                console.log(response_data[i]);
            }
        });
    };

    load_request_monitor_page = function(request_id){
        SERVICE_URL = get_service_url('request/' + request_id);
        alert(SERVICE_URL);
        window.location.href = SERVICE_URL;
    };

});