/*
 * Copyright (C) 2016+ AzerothCore <www.azerothcore.org>, released under GNU AGPL v3 license: https://github.com/azerothcore/azerothcore-wotlk/blob/master/LICENSE-AGPL3
 */

#include "ScriptMgr.h"
#include "Player.h"
#include "Item.h"

enum {
    OLD_WORLD_FLYING_SPELL = 200001
};

// Player script for zone flight permissions
class FlyInOldWorld : public PlayerScript
{
public:
    FlyInOldWorld() : PlayerScript("FlyInOldWorld") { }

    bool OnPlayerCanFlyInZone(Player* player, uint32 mapId, uint32 zoneId, SpellInfo const* /*bySpell*/) override
    {
        uint32 v_map = GetVirtualMapForMapAndZone(mapId, zoneId);
        if (v_map == 0 || v_map == 1)
        {
            if (!player->HasSpell(OLD_WORLD_FLYING_SPELL))
            {
                return false;
            }
        }
        return true;
    }
};

// Item script to bypass spell engine requirements entirely
class item_tome_of_old_world_flight : public ItemScript
{
public:
    item_tome_of_old_world_flight() : ItemScript("item_tome_of_old_world_flight") { }

    bool OnUse(Player* player, Item* item, SpellCastTargets const& /*targets*/) override
    {
        if (player->HasSpell(OLD_WORLD_FLYING_SPELL))
        {
            player->SendSystemMessage("You already know Old World Flying.");
            return false; 
        }

        // Force teach the spell and destroy the item natively
        player->learnSpell(OLD_WORLD_FLYING_SPELL, false);
        player->SendSystemMessage("You have successfully learned Old World Flying!");
        player->DestroyItemCount(item->GetEntry(), 1, true);

        return true; 
    }
};

// Add all scripts
void AddFlyInOldWorld()
{
    new FlyInOldWorld();
    new item_tome_of_old_world_flight();
}
