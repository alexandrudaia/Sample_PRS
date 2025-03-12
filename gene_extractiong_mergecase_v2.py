import csv
from multiprocessing import Pool
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

# Function to retrieve gene and consequence information
def get_snp_info(snp_id):
    # Each process creates its own session
    with requests.Session() as session:
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            url = f"https://www.ncbi.nlm.nih.gov/snp/rs{snp_id}"
            while True:
                response = session.get(url, timeout=10)
                if response.status_code != 200:
                    return "Failed to retrieve data"

                soup = BeautifulSoup(response.content, 'html.parser')

                # Check for SNP merge information
                status = soup.find('dt', string='Status')
                if status and status.find_next_sibling('dd'):
                    merge_link = status.find_next_sibling('dd').find('a')
                    if merge_link and merge_link.get('href'):
                        new_snp_id = merge_link.get('href').split('/')[-1].replace('rs', '')  # Extract new SNP ID from the link
                        snp_id = new_snp_id.strip()
                        url = f"https://www.ncbi.nlm.nih.gov/snp/{new_snp_id}"  # Update the URL with the new SNP ID
                        continue  # Continue with the new SNP ID

                gene_consequence = "Not found"
                elements = soup.find_all(['dt', 'dd'])
                for i, elem in enumerate(elements):
                    if 'Gene : Consequence' in elem.get_text():
                        if i + 1 < len(elements):
                            # Extracting all gene:consequence pairs from the <dd> tag
                            gene_consequence_pairs = elements[i + 1].find_all(['div', 'span'])
                            gene_consequence = ', '.join([pair.get_text(strip=True) for pair in gene_consequence_pairs])
                            break

                return gene_consequence

        except requests.exceptions.RequestException as e:
            print(f"Request failed for SNP ID {snp_id}: {e}")
            return None

# Updated function to process each row in the pool and print a message
def process_row(row):
    snp_id = row[0]  # Assuming SNP ID is in the first column
    gene_consequence = get_snp_info(snp_id)

    # Print message after processing each entry
    print(f"Processed SNP ID {snp_id}: Gene consequence - {gene_consequence if gene_consequence is not None else 'Error'}")

    # Append the gene consequence information to the row
    row.append(gene_consequence if gene_consequence is not None else 'Error')
    return row

# Main function that sets up multiprocessing
def main(input_file_path, output_file_path, num_processes):
    with open(input_file_path, mode='r') as infile, open(output_file_path, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # The first row is the header
        header = next(reader)
        header.append('Gene : Consequence')
        writer.writerow(header)

        # Read the rest of the rows from the input file
        rows = list(reader)

        # Create a pool of worker processes
        with Pool(processes=num_processes) as pool:
            # Map process_row to the rows, processing in parallel
            results = pool.map(process_row, rows)

            # Write results to the output file
            writer.writerows(results)

    print("Processing complete. Check the output in 'snp_gene_consequences_merge.csv'")

# Entry point for running the script
if __name__ == "__main__":
    input_file_path = 'sample_with_id.csv'
    output_file_path = 'test_no3.csv'
    num_processes = 4
    main(input_file_path, output_file_path, num_processes)
