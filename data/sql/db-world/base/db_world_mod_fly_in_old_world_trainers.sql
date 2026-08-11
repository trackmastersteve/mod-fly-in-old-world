-- Add Custom Old World Flying to Trainers
DELETE FROM trainer_spell WHERE SpellId = 200001;
INSERT INTO trainer_spell (TrainerId, SpellId, MoneyCost, ReqSkillLine, ReqSkillRank, ReqAbility1, ReqAbility2, ReqAbility3, ReqLevel, VerifiedBuild) VALUES 
(31238, 200001, 5000000, 773, 225, 0, 0, 0, 60, 0),
(16654, 200001, 5000000, 773, 225, 0, 0, 0, 60, 0),
(17502, 200001, 5000000, 773, 225, 0, 0, 0, 60, 0);
