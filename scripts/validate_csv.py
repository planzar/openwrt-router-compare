import csv
import sys
import re

def main():

    notes_ids = set()
    
    # Validate notes.csv
    with open('notes.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            notes_header = next(reader)
        except StopIteration:
            print("Error: notes.csv is empty")
            sys.exit(1)
            
        notes_header_len = len(notes_header)
        if notes_header_len < 2:
            print(f"Error: notes.csv must have at least 2 columns, got {notes_header_len}")
            sys.exit(1)
            
        for row_num, row in enumerate(reader, start=2):
            if len(row) != notes_header_len:
                print(f"Error: notes.csv row {row_num} has {len(row)} columns, expected {notes_header_len}")
                sys.exit(1)
            if not row[0].isdigit():
                print(f"Error: notes.csv row {row_num} id is not a number: {row[0]}")
                sys.exit(1)
            notes_ids.add(row[0])
            
    # Validate data.csv
    with open('data.csv', 'r', encoding='utf-8') as f:
        # Use strict=True to catch unescaped quotes
        reader = csv.reader(f, strict=True)
        try:
            data_header = next(reader)
        except StopIteration:
            print("Error: data.csv is empty")
            sys.exit(1)
            
        header_len = len(data_header)
        
        for row_num, row in enumerate(reader, start=2):
            if len(row) != header_len:
                print(f"Error: data.csv row {row_num} has {len(row)} columns, expected {header_len}")
                sys.exit(1)
                
            # Check footnotes in cells [id]
            for col_idx, cell in enumerate(row):
                footnotes = re.findall(r'\[(\d+)\]', cell)
                for fn in footnotes:
                    if fn not in notes_ids:
                        print(f"Error: data.csv row {row_num}, column '{data_header[col_idx]}' references unknown footnote [{fn}]")
                        sys.exit(1)

    print("CSV validation passed.")

if __name__ == "__main__":
    try:
        main()
    except csv.Error as e:
        print(f"CSV parsing error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
