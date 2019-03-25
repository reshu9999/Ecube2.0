/**
 * Created by ironeagle on 3/19/18.
 */

jQuery(document).ready(function ($) {
    CRAWLER_OPS_SERVICE = {
        'HOST': 'http://localhost',
        'PORT': '5000',
        'VERSION': 'api/v1'
    };

    var get_service_url = function(path){
        return CRAWLER_OPS_SERVICE['HOST'] + ':'
            + CRAWLER_OPS_SERVICE['PORT'] + '/'
            + CRAWLER_OPS_SERVICE['VERSION'] + '/'
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

    pause_request = function(request_id){
        SERVICE_URL = get_service_url('request/pause');
        PAYLOAD = {'RequestID': request_id};
        SETTINGS = make_ajax_setting(SERVICE_URL, "POST", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
        });
    };

    resume_request = function(request_id){
        SERVICE_URL = get_service_url('request/resume');
        PAYLOAD = {'RequestID': request_id};
        SETTINGS = make_ajax_setting(SERVICE_URL, "POST", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
        });
    };

    reparse_request = function(request_run_id){
        SERVICE_URL = get_service_url('request-run/reparse');
        PAYLOAD = {'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL,"POST",  PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
        });
    };

    sub_request_status = function(request_id, sub_request_id){
        SERVICE_URL = get_service_url('sub-request/status');
        PAYLOAD = {'RequestID': request_id, 'SubRequestID': sub_request_id};
        SETTINGS = make_ajax_setting(SERVICE_URL, "POST", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
        });
    };
});