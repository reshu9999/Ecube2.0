DELIMITER ;;

CREATE PROCEDURE `bd_outprm`(OUT po_ErrMessage   VARCHAR(200))
BEGIN
	DECLARE code CHAR(5) DEFAULT '00000';
	DECLARE msg TEXT;
    
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
	GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE,@errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
	SET po_ErrMessage = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		-- SELECT @sqlstate, @errno, @text;
-- select @ERROR_MESSAGE, @ERROR_NUMBER,@SQLSTATE_MESSAGE  ;
    -- set po_ErrMessage = 'Error in procedure sp_Get';
    -- GET DIAGNOSTICS @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
    -- GET DIAGNOSTICS CONDITION 1 code = RETURNED_SQLSTATE, msg = MESSAGE_TEXT;
    -- select code, msg;
    -- select @SQLSTATE   ,    @SQLSTATE_MESSAGE;
    
    /*create temporary table error_table( -- code char(5), 
    message text);
    insert into  error_table (
    --     code    ,   
    message
    ) values (
        -- @@SQLSTATE   ,    
        @@SQLSTATE_MESSAGE
    );
    */
  END;

drop temporary table if exists x;
Create temporary table x (id int);
insert into x (id) select 'z' ;

select msg;
select * from x;


END ;;
