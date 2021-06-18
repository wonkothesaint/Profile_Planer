import openpyxl
from pathlib import Path
import json

dirname = Path(__file__).parent
project_dir = dirname.parent
database_dir = project_dir / "database"


def reduce_float_percision(f,p):
    formating = "{:."+str(p)+"f}"
    return float(formating.format(f))


def assets_excel_to_json(user):
    excel_path = database_dir / user / 'assets.xlsx'
    xlsx_file = Path('SimData', excel_path)
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active
    i = 2
    data = {}
    while not sheet["A" + str(i)].value is None:
        # print(sheet["B" + str(i)].value, sheet["B" + str(i)].number_format)
        # print(float(sheet["B" + str(i)].value[1:]. replace(',', '')))
        data[sheet["A" + str(i)].value] = {"value": float(sheet["B" + str(i)].value[1:].replace(',', '')),
                                           "deposit_fee_pct": reduce_float_percision(sheet["D" + str(i)].value, 4),
                                           "management_fees_yearly_pct": reduce_float_percision(sheet["F" + str(i)].value, 4),
                                           "yield_yearly_pct": reduce_float_percision(sheet["H" + str(i)].value, 4),
                                           "dividends_yield_yearly_pct": reduce_float_percision(sheet["J" + str(i)].value, 4),
                                           "tax_pct": reduce_float_percision(sheet["M" + str(i)].value, 4),
                                           "tax_dividends_pct": reduce_float_percision(sheet["N" + str(i)].value, 4),
                                           "gains": reduce_float_percision(sheet["L" + str(i)].value, 4)}
        i += 1
    print(data)
    json_path = database_dir / user / 'assets.json'
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, separators=(',', ': '))


def debts_excel_to_json(user):
    excel_path = database_dir / user / 'debts.xlsx'
    xlsx_file = Path('SimData', excel_path)
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active
    i = 2
    data = {}
    while sheet["A" + str(i)].value is not None:
        # print(sheet["B" + str(i)].value, sheet["B" + str(i)].number_format)
        # print(float(sheet["B" + str(i)].value[1:]. replace(',', '')))
        data[sheet["A" + str(i)].value] = {"loan_type": sheet["G" + str(i)].value,
                                           "date_start": sheet["C" + str(i)].value.strftime('%Y-%d-%m'),
                                           "ammount": float(sheet["F" + str(i)].value[1:].replace(',', '')),
                                           "duration": int(sheet["D" + str(i)].value),
                                           "interest": reduce_float_percision(sheet["B" + str(i)].value, 4)}
        i += 1
    json_path = database_dir / user / 'debts.json'
    print(data)
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, separators=(',', ': '))


assets_excel_to_json('Wonko')
debts_excel_to_json('Wonko')
