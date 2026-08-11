-- Add Custom Old World Flying to Outland & Northrend Flight Trainers
DELETE FROM `npc_trainer` WHERE `SpellId` = 200001;
INSERT INTO `npc_trainer` (`ID`, `SpellId`, `MoneyCost`, `ReqSkillLine`, `ReqSkillRank`, `ReqLevel`, `ReqSpell`) VALUES
(31238, 200001, 5000000, 773, 225, 60, 0), -- Hira Snowdawn (Dalaran)
(16654, 200001, 5000000, 773, 225, 60, 0), -- Hargen Bronzewing (Honor Hold)
(17502, 200001, 5000000, 773, 225, 60, 0); -- Wind Rider Jahubo (Thrallmar)
