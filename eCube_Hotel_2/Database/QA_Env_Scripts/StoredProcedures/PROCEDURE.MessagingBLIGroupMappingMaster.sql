DELIMITER ;;

CREATE PROCEDURE `MessagingBLIGroupMappingMaster`(
		IN prmBLIName varchar(500),
		IN prmBLIGroupName varchar(500),
        IN prmRevenue int
)
BEGIN

		select count(*) into @blicount from tbl_BliMaster where BliName=prmBLIName;


        select count(*) into @bligrpcount from tbl_Bli_GroupMaster where BLIGroupName=prmBLIGroupName;

        IF @bligrpcount= 0 then
        INSERT INTO tbl_Bli_GroupMaster (BLIGroupName)
		values (prmBLIGroupName);
        end if;


        select Id into @bligrpid from tbl_Bli_GroupMaster
        where BLIGroupName=prmBLIGroupName;


		if @blicount= 0 then
        Insert into tbl_BliMaster (BLIName,Active,CreatedDate,ModifiedDate,BLI_GRP_Id,Revenue)
        values (prmBLIName,1,now(),now(),@bligrpid,prmRevenue);
        END IF;

END ;;
