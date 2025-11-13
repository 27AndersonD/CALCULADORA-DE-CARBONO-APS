from app.core.factors import DEFAULT_FACTORS
import pandas as pd

def calc_transport(transport_dict):
    total=0; details={}
    for mode, km in transport_dict.items():
        if mode=='car':
            f=DEFAULT_FACTORS['car_km']
        elif mode=='bus':
            f=DEFAULT_FACTORS['bus_km']
        elif mode=='train':
            f=DEFAULT_FACTORS['train_km']
        else:
            f=0
        co2 = km * f
        details[mode.capitalize()] = co2
        total += co2
    return total, details

def calc_energy(elec_kwh, gas_m3):
    elec = elec_kwh * DEFAULT_FACTORS['electricity_kwh']
    gas = gas_m3 * DEFAULT_FACTORS['natural_gas_m3']
    return elec+gas, {'Eletricidade':elec, 'Gás':gas}

def calc_food(food_dict):
    total=0; details={}
    for k,v in food_dict.items():
        factor = DEFAULT_FACTORS.get(k, 0)
        co2 = factor * v
        details[k.replace('_',' ').capitalize()] = co2
        total += co2
    return total, details

def calc_waste(waste_kg):
    val = waste_kg * DEFAULT_FACTORS['waste_kg']
    return val, {'Resíduos': val}

def calc_flights(km):
    val = km * DEFAULT_FACTORS['flight_km']
    return val, {'Voos': val}

def calculate_all(inputs: dict):
    t_total, t_det = calc_transport(inputs['transport'])
    e_total, e_det = calc_energy(inputs['elec_kwh_year'], inputs['gas_m3_year'])
    f_total, f_det = calc_food(inputs['food'])
    w_total, w_det = calc_waste(inputs['waste_kg_year'])
    fl_total, fl_det = calc_flights(inputs['flights_km_year'])

    total = t_total + e_total + f_total + w_total + fl_total
    recycling_benefit = w_total * (inputs.get('recycle_rate',0)/100) * 0.6
    total_after = max(0, total - recycling_benefit)

    breakdown = {
        'Transporte': t_total,
        'Energia': e_total,
        'Alimentação': f_total,
        'Resíduos': max(0, w_total - recycling_benefit),
        'Voos': fl_total,
        'Total': total_after
    }

    details = {**t_det, **e_det, **f_det, **w_det, **fl_det}
    df = pd.DataFrame(list(details.items()), columns=['Categoria','kgCO2e/ano']).sort_values('kgCO2e/ano', ascending=False)
    return {'total': total, 'total_after': total_after, 'breakdown': breakdown, 'details_df': df}
