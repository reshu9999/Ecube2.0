DELIMITER ;;

CREATE PROCEDURE `TEST_MDM_HB_1`(batcid int)
BEGIN

drop Temporary table if exists MDM_data;

create temporary table MDM_data
(
 Hotelid int (11),
 Hotelname nvarchar(500)
);



 insert into MDM_data (Hotelid, Hotelname)
select Hotelid, Hotelname FROM eCube_Centralized_DB.Hotels;

#select * from MDM_data;

truncate table MDM_data_1;

insert into MDM_data_1 (Hotelid, Hotelname)
select  Hotelid, Hotelname from MDM_data;



drop temporary table MDM_data;
select * from MDM_data_1;

END ;;
