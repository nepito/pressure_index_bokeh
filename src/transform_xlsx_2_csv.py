import os

all_files_in_data = [file for _, _, file in os.walk("/workdir/data")][0]
all_files_xlsx = [file for file in all_files_in_data if file.split(".")[1] == "xlsx"]
files_to_change = [file[20:29] for file in all_files_xlsx if file[0:11] == "IG_POSICION"]


def return_transformation_command(date: str):
    return f"in2csv /workdir/data/IG_POSICION_TRAMPAS_{date}.xlsx > /workdir/data/IG_POSICION_TRAMPAS_{date}.csv"


for file in files_to_change:
    os.system(return_transformation_command(file))