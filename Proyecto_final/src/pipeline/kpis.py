def calcular_kpis(valores):
    if not valores:
        return None
    
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / len(valores)

    return {
        "min": minimo,
        "max": maximo,
        "promedio": promedio,
        "conteo": len(valores)
    }
