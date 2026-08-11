-- ==========================================
-- Custom Old World Flying Module - SQL Script
-- ==========================================

-- 1. Create the Tome of Old World Flight item with a clean entry ID (900002)
-- Uses a stable book display ID (1733) and links directly to spell 200001
DELETE FROM item_template WHERE entry = 900002;
INSERT INTO item_template (entry, class, subclass, name, displayid, quality, flags, buyprice, sellprice, inventorytype, allowableclass, allowablerace, RequiredLevel, SpellId_1, SpellTrigger_1, SpellCharges_1, description) 
VALUES (900002, 13, 0, 'Tome of Old World Flight', 1733, 2, 0, 5000000, 100000, 0, -1, -1, 60, 200001, 0, 0, '');

-- 2. Add the Tome to Vendor Inventories
-- Includes Hira Snowdawn (31238), Grunda Bronzewing (16654), and Bana Wildmane (15502)
DELETE FROM npc_vendor WHERE item = 900002;
INSERT INTO npc_vendor (entry, item, maxcount, incrtime) VALUES 
(31238, 900002, 0, 0), -- Hira Snowdawn (Dalaran)
(16654, 900002, 0, 0), -- Grunda Bronzewing (Hellfire Peninsula - Alliance)
(15502, 900002, 0, 0); -- Bana Wildmane (Hellfire Peninsula - Horde)
