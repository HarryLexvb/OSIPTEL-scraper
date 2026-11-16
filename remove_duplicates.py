import csv

# Leer RUCs ya scrapeados de resultados.csv
print("Leyendo RUCs ya scrapeados...")
scraped_rucs = set()
with open('resultados.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if row:  # Skip empty rows
            scraped_rucs.add(row[0])  # First column is RUC

print(f"Total de RUCs ya scrapeados: {len(scraped_rucs)}")

# Leer RUCs faltantes
print("\nLeyendo RUCs faltantes...")
pending_rucs = []
with open('rucs/ruc_faltante_osiptel_parte1.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if row:  # Skip empty rows
            pending_rucs.append(row[0])

print(f"Total de RUCs en archivo de faltantes (antes): {len(pending_rucs)}")

# Filtrar RUCs que NO han sido scrapeados
filtered_rucs = [ruc for ruc in pending_rucs if ruc not in scraped_rucs]
removed_count = len(pending_rucs) - len(filtered_rucs)

print(f"RUCs eliminados (ya scrapeados): {removed_count}")
print(f"RUCs restantes por scrapear: {len(filtered_rucs)}")

# Guardar RUCs filtrados en el mismo archivo
print("\nGuardando archivo actualizado...")
with open('rucs/ruc_faltante_osiptel_parte1.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['RUC'])  # Header
    for ruc in filtered_rucs:
        writer.writerow([ruc])

print("✓ Proceso completado!")
print(f"\nResumen:")
print(f"  - RUCs originales: {len(pending_rucs)}")
print(f"  - RUCs ya scrapeados (eliminados): {removed_count}")
print(f"  - RUCs por scrapear (restantes): {len(filtered_rucs)}")
