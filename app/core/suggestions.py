def suggest_reductions(inputs):
    suggestions=[]
    # placeholder heuristics
    if inputs['transport']['car']>0:
        suggestions.append('Consider carpooling or reducing car use')
    if inputs['food']['meat_kg']>52*0.2:
        suggestions.append('Reduce red meat consumption')
    return suggestions
