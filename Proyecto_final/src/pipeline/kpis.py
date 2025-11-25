def avg(values):
    return sum(values) / len(values) if values else 0


def compute_kpis(normal_rows, evento_rows, outfile):
    """
    KPIs básicos sin pandas.
    """

    h_normal = [r[2] for r in normal_rows]
    h_evento = [r[2] for r in evento_rows]

    t_normal = [r[3] for r in normal_rows]
    t_evento = [r[3] for r in evento_rows]

    total = len(normal_rows) + len(evento_rows)
    porc_eventos = (len(evento_rows) / total * 100) if total else 0

    with open(outfile, "w", encoding="utf-8") as f:
        f.write("===== KPI DEL SENSOR =====\n\n")

        f.write("---- Humedad ----\n")
        f.write(f"Normal promedio: {avg(h_normal):.2f}\n")
        f.write(f"Evento promedio: {avg(h_evento):.2f}\n")
        f.write(f"Máximo: {max(h_normal + h_evento):.2f}\n")
        f.write(f"Mínimo: {min(h_normal + h_evento):.2f}\n\n")

        f.write("---- Temperatura ----\n")
        f.write(f"Normal promedio: {avg(t_normal):.2f}\n")
        f.write(f"Evento promedio: {avg(t_evento):.2f}\n")
        f.write(f"Máximo: {max(t_normal + t_evento):.2f}\n")
        f.write(f"Mínimo: {min(t_normal + t_evento):.2f}\n\n")

        f.write("---- Eventos ----\n")
        f.write(f"Total de eventos: {len(evento_rows)}\n")
        f.write(f"Porcentaje de eventos: {porc_eventos:.2f}%\n")
