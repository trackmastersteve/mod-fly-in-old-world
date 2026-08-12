-- ---------------------------------------------------------------------------
-- Custom Item: Tome of Old World Flight (Entry: 900002)
-- ---------------------------------------------------------------------------
DELETE FROM item_template WHERE entry = 900002;

INSERT INTO item_template (
    entry, class, subclass, name, displayid, Quality, 
    BuyCount, BuyPrice, SellPrice, InventoryType, 
    AllowableClass, AllowableRace, ItemLevel, RequiredLevel, 
    maxcount, stackable, bonding, spellid_1, spelltrigger_1, 
    spellcharges_1, VerifiedBuild
) VALUES (
    900002, 15, 0, 'Tome of Old World Flight', 61330, 7, 
    1, 5000000, 100000, 0, 
    -1, -1, 0, 60, 
    1, 1, 0, 200001, 0, 
    0, NULL
);
-- ---------------------------------------------------------------------------
-- Spell Script Mapping
-- ---------------------------------------------------------------------------
DELETE FROM spell_script_names WHERE spell_id = 200001;
INSERT INTO spell_script_names (spell_id, ScriptName) VALUES (200001, 'spell_tome_of_old_world_flight');

-- ---------------------------------------------------------------------------
-- Vendor Mappings (Hira Snowdawn, Grunda Bronzewing, etc.)
-- ---------------------------------------------------------------------------
DELETE FROM npc_vendor WHERE item = 900002;

INSERT INTO npc_vendor (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild) VALUES
(16654, 0, 900002, 0, 0, 0, NULL),
(31238, 0, 900002, 0, 0, 0, NULL),
(35101, 0, 900002, 0, 0, 0, NULL);
