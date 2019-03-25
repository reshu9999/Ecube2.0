DELIMITER ;;

CREATE PROCEDURE `bd_outprm`(OUT po_ErrMessage   VARCHAR(200))
BEGIN
	DECLARE code CHAR(5) DEFAULT '00000';
	DECLARE msg TEXT;
    
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
	set po_ErrMessage = 'Error in procedure sp_Get';
    -- GET DIAGNOSTICS @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
    GET DIAGNOSTICS CONDITION 1 code = RETURNED_SQLSTATE, msg = MESSAGE_TEXT;
    
  END;

drop temporary table if exists x;
Create temporary table x (id int);
insert into x (id) select 'z' ;

select msg;
select * from x;


END ;;
