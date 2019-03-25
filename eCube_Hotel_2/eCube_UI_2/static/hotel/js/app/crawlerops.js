/**
 * Created by ironeagle on 3/19/18.
 */

jQuery(document).ready(function ($) {
    CRAWLER_OPS_SERVICE = {
        'HOST': 'https://ecube-hotel.eclerx.com',
        'VERSION': 'api/v1'
    };

    var get_service_url = function(path){
        return CRAWLER_OPS_SERVICE['HOST'] + '/'
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

    reparse_request = function(request_run_id){
        SERVICE_URL = get_service_url('request-management/reparse-request-run/' + request_run_id);
        PAYLOAD = {'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL,"POST",  PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
            window.location.href = window.location.href;
        });
    };

    reparse_sub_request = function(request_run_id, sub_request_id){
        SERVICE_URL = get_service_url('request-management/reparse-sub-request/' + request_run_id + '/' + sub_request_id);
        PAYLOAD = {'SubRequestID': sub_request_id, 'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL,"POST",  PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
            window.location.href = window.location.href;
        });
    };

    recrawl_sub_request = function(request_run_id, sub_request_id){
        SERVICE_URL = get_service_url('request-management/reparse-sub-request/' + request_run_id + '/' + sub_request_id);
        PAYLOAD = {'SubRequestID': sub_request_id, 'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL,"POST",  PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
            window.location.href = window.location.href;
        });
    };

    reparse_selected_sub_request = function(request_run_id, sub_request_id){
        SERVICE_URL = get_service_url('request-management/reparse-sub-request/' + request_run_id + '/' + sub_request_id);
        PAYLOAD = {'SubRequestID': sub_request_id, 'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL,"POST",  PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
           // window.location.href = window.location.href;
        });
    };

    pause_request = function(request_run_id){
        SERVICE_URL = get_service_url('request-management/pause-request-run/' + request_run_id);
        PAYLOAD = {'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL, "POST", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
            window.location.href = window.location.href;
        });
    };

    resume_request = function(request_run_id){
        SERVICE_URL = get_service_url('request-management/resume-request-run/' + request_run_id);
        PAYLOAD = {'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL, "POST", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
            window.location.href = window.location.href;
        });
    };

    stop_request = function(request_run_id){
        SERVICE_URL = get_service_url('request-management/stop-request-run/' + request_run_id);
        PAYLOAD = {'RequestRunID': request_run_id};
        SETTINGS = make_ajax_setting(SERVICE_URL, "POST", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
            window.location.href = window.location.href;
        });
    };

    delete_request_schedule = function(request_id){
        SERVICE_URL = get_service_url('request-management/delete-request-schedule/' + request_id);
        PAYLOAD = {'RequestID': request_id};
        SETTINGS = make_ajax_setting(SERVICE_URL, "POST", PAYLOAD);

        $.ajax(SETTINGS).done(function (response) {
            console.log(response);
            window.location.href = window.location.href;
        });
    };
});
