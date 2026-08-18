/*
 * Copyright (C) 2016+ AzerothCore <www.azerothcore.org>, released under GNU AGPL v3 license: https://github.com/azerothcore/azerothcore-wotlk/blob/master/LICENSE-AGPL3
 */

#include "ScriptMgr.h"
#include "Player.h"
#include "SpellScript.h"
#include "SpellAuraEffects.h"

enum {
    OLD_WORLD_FLYING_SPELL = 200001
};

// Player script for zone flight permissions
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

// Spell script to handle learning the ability when the tome spell is triggered
class spell_tome_of_old_world_flight : public SpellScriptLoader
{
public:
    spell_tome_of_old_world_flight() : SpellScriptLoader("spell_tome_of_old_world_flight") { }

    class spell_tome_of_old_world_flight_SpellScript : public SpellScript
    {
        PrepareSpellScript(spell_tome_of_old_world_flight_SpellScript);

        bool Validate(SpellInfo const* /*spellInfo*/) override
        {
            return true;
        }

        // Force the server to accept the cast, bypassing vanilla level/skill checks
        SpellCastResult CheckCast()
        {
            return SPELL_CAST_OK;
        }

        void HandleScriptEffect(SpellEffIndex effIndex)
        {
            // Block the core engine from natively processing the cloned learn effect
            PreventHitEffect(effIndex); 

            Player* player = GetCaster()->ToPlayer();
            if (!player)
                return;

            if (player->HasSpell(OLD_WORLD_FLYING_SPELL))
            {
                player->SendSystemMessage("You already know Old World Flying.");
                return;
            }

            player->learnSpell(OLD_WORLD_FLYING_SPELL, false);
            player->SendSystemMessage("You have successfully learned Old World Flying!");
        }

        void Register() override
        {
            // Hook the CheckCast override and the Effect handler
            OnCheckCast += SpellCheckCastFn(spell_tome_of_old_world_flight_SpellScript::CheckCast);
            OnEffectHit += SpellEffectFn(spell_tome_of_old_world_flight_SpellScript::HandleScriptEffect, EFFECT_0, SPELL_EFFECT_LEARN_SPELL);
        }
    };

    SpellScript* GetSpellScript() const override
    {
        return new spell_tome_of_old_world_flight_SpellScript();
    }
};

// Add all scripts
void AddFlyInOldWorld()
{
    new FlyInOldWorld();
    new spell_tome_of_old_world_flight();
}
