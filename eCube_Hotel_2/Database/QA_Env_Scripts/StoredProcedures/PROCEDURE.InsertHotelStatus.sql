DELIMITER ;;

CREATE PROCEDURE `InsertHotelStatus`()
BEGIN

set foreign_key_checks =0;
alter table HotelStatus change HotelStatusId HotelStatusId int(11) not NULL;

truncate table HotelStatus;


insert into HotelStatus(HotelStatusId,HotelStatus,Active,CreatedBy,CreatedDateTime,ModifiedBy,ModifiedDatetime) 
select 
HotelStatusId,HotelStatus,Active,1,CreatedDateTime,ModifiedBy,ModifiedDatetime
from
ecube_Staging.HotelStatus
order by HotelStatusId;


alter table HotelStatus change HotelStatusId HotelStatusId int(11) not NULL auto_increment;


SET @newIndex = (select max(HotelStatusId) from HotelStatus);
set @sql1 = concat('ALTER table HotelStatus auto_increment = ',@newIndex );
prepare st from @sql1;
execute st;
set foreign_key_checks =1;
END ;;
