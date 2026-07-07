INPUT_FILES = ["0kg_przed.txt", "0kg_po.txt", "97kg.txt", "197kg.txt", "299kg.txt", "396kg.txt", "490kg.txt", "569kg.txt"]
OUTPUT_FILE = "usrednione_dane_wzorcowe.txt"


for input_file in INPUT_FILES:
    y_values = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            
            line = line.strip()
            if not line:
                continue
            
            try:
                parts = line.split("|")
                value = float(parts[1].strip())
                y_values.append(value)
            except (IndexError, ValueError):
                continue

    if not y_values:
        print("Brak poprawnych danych w pliku.")
        exit()

    sum = 0
    for y in y_values:
        sum += y

    average = sum / len(y_values)

    # x value to file is a filename without extension
    x_value = input_file.split(".")[0]
    with open(OUTPUT_FILE, "a", encoding="utf-8") as output_file:
        output_file.write(f"{x_value} | {average}\n")