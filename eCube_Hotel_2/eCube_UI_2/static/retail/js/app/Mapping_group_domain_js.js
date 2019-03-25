$(document).ready(function ($) {
   Bind_table_data();
});

function Bind_table_data() {
    $.ajax({
        url: f_Bind_grp_mapp_detail,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#tbody_save_table').empty();
            $('#tbody_grp_name_front').empty();
            $(data.Field_master_db).each(function (index, item) {
                var sup = '<tr ><td><div class="checkbox checkbox-primary"><input id="tbl_main_grp_chk_'+item.id+'" type="checkbox"><label for="tbl_main_grp_chk_'+item.id+'"> '+item.name+'</label></div></td><td><label id="lbl_main_text_'+item.id+'">'+item.name+'</label></td> </tr>';
                $('#tbody_save_table').append(sup);
            });
            $('#drp_grp').empty();
            $('#drp_grp').append($('<option></option>').val('0').html('select option'));
            $(data.Field_master).each(function (index, item) {
                $('#drp_grp').append($('<option></option>').val(item.id).html(item.name));
            });
            $('#drp_bli').empty();
            $('#drp_bli').append($('<option></option>').val('0').html('select option'));
            $(data.bli_master).each(function (index, item) {
                $('#drp_bli').append($('<option></option>').val(item.id).html(item.BliName));
            });
           
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}

function get_grp_data()
{
    var id = $('#drp_grp').val();
    if (id>0)
    {
        var model = {grp_id: id}
        $.ajax({
            url: f_get_grp_mapp_detail,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                debugger;
                $('#div_tbl_frm_frnt').show();
                $('#map_div').show();
                $('#map_bli').show();
                if(data.Field_master_db.length>0)
                { 
               
                $('#tbody_grp_name_front').empty();
                $(data.Field_master_db).each(function (index, item) {
                    var sup = '<tr id ="tr_id_'+item.id+'"><td>'+item.textboxvalue+'</td> <td>'+item.textboxvalue+'</td>  <td> <a href="javascript:void(0);"  onclick ="Delete_Record('+item.id+')"> Delete </a></td> </tr>';
                     $('#tbody_grp_name_front').append(sup);
                 });
                 $('#bind_grp_description').text(data.Field_master_data[0].description);
                 if (data.bli_master !='')
                 {
                    $('#bind_grp__bli_description').text(data.bli_master[0].BliName);
                 }
                 else{
                    $('#bind_grp__bli_description').text('No record found !!!');
                 }
                }
                else
                {
                $('#tbody_grp_name_front').empty(); 
                
                    var sup = '<tr><td colspan="3" align="center" style="color:#900;"> No record found </td>  </tr>';
                     $('#tbody_grp_name_front').append(sup);                
                     $('#bind_grp_description').text('No record found');
                }
                
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }
}


function Delete_Record(id)
{

    if (confirm('Are you sure ?')) {
        var model ={id:id, grp_id : $('#drp_grp').val() }
    $.ajax({
        url: f_delete_grp_mapp_detail,
        type: 'POST',
        data: model,
        dataType: 'json',
        success: function (data) {
            debugger;
            alert("Record deleted successfully ");
            $('#tbody_grp_name_front').empty();
                $(data.Field_master_db).each(function (index, item) {
                    var sup = '<tr id ="tr_id_'+item.id+'"><td>'+item.textboxvalue+'</td> <td>'+item.textboxvalue+'</td>  <td> <a href="javascript:void(0);"  onclick ="Delete_Record('+item.id+')"> Delete </a></td> </tr>';
                     $('#tbody_grp_name_front').append(sup);
                 });
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
    } 
   
}


function Save_grp_detail()
{
   var count= $('#tbody_save_table').find("input:checkbox:checked").length
   var grp_name= $('#txt_grp_name').val().trim();
   var grp_desc= $('#txt_grp_desc').val().trim();
   var blI_data= $('#drp_bli').val();
       if (grp_name!='')
       {
           if (grp_desc!='')
           {
            if (count>0)
            { 

            if (blI_data ==0)
            {
               alert('Please select bli !!!');
               return false;
            }
            var grp_id ='';
            var grp_field_name='';
            var div_element= $('#tbody_save_table').find("input:checkbox:checked");
            $(div_element).each(function (index, item) {
               var chk_id= (item.id).replace('tbl_main_grp_chk_','');
               var lbl_text = $('label[for='+  item.id  +']').text();
               grp_id=grp_id+chk_id+',';
               grp_field_name=grp_field_name+lbl_text+',';
            });
            var model = {grp_name: grp_name,
                grp_desc:grp_desc,
                user_id:1,
                grp_id:grp_id.replace(/,\s*$/, "").trim(),
                grp_field_name:grp_field_name.replace(/,\s*$/, "").trim(),
                bli_data :blI_data
            }
            $.ajax({
                url: f_Save_grp_detail,
                type: 'POST',
                data: model,
                dataType: 'json',
                success: function (data) {
                   alert(grp_name+ ' Saved successfully ');
                   $('#tbody_save_table').find("input:checkbox:checked").prop('checked',false);
                   $('#txt_grp_name').val('');
                   $('#txt_grp_desc').val('');
                   Bind_table_data();
                },
                error: function (xhr, errorType, exception) {
                    alert(exception)
                }
            });
            
        }

    
        else
        {
            alert('Please select  any mapping field group !!!');
        }

           }
           else{
            alert('Please enter mapping group description  !!!');
           }
       }
       else{
        alert('Please enter mapping group name !!!');
       }
}

function getSelected(){
       var grp_type = $('.svpopupbtn.selected').text().trim();
       var lbl_text = $('#lbl_main_text_1').text();
       lbl_text =lbl_text +' '+grp_type
       $('#lbl_main_text_1').text(lbl_text);
    }