import csv

def write_line_to_csv(file_path, line):
    """
    Opens the CSV file in append mode and writes the provided line.
    If 'line' is a string, it splits the string by commas to convert it into a list.
    
    :param file_path: Path to the CSV file.
    :param line: A string or list representing a row in the CSV.
    """
    # If line is a string, split it using commas.
    if isinstance(line, str):
        line = line.split(',')
    
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(line)

# Your provided line as a string:
# line = '\nGRB150110923,1,1.61,289.64,32.71,0.3,289.36,32.522,1105025552,1105046072,1104962912,17.39996282,23.09996282,0.009,0.05'

# # Write the line to 'archivo.csv'
# write_line_to_csv('archivo.csv', line)
