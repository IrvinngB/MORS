import pytest

from app.models.roles import RoleSpecialAbility
from app.models.roles_registry import ROLES


EXPECTED_ROLE_IDS = {"sherpa", "clasico", "investigador", "tecnico", "medico"}

VALID_ABILITY_PARAMS = {
    RoleSpecialAbility.SHERPA_FALL_RESISTANCE: {"fall_chance_multiplier"},
    RoleSpecialAbility.INVESTIGATOR_FORECAST: {"forecast_reliability_bonus"},
    RoleSpecialAbility.TECNICO_ALTITUDE_DISCOUNT: {"altitude_threshold", "stamina_discount"},
    RoleSpecialAbility.MEDICO_FREE_HEAL: {"free_heal_amount", "hp_event_mitigation"},
    RoleSpecialAbility.NONE: set(),
}


class TestRolesRegistry:
    def test_exactly_five_roles(self):
        assert len(ROLES) == 5

    def test_all_expected_ids_present(self):
        assert set(ROLES.keys()) == EXPECTED_ROLE_IDS

    def test_each_role_has_valid_special_ability(self):
        for role_id, role_def in ROLES.items():
            assert role_def.special_ability in RoleSpecialAbility, (
                f"Role {role_id} has invalid special_ability: {role_def.special_ability}"
            )

    def test_each_role_has_valid_ability_params(self):
        for role_id, role_def in ROLES.items():
            expected_keys = VALID_ABILITY_PARAMS[role_def.special_ability]
            if expected_keys:
                for key in expected_keys:
                    assert key in role_def.ability_params, (
                        f"Role {role_id} missing ability param: {key}"
                    )
            else:
                assert role_def.ability_params == {}, (
                    f"Role {role_id} with NONE ability should have empty ability_params"
                )

    def test_each_role_has_required_fields(self):
        for role_id, role_def in ROLES.items():
            assert role_def.id == role_id
            assert role_def.display_name, f"Role {role_id} missing display_name"
            assert role_def.difficulty in ("Easy", "Medium", "Normal", "Hard"), (
                f"Role {role_id} has invalid difficulty: {role_def.difficulty}"
            )
            assert role_def.description, f"Role {role_id} missing description"

    def test_sherpa_has_fall_resistance(self):
        sherpa = ROLES["sherpa"]
        assert sherpa.special_ability == RoleSpecialAbility.SHERPA_FALL_RESISTANCE
        assert sherpa.ability_params["fall_chance_multiplier"] == 0.7
        assert sherpa.stamina_cost_multiplier == 0.85
        assert sherpa.hp_delta == 5
        assert sherpa.stamina_delta == 15
        assert sherpa.willpower_delta == -5
        assert sherpa.starting_equipment.get("rope_sections") == 2

    def test_clasico_has_no_ability(self):
        clasico = ROLES["clasico"]
        assert clasico.special_ability == RoleSpecialAbility.NONE
        assert clasico.stamina_cost_multiplier == 1.10
        assert clasico.hp_delta == 5
        assert clasico.stamina_delta == 5
        assert clasico.willpower_delta == 5

    def test_investigador_has_forecast_bonus(self):
        inv = ROLES["investigador"]
        assert inv.special_ability == RoleSpecialAbility.INVESTIGATOR_FORECAST
        assert inv.ability_params["forecast_reliability_bonus"] == 0.25
        assert inv.hp_delta == -10
        assert inv.stamina_delta == -15
        assert inv.willpower_delta == 20
        assert inv.stamina_cost_multiplier == 1.05
        assert inv.starting_equipment.get("oxygen_pct") == 10

    def test_tecnico_has_altitude_discount(self):
        tec = ROLES["tecnico"]
        assert tec.special_ability == RoleSpecialAbility.TECNICO_ALTITUDE_DISCOUNT
        assert tec.ability_params["altitude_threshold"] == 7000
        assert tec.ability_params["stamina_discount"] == 0.90
        assert tec.stamina_cost_multiplier == 0.95
        assert tec.starting_equipment.get("rope_sections") == 2
        assert tec.starting_equipment.get("gas_canisters") == 1
        assert tec.hp_delta == 0
        assert tec.stamina_delta == 0
        assert tec.willpower_delta == 0

    def test_medico_has_free_heal(self):
        med = ROLES["medico"]
        assert med.special_ability == RoleSpecialAbility.MEDICO_FREE_HEAL
        assert med.ability_params["free_heal_amount"] == 15
        assert med.ability_params["hp_event_mitigation"] == 0.20
        assert med.starting_equipment.get("food_rations") == 2
        assert med.starting_equipment.get("oxygen_pct") == 10
        assert med.hp_delta == -5
        assert med.stamina_delta == -10
        assert med.willpower_delta == 15
