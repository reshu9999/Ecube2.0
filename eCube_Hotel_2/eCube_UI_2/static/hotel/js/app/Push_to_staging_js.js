$(document).ready(function ($) {
    Bind_data_on_page_load();
    $('.multiselect_box').multiselect({
        includeSelectAllOption: true,
        buttonWidth: 250,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true
    });
});
function reset_frm()
{
   window.location.href=window.location.href;
}
function set_span_count_batch()
{
    $('#span_id_div_batch').text($('#div_append_sup').find("input:checkbox:checked").length)
    $('#span_id_sup_sec').text($('#div_sup_sec').find("input:checkbox:checked").length)
}
function Bind_data_on_page_load()
{
    $.ajax({
        url: Bind_request_and_batch_name,
        type: 'GET',
        dataType: 'json',
        success: function (data) {

            $('#drp_req').empty();
            $('#drp_req').append($('<option></option>').val('0').html('--Select Request----'))
            $(data.country).each(function (index, item) {
                $('#drp_req').append($('<option></option>').val(item.id).html(item.title));
            });

           
            $('#drp_req').multiselect('rebuild');
            setData_detals(data.list);
            
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}

function refresh_grid()
{
    $.ajax({
        url: Bind_grid_push_to_Stagging,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            setData_detals(data.list);
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}

function Get_sup_name_by_request()
{
    var id = $('#drp_req').val();
    if (id>0)
    {
        var model ={req_id : id}
        $.ajax({
            url: Bind_request_and_sup_name_by_request_id,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {

            $('#div_append_sup').empty();
            $(data.compt).each(function (index, item) {
                var sup = ' <div class="col-md-6 col-sm-12"><div class="checkbox checkbox-primary checkItem"> <input id="Chk_bx_sup_'+item[0]+'" type="checkbox" onchange="set_span_count_batch();"><label for="Chk_bx_sup_'+item[0]+'"><span>'+item[1]+'</span></label></div></div>';
                $('#div_append_sup').append(sup);
            });
            $('#div_append_sup').find("input:checkbox").prop('checked', true);
            $('#div_sup_sec').empty();
            $(data.compt).each(function (index, item) {
                var sup = ' <div class="col-md-6 col-sm-12"><div class="checkbox checkbox-primary checkItem"> <input id="Chk_bx_sup_sec_'+item[0]+'" type="checkbox" onchange="set_span_count_batch();"><label for="Chk_bx_sup_sec_'+item[0]+'"><span>'+item[1]+'</span></label></div></div>';
                $('#div_sup_sec').append(sup);
            });
            set_span_count_batch();

            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });

    }
    else{
        alert('Please select request !!!');
    }
}






function Pust_to_staging()
{
    var req_id= $('#drp_req').val();
    var first_sup_count= $('#div_append_sup').find("input:checkbox:checked").length;
    var Second_sup_count= $('#div_sup_sec').find("input:checkbox:checked").length
    if (req_id>0)
    {
         if (first_sup_count >0)
         {
            
                var rad_fir= $('#div_radio_first input:radio:checked')[0].id;
                var rad_sec= $( $('#div_radio_Second input:radio:checked')[0]).val();
                
                var Prim_sup_id=''; var Sec_sup_id='';
                var div_sup_1 =$('#div_append_sup').find("input:checkbox:checked");
                $(div_sup_1).each(function (index, item) {
                    var id = (item.id).replace('Chk_bx_sup_','') ;
                    Prim_sup_id=Prim_sup_id+id+',';
                });
                Prim_sup_id =Prim_sup_id.replace(/,\s*$/, "").trim();
                var div_sup_2 =$('#div_sup_sec').find("input:checkbox:checked");
                $(div_sup_2).each(function (index, item) {
                    var id = (item.id).replace('Chk_bx_sup_sec_','') ;
                    Sec_sup_id=Sec_sup_id+id+',';
                });
                Sec_sup_id =Sec_sup_id.replace(/,\s*$/, "").trim();
                var req_text =$("#drp_req option:selected").text();
                var model = {rad_fir: rad_fir,
                    rad_sec:rad_sec,
                    Prim_sup_id:Prim_sup_id,
                    Sec_sup_id:Sec_sup_id,
                    req_id:req_id ,
                    req_text:req_text,
                    user_res:0      
                }
                $.ajax({
                    url: Push_tostg_db_save,
                    type: 'POST',
                    data: model,
                    dataType: 'json',
                    success: function (data) {
                        if (data.htl_grp_dtls > 0) {
                            setData_detals(data.list);
                            reset();
                            alert('Data saved successfully ');
                        }
                        else 
                        {
                            if (data.error_msg != undefined && data.error_msg.trim() !='')
                            {

                                if (data.error_type == "active_batch"){
                                      alert(data.error_msg);
                                }else if(data.error_type == "completed_batch"){
                                    if (confirm(data.error_msg)) {
                                        Pust_to_staging_after_validation();
                                    }
				}
                                  
                            }
                        }
                    },
                    error: function (xhr, errorType, exception) {
                        alert(exception)
                    }
                });
            // }
            // else{
            //     alert('Please select second Sup name !!!!')
            // }
         }
         else{
            alert('Please select First Sup name !!!!')
         }
    }
    else{
        alert('Please select Request ID !!!!')
    }
}


function Pust_to_staging_after_validation()
{
    var req_id= $('#drp_req').val();
    var first_sup_count= $('#div_append_sup').find("input:checkbox:checked").length;
    var Second_sup_count= $('#div_sup_sec').find("input:checkbox:checked").length
    if (req_id>0)
    {
         if (first_sup_count >0)
         {
            
                var rad_fir= $('#div_radio_first input:radio:checked')[0].id;
                var rad_sec= $( $('#div_radio_Second input:radio:checked')[0]).val();
                
                var Prim_sup_id=''; var Sec_sup_id='';
                var div_sup_1 =$('#div_append_sup').find("input:checkbox:checked");
                $(div_sup_1).each(function (index, item) {
                    var id = (item.id).replace('Chk_bx_sup_','') ;
                    Prim_sup_id=Prim_sup_id+id+',';
                });
                Prim_sup_id =Prim_sup_id.replace(/,\s*$/, "").trim();
                var div_sup_2 =$('#div_sup_sec').find("input:checkbox:checked");
                $(div_sup_2).each(function (index, item) {
                    var id = (item.id).replace('Chk_bx_sup_sec_','') ;
                    Sec_sup_id=Sec_sup_id+id+',';
                });
                Sec_sup_id =Sec_sup_id.replace(/,\s*$/, "").trim();
                var req_text =$("#drp_req option:selected").text();
                var model = {rad_fir: rad_fir,
                    rad_sec:rad_sec,
                    Prim_sup_id:Prim_sup_id,
                    Sec_sup_id:Sec_sup_id,
                    req_id:req_id ,
                    req_text:req_text, 
                    user_res:1        
                }
                $.ajax({
                    url: Push_tostg_db_save,
                    type: 'POST',
                    data: model,
                    dataType: 'json',
                    success: function (data) {
                        if (data.htl_grp_dtls > 0) {
                            setData_detals(data.list);
                            reset();
                            alert('Data saved successfully ');
                        }
                        else 
                        {
                            if (data.error_msg != undefined && data.error_msg.trim() !='')
                            {
                                alert(data.error_msg );
                            }
                        }
                    },
                    error: function (xhr, errorType, exception) {
                        alert(exception)
                    }
                });
            // }
            // else{
            //     alert('Please select second Sup name !!!!')
            // }
         }
         else{
            alert('Please select First Sup name !!!!')
         }
    }
    else{
        alert('Please select Request ID !!!!')
    }
}

function reset()
{
    $('#drp_req').val('0');
    $('#drp_req').multiselect('clearSelection');
    $('#drp_req').multiselect('refresh');
    $('#div_append_sup').find("input:checkbox:checked").prop('checked', false);
    $('#div_sup_sec').find("input:checkbox:checked").prop('checked', false);
    $('#span_id_div_batch').text('0');
    $('#span_id_sup_sec').text('0');
    $('#div_append_sup').empty();
    $('#div_sup_sec').empty();
}

function setData_detals(data) {
    $('#divtable').show();
    var table = $("#hotel_match_unmatch2").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    
    $.each(data, function (i, item) {

        var chk='';
        var comp_chk = '';
        if (item.Priority=='1')
        {
            chk= 'checked';
        }
        if (item.Status_id !='1' )
        {
            comp_chk= 'disabled';
        }
        var time= item.Rep_time.replace('T','  ');
        var start_time= item.Report_start_time == null ? "" : item.Report_start_time.replace('T','  ');
        var end_time= item.Reprot_end_time == null ? "" : item.Reprot_end_time.replace('T','  ');
        var client_priority= item.client_priority == 1 ? "Yes" : "No";

        trHTML+='<tr id="tr_grid_'+item.main_id+'">'+
         ' <td><div class="checkbox checkbox-default checkbox-inline pull-left">'+
                  '<input id="grid_chk_bx_'+item.main_id+'" type="checkbox" '+comp_chk+'>'+
                  '<label for="grid_chk_bx_'+item.main_id+'"> '+item.Batch_id+' </label>'+
                '</div></td>'+
        '<td>'+item.Batch_name+'</td>'+
        '<td>'+item.status+'</td>'+
        '<td>'+item.Report_Type+'</td>'+
        '<td>'+time+'</td>'+
        '<td>'+start_time+'</td>'+
        '<td>'+end_time+'</td>'+
      
        ' <td><label class="switch">'+
           '<input id="grid_chk_bx_Prio_'+item.main_id+'" class="switch-input" type="checkbox" '+chk+' onchange= fun_update_prio(this,event)   '+comp_chk+' />'+
            '<span class="switch-label" data-on="HIGH" data-off="NORMAL"></span> <span class="switch-handle"></span> </label></td>'+
        
        '<td>'+client_priority+'</td>'+
      '</tr>';

    });
    $('#tbody_grid').append(trHTML);
    $('#hotel_match_unmatch2').dataTable( {
        "sPaginationType": "full_numbers",
		"bFilter": true,
		"bInfo": false,
		"bPaginate": true,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
		aaSorting :[],
        fixedColumns:   {
            leftColumns: 0,
            rightColumns: 1
        }, 
	});
    $('.dataTables_scrollBody,.addhotel_checkbox_contaner').perfectScrollbar();

}

function frm_reset()
{
    window.location.href =window.location.href;
}

function Save_stopped_selected()
{
    var rd_chk_count = 0;
    var csv_id='';
    var table = $('#hotel_match_unmatch2').dataTable();
    $(table.fnGetNodes()).each(function (i, item) {
        // debugger;
       var id = (item.id).replace('tr_grid_','');
       var chak_bx= $($('#'+item.id+'').find("input:checkbox")[0]).prop('checked');
       if (chak_bx)
       {
         rd_chk_count=rd_chk_count+1;
         csv_id= csv_id+id+',';
       }
    });

    if (rd_chk_count==0)
    {
        alert('No any checkbox selected !!!');
        return false;
    }

    var model = {csv_id: csv_id.replace(/,\s*$/, "").trim(),
        session_id :1
    }
    $.ajax({
        url: Db_push_stag_stopped,
        type: 'POST',
        data: model,
        dataType: 'json',
        success: function (data) {
            alert('Save successfully !!!');
            setData_detals(data.list);
            reset();
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });


}

function fun_update_prio(id,e)
{

    var Act_fal='low';
    var chk_val = $('#'+id.id+'').prop('checked');
    if (chk_val)
    {
        Act_fal ="high";
    }
    if (confirm('Are you sure want set '+Act_fal+' priority?')) {
        var main_id = (id.id).replace('grid_chk_bx_Prio_','');
    var model = {id: main_id,
        chk_val:chk_val,
        session_id :1
    }
    $.ajax({
        url: Db_push_to_stag_prio_update,
        type: 'POST',
        data: model,
        dataType: 'json',
        success: function (data) {
            alert(Act_fal+" priority set sucessfully ");
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
    } else {
        $('#'+id.id+'').prop('checked', !chk_val );
        e.stopImmediatePropagation();
    }
    
}


