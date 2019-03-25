//js file being used to validate forms 
//Author: Shrikant Panada
//Date : 08 May 2018

function valHotelStandUpload()
{
    var fileobject=document.getElementById("HotelStanFile");
    var filename=fileobject.value;
    if (filename.length < 1)
    {
        alert("No CSV file Found to Upload ....");
        return false;
    }
    var ext=filename.substring(filename.lastIndexOf('.') + 1);
    if (ext.localeCompare('csv')==0)
    {
        return true;
    }
    else
    {
        alert("Upload only CSV files...");
    }
    alert("valHotelStandUpload function failed...");
    return false;
}

function valHotelSplCharUpl()
{
	var fileobject=document.getElementById("SpecialCharFileUpld");
    var filename=fileobject.value;
    if (filename.length < 1)
    {
        alert("No CSV file Found to Upload ....");
        return false;
    }
    var ext=filename.substring(filename.lastIndexOf('.') + 1);
    if (ext.localeCompare('csv')==0)
    {
        return true;
    }
    else
    {
        alert("Upload only CSV files...");
    }
    alert("valHotelSplCharUpl function failed...");
    return false;
    
}


function valHotelStandAdd()
{
    var priority=document.getElementById("txtpriority").value;
    var txtroomtype=document.getElementById("txtroomtype").value;
    var txtroomtypeMatch=document.getElementById("txtroomtypeMatch").value;
    var txtruletype=document.getElementById("txtruletype").value.toLowerCase() ;
    
    
    if (priority.length<1)
    {
        alert(" Priority are Mandatory..");
        return false;
    }
    else if  (txtroomtype.length<1)
    {
        alert(" Room type  are Mandatory..");
        return false;
    }
    else if  (txtroomtypeMatch.length<1)
    {
        alert(" Room type match  are Mandatory..");
        return false;
    }
    
    else if  (txtruletype != ''){
       
       if (txtruletype == 'general' || txtruletype == 'primary'){
        
       }
       else{
        alert(" Rule type  Should be General, Primary or Blank");
        return false;
       }
    }


    if(isNaN(priority))
    {
        alert("Priority can not be string");
        return false;
    }
}

function valHotelSpcCharUpload()
{
    var txtSpecialChar=document.getElementById("txtSpecialChar").value;
    var txtReplaceSepChar=document.getElementById("txtReplaceSepChar").value;
    var active=document.getElementById("active").value;
    var in_active=document.getElementById("in_active").value;

    if (txtSpecialChar.length<1)
    {
        alert(" Special character are Mandatory..");
        return false;
    }
    else if  (txtReplaceSepChar.length<1)
    {
        alert(" Replace  character   are Mandatory..");
        return false;
    }
    else if  (active.length<1)
    {
        alert(" Status  are Mandatory..");
        return false;
    }
    else if  (in_active.length<1)
    {
        alert(" Inactive status  are Mandatory..");
        return false;
    }

}
