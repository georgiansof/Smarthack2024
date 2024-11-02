def calculateKpi(productie, miscari, penalitati):
    kpi = 0
    for i in range(42):
        kpi += productie[i] + miscari[i] + penalitati[i]
    
    return kpi