import csv


def read_txt_file(txt_file):
    data = []
    with open(txt_file, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            pdbid_chain = lines[i].strip().split('_')
            pdbid = pdbid_chain[0]
            chain_id = pdbid_chain[1]
            sequence = lines[i+1].strip()
            interface_residues = lines[i+2].strip()
            data.append((pdbid, chain_id, sequence, interface_residues))
    return data

def write_csv_file(data, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['PDBID', 'ChainID', 'Sequence', 'Interface'])
        for entry in data:
            writer.writerow(entry)