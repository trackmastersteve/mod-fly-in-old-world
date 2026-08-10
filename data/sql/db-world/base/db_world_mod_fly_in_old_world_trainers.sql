-- Add Custom Old World Flying to Outland & Northrend Flight Trainers
INSERT IGNORE INTO `npc_trainer` (`ID`, `SpellID`, `MoneyCost`, `ReqSkillLine`, `ReqSkillRank`, `ReqLevel`) VALUES
(31238, 200001, 5000000, 773, 225, 60), -- Hira Snowdawn (Dalaran)
(16654, 200001, 5000000, 773, 225, 60), -- Hargen Bronzewing (Honor Hold)
(17502, 200001, 5000000, 773, 225, 60); -- Wind Rider Jahubo (Thrallmar)
