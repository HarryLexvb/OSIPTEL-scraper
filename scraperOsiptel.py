"""
OSIPTEL Scraper - Telephone Lines Information Extractor
Author: Harold Alejandro Villanueva Borda
License: MIT
Version: 1.0.0

This script automates the extraction of telephone line information
from the OSIPTEL (Peruvian telecommunications regulator) database.
Supports single RUC queries and batch processing from CSV/Excel files.
"""

import asyncio
import csv
import pandas as pd
from camoufox import AsyncCamoufox
from pathlib import Path
from datetime import datetime
import os

async def scrape_osiptel_single(document_number):
    """
    Scrapes OSIPTEL database for telephone lines associated with a RUC
    
    Args:
        document_number (str): RUC number (Tax ID) to query
    
    Returns:
        dict: Contains 'success' status, 'ruc', and 'data' (list of lines)
    """
    async with AsyncCamoufox(
        headless=True,
        humanize=True,
        timeout=120000
    ) as browser:
            
            page = await browser.new_page()
            url = "https://checatuslineas.osiptel.gob.pe/"
            
            try:
                await page.goto(url, timeout=120000, wait_until='networkidle')
                
                # Wait for form to load completely
                await page.wait_for_selector('#IdTipoDoc', timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Select RUC document type (type 2)
                await page.evaluate('document.getElementById("IdTipoDoc").value = "2"')
                await page.wait_for_timeout(500)
                
                # Enter document number
                await page.evaluate(f'document.getElementById("NumeroDocumento").value = "{document_number}"')
                await page.wait_for_timeout(500)
                
                # Click search button
                await page.evaluate('document.getElementById("btnBuscar").click()')
                
                # Wait for table to load
                await page.wait_for_timeout(6000)
                
                # Change record selector to display 100 records
                await page.evaluate('''() => {
                    const selector = document.querySelector('select[name="GridConsulta_length"]');
                    if (selector) {
                        let hasOption = false;
                        for (let option of selector.options) {
                            if (option.value === '100') {
                                hasOption = true;
                                break;
                            }
                        }
                        if (!hasOption) {
                            const newOption = document.createElement('option');
                            newOption.value = '100';
                            newOption.text = '100';
                            selector.add(newOption);
                        }
                        selector.value = '100';
                        const event = new Event('change', { bubbles: true });
                        selector.dispatchEvent(event);
                    }
                }''')
                
                # Wait for table to update
                await page.wait_for_timeout(5000)
                
                # Extract all data from table
                data = await page.evaluate('''() => {
                    const table = document.getElementById("GridConsulta");
                    if (!table) return [];
                    
                    const rows = table.rows;
                    const data = [];
                    
                    for (let i = 1; i < rows.length; i++) {
                        const row = rows[i];
                        
                        // Skip pager row
                        if (row.className && row.className.includes('GridPager')) {
                            continue;
                        }
                        
                        const cells = row.cells;
                        if (!cells || cells.length < 3) continue;
                        
                        const rowData = [];
                        for (let j = 0; j < cells.length; j++) {
                            const cellText = cells[j].innerText ? cells[j].innerText.trim() : '';
                            rowData.push(cellText);
                        }
                        
                        if (rowData.length >= 3 && rowData[0]) {
                            data.push(rowData);
                        }
                    }
                    
                    return data;
                }''')
                
                if len(data) == 0:
                    print(f"⚠️  RUC {document_number}: No registered telephone lines")
                else:
                    print(f"✓ RUC {document_number}: {len(data)} lines found")
                
                return {
                    'success': True,
                    'ruc': document_number,
                    'data': data
                }
                
            except Exception as e:
                print(f"❌ Error processing RUC {document_number}: {str(e)}")
                return {
                    'success': False,
                    'ruc': document_number,
                    'error': str(e),
                    'data': []
                }

async def scrape_multiple_rucs(rucs):
    """
    Sequential scraper for multiple RUCs (one by one to avoid server bans)
    
    Args:
        rucs (list): List of RUC numbers to process
    
    Returns:
        list: List of results for all RUCs
    """
    results = []
    total = len(rucs)
    
    # Process one by one
    for idx, ruc in enumerate(rucs, 1):
        print(f"\n[{idx}/{total}] Processing RUC: {ruc}")
        result = await scrape_osiptel_single(ruc)
        results.append(result)
        
        # Pause between requests to avoid server bans
        if idx < total:
            await asyncio.sleep(2)
    
    return results

def format_results_to_csv(results, output_file="resultados_osiptel.csv"):
    """
    Formats results and saves them to CSV with indexed columns
    
    Format: RUC, Modalidad_1, Número_Telefónico_1, Empresa_Operadora_1, ...
    
    Args:
        results (list): List of scraping results
        output_file (str): Output CSV filename
    
    Returns:
        str: Output filename
    """
    rows = []
    
    for result in results:
        if not result['success'] or not result['data']:
            # Add RUC without data
            rows.append({'RUC': result['ruc']})
            continue
        
        row = {'RUC': result['ruc']}
        
        # Add each line with its index
        for idx, line_data in enumerate(result['data'], 1):
            if len(line_data) >= 3:
                row[f'Modalidad_{idx}'] = line_data[0]
                row[f'Número_Telefónico_{idx}'] = line_data[1]
                row[f'Empresa_Operadora_{idx}'] = line_data[2]
        
        rows.append(row)
    
    # Create DataFrame and save
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ File saved: {output_file}")
    return output_file

def read_rucs_from_file(file_path):
    """
    Reads RUCs from Excel or CSV file
    
    Args:
        file_path (str): Path to Excel (.xlsx, .xls) or CSV file
    
    Returns:
        list: List of RUC numbers (as strings)
    """
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported format. Use .xlsx, .xls or .csv")
    
    # Get first column and convert to string
    rucs = df.iloc[:, 0].astype(str).str.strip().tolist()
    # Filter empty values or NaN
    rucs = [ruc for ruc in rucs if ruc and ruc != 'nan']
    
    return rucs

async def main():
    """
    Main function - Interactive menu for single or batch RUC processing
    """
    print("="*60)
    print("     SCRAPER OSIPTEL - CONSULTA DE LÍNEAS TELEFÓNICAS")
    print("="*60)
    print("\nSeleccione una opción:")
    print("1. Ingresar un RUC manualmente")
    print("2. Cargar archivo (Excel o CSV)")
    print("="*60)
    
    opcion = input("\nIngrese opción (1 o 2): ").strip()
    
    if opcion == "1":
        # Opción 1: Ingresar RUC manualmente
        ruc = input("Ingrese el RUC: ").strip()
        
        print(f"\n🚀 Iniciando scraping para RUC: {ruc}")
        print("-"*60)
        
        result = await scrape_osiptel_single(ruc)
        
        # Generar CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"resultado_{ruc}_{timestamp}.csv"
        format_results_to_csv([result], output_file)
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("📊 RESUMEN")
        print("="*60)
        if result['success']:
            print(f"RUC: {result['ruc']}")
            print(f"Total de líneas: {len(result['data'])}")
        else:
            print(f"Error al procesar RUC {ruc}")
    
    elif opcion == "2":
        # Opción 2: Cargar archivo
        file_path = input("Ingrese la ruta del archivo (Excel o CSV): ").strip()
        
        # Remover comillas si las hay
        file_path = file_path.strip('"').strip("'")
        
        if not os.path.exists(file_path):
            print(f"❌ Error: El archivo no existe: {file_path}")
            return
        
        print(f"\n📂 Leyendo archivo: {file_path}")
        rucs = read_rucs_from_file(file_path)
        
        print(f"✓ Se encontraron {len(rucs)} RUCs")
        print(f"⚙️  Processing sequentially (one by one) to avoid server bans")
        print("-"*60)
        
        # Process all RUCs sequentially
        results = await scrape_multiple_rucs(rucs)
        
        # Generar CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"resultados_osiptel_{timestamp}.csv"
        format_results_to_csv(results, output_file)
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("📊 RESUMEN GENERAL")
        print("="*60)
        exitosos = sum(1 for r in results if r['success'])
        con_datos = sum(1 for r in results if r['success'] and len(r['data']) > 0)
        sin_datos = sum(1 for r in results if r['success'] and len(r['data']) == 0)
        errores = sum(1 for r in results if not r['success'])
        
        print(f"Total de RUCs procesados: {len(results)}")
        print(f"  ✓ Exitosos: {exitosos}")
        print(f"  📱 Con líneas telefónicas: {con_datos}")
        print(f"  ⚠️  Sin líneas telefónicas: {sin_datos}")
        print(f"  ❌ Con errores: {errores}")
        print("="*60)
    
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    asyncio.run(main())
