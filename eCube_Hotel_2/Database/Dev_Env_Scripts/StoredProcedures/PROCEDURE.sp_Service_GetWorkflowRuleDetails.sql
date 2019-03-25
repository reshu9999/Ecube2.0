DELIMITER ;;

CREATE PROCEDURE `sp_Service_GetWorkflowRuleDetails`(
In p_RunID int 
)
BEGIN

SELECT Distinct
    map.MatchingworkflowRulesmappingid as FlowSequence,
    map.MatchingRulesMasterId as RuleId,
    rul.MatchingRulesName as RuleName,
    rul.active,
    fmap.MatchingWeightage as Weightage,
    map.LowerCutOffLimit as LowerLimit,
    map.UpperCutOffLimit as UpperLimit,
    map.SuccessRuleId as SuccessFlowID,
    map.FailureRuleId as FailureFlowID,
    map.MstThresholdActionId as ThresholdAction,
    fmas.TableFieldName as FieldName,
    alg.AlgorithmsName as `Algorithm`
  FROM  MatchingWorkFlowRulesMapping map 
  Inner Join MatchingRunMaster r on r.MatchingWorkflowMasterId = map.MatchingWorkflowMasterId
  INNER JOIN MatchingRulesMaster rul  
    ON map.MatchingRulesMasterId = rul.MatchingRulesMasterId
  INNER JOIN MatchingRulesFieldMapping fmap  
    ON fmap.MatchingRulesMasterId = rul.MatchingRulesMasterId
  INNER JOIN MatchingFieldMaster fmas  
    ON fmas.MatchingFieldMasterId = fmap.MatchingFieldMasterId
  LEFT JOIN AlgorithmsMaster alg  
    ON fmap.AlgorithmsId = alg.AlgorithmsId
  WHERE  r.runid = p_RunID;

END ;;
