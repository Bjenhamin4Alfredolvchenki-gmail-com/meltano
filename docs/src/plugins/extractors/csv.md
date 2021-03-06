---
sidebar: auto
metaTitle: Extract Data from CSV
description: Use Meltano to extract raw data from any CSV and insert it into Postgres, Snowflake, and more. 
---

# Comma Separated Values (CSV)

The [CSV Extractor](https://gitlab.com/meltano/tap-csv) can be used to load CSV files to a Database or Data Warehouse. 

Each input CSV file used with the [CSV Extractor](https://gitlab.com/meltano/tap-csv) must be a traditionally-delimited CSV (comma separated columns, newlines indicate new rows, double quoted values).

The first row is the header defining the attribute name for that column and will result to a column of the same name in the database. It must have a valid format with no spaces or special characters (like for example `!` or `@`, etc).

You can check the following files as an example of valid CSV files:

- [GitFlixUsers.csv](/files/GitFlixUsers.csv)
- [GitFlixEpisodes.csv](/files/GitFlixEpisodes.csv)
- [GitFlixStreams.csv](/files/GitFlixStreams.csv)

Those files were generated by exporting Google Sheets to CSV. By exporting to CSV from most spreadsheet applications, you can be sure that the format of the CSV files will be supported by the CSV Extractor.

## Setup

The [CSV Extractor](https://gitlab.com/meltano/tap-csv) needs a definition file in the `extract/` directory of your Meltano project:

**[files-def.json](/files/files-def.json)**

```json
[
  { "entity": "users", "file": "extract/GitFlixUsers.csv", "keys": ["id"] },
  { "entity": "episodes", "file": "extract/GitFlixEpisodes.csv", "keys": ["id"] },
  { "entity": "streams", "file": "extract/GitFlixStreams.csv", "keys": ["id"] }
]
```

This file allows us to define the CSV files that the CSV Extractor is going to extract data from. The available options are as follows:

- entity: The entity name, used as the table name for the data loaded from that CSV.
- file: Local path (relative to the project's root) of the file to be loaded.
- keys: The names of the columns that constitute the unique keys for that entity.

You can download the example csv files and the `files-def.json` file in the `extract/` directory of your Meltano project and test the CSV Extractor.

## Command Line Installation

1. Navigate to your Meltano project in the terminal
2. Run the following command:

```bash
meltano add extractor tap-csv
```

If you are successful, you should see `Added and installed extractors 'tap-csv'` in your terminal.

### Configuration

1. Open your project's `.env` file in a text editor
1. Add the following variable to your file:

**.env**

```bash
export TAP_CSV_FILES_DEFINITION="extract/files_def.json"
```

Where `files_def.json` is the json file described in the Setup section.

Check the [README](https://gitlab.com/meltano/tap-csv#run) for details.

::: tip

**Ready to do more with data from CSV files?** 

Check out our [Loading CSV files into a Postgres Database tutorial](/tutorials/csv-with-postgres.html) to learn how you can create an analytics database from within Meltano, and start analyzing your CSV data.

:::

