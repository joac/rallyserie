# coding: utf-8
import os
import csv
import sys
import glob
from collections import defaultdict, Counter

def fix_name(raw):
    cleaned = raw.replace('´', '').replace('N~', 'Ñ').strip()
    if ',' in cleaned:
        last, first = cleaned.split(', ')
        return f'{first} {last}'
    return cleaned


def clean_data(file):
    with open(file) as fh:
        data = fh.readlines()
    valid = [l.strip().split('\t') for l in data if not l.strip().isnumeric()]
    
    header = valid[0]
    return header, valid[1:] 


def filtar_por_carreras(cantidad):
    return list(sorted((corredor for corredor, resultados in corredor_resultados.items() if len(resultados) == cantidad)))

def format_resultados(resultados):
    return ' '.join((f"{k}: {v}" for k, v in resultados.items()))

corredores_fecha = []

corredor_resultados = defaultdict(dict)
corredor_puntos = Counter()

for file in sorted(glob.glob('2022/*.csv')):
    header, data = clean_data(file)
    corredores = {fix_name(row[2]) for row in data} 
    _, fecha = os.path.splitext(os.path.basename(file))[0].split('_', maxsplit=1)

    for row in data:
        name = fix_name(row[2])
        position = int(row[0])
        puntos = int(row[-1])
        corredor_resultados[name][fecha] = position
        corredor_puntos[name] += puntos

    corredores_fecha.append(corredores)

print("# Rally serie 2022 - Categoria Promo B (30-40 años)")
print()
total = len(corredor_resultados)
print('## Corredores totales')
print(total)

print('## Participacion')
for cantidad in range(1, 5):
    numero_participantes = len(filtar_por_carreras(cantidad))

    print(f' - {cantidad} carreras {numero_participantes:2d}    ({round(numero_participantes/total*100, 1)}%)') 

print()
print('## Resultados Campeonato')
for pos, (corredor, puntos) in enumerate(corredor_puntos.most_common(), 1):
    print(f' - **{pos}** - ({puntos:2d}) _({len(corredor_resultados[corredor])} fechas)_ **{corredor.title()}**  _({format_resultados(corredor_resultados[corredor])})_')

print()
print("## Cantidad de fechas")
for cant in range(5, 0, -1):
    print(f"### {cant}")
    # Ineficiente, pero... son 77 filas
    for corredor, puntos in corredor_puntos.most_common():
        resultados = corredor_resultados[corredor]
        if len(resultados) == cant:
            print(f' - ({puntos:2d}) **{corredor.title()}**  _({format_resultados(corredor_resultados[corredor])})_')
