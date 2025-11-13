from app.core.calculator import calculate_all
def test_calculator_basic():
    inputs = {
        'transport': {'car': 1000, 'bus': 0, 'train': 0},
        'elec_kwh_year': 1200,
        'gas_m3_year': 50,
        'food': {'meat_kg': 26, 'dairy_kg': 52, 'veg_kg': 156},
        'waste_kg_year': 364,
        'recycle_rate': 30,
        'flights_km_year': 0
    }
    res = calculate_all(inputs)
    assert 'total_after' in res
    assert res['total_after'] >= 0
