/*
 * Copyright (C) 2016+ AzerothCore <www.azerothcore.org>, released under GNU AGPL v3 license: https://github.com/azerothcore/azerothcore-wotlk/blob/master/LICENSE-AGPL3
 */

#include "ScriptMgr.h"
#include "Player.h"
#include "Item.h"

enum {
    OLD_WORLD_FLYING_SPELL = 200001,
    OLD_WORLD_FLYING_ITEM   = 900002
};

// Add player scripts for zone flight permissions
class FlyInOldWorld : public PlayerScript
{
public:
    FlyInOldWorld() : PlayerScript("FlyInOldWorld") { }

    bool OnPlayerCanFlyInZone(Player* player, uint32 mapId, uint32 zoneId, SpellInfo const* bySpell) override
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

// Item script to handle right-clicking the tome without client spell casting restrictions
class TomeOfOldWorldFlightScript : public ItemScript
{
public:
    TomeOfOldWorldFlightScript() : ItemScript("TomeOfOldWorldFlightScript") { }

    bool OnItemUse(Player* player, Item* item, SpellCastTargets const& /*targets*/) override
    {
        if (player->HasSpell(OLD_WORLD_FLYING_SPELL))
        {
            player->SendSysMessage("You already know Old World Flying.");
            return false;
        }

        player->LearnSpell(OLD_WORLD_FLYING_SPELL, false);
        player->SendSysMessage("You have successfully learned Old World Flying!");
        player->DestroyItem(item->GetBagSlot(), item->GetSlot(), true);
        return true;
    }
};

// Add all scripts
void AddFlyInOldWorld()
{
    new FlyInOldWorld();
    new TomeOfOldWorldFlightScript();
}
