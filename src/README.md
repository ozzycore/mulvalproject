## Source file explained
**Goal:** Building an Attack Graph using MulVAL.
**Prerequisite:**
1. Deploy an empty MySQL database.
2. Get Nessus/OVAL report.

**Process:**


1. Sync the vulnerability NVD data feeds to local database:
- `setup_nvd_database.py`: creates the 'nvd' database and table.
- `download_nvd_cves.sh`: downloads NVD's json files.
- `parse_nvd_cves.py`: iterating over each cve item (json), parsing and inserting into the 'nvd' table.
2. Based on the Nessus/OVAL reports, use NVD data and construct an valid MulVAL input file:
- `parse_nessus_xml.sh:` parses Nessus XML reports, uses the old Java 'NessusXMLParser' implementation.
- `retrieve_data_from_nvd.py`: retrieves the relevant CVE rows from MySQL based on the nessus xml report. Generates the predicates for the input file.
- `translate_nessus_scan.sh:` generates the final input file.
3. Generate an Attack Graph:
- Use the original `graph_gen.sh` script.

**General files:**
- `db_fucntions.py`: MySQL functionality - checking connection, generating database.
- `nvd_json_files`: Directory for storing NVD vulnerability data feeds. Moreover, the directory contains an example file - `example_nvdcve-1.1-2019.json`.
