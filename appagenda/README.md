## Generating the Schedule and Attendees for the Whova App

This directory contains the data files and code used to generate the agenda and attendees for the NAACL 2019 official Whova app. To do this, it relies on the code and data provided by the [NAACL 2019 schedule repository](https://github.com/naacl-org/naacl-schedule-2019), which is used as a submodule in this repository. This is structured in this way because it makes it much easier to allow syncing any changes in the data files much easier across both the websites and the apps and also allows for code sharing.

### Setting Up

In order to run the code in this repository, you first need to create a [conda](https://conda.io/en/latest/) environment. First you should [install miniconda](https://conda.io/en/latest/miniconda.html). Once you have it installed, run the following to create the Python environment:

```bash
conda create -n naacl2019 -c conda-forge --file agenda/requirements.txt
```

This will create a conda environment called `naacl2019` which you will need to "activate" before running any of the code. To activate this environment, run:

```bash
conda activate naacl2019
```

### Contents 

The main file in this directory is `generate.py`. This is the main driver script that generates the spreadsheets for the agenda and attendees that can then be imported into the Whova Event Management System (EMS). This script uses the classes defined in the `orderfile.py` module from the NAACL 2019 schedule repository that is integrated as a submodule in this repository under the `agenda` directory. It takes as input a single JSON configuration file that contains the following fields:
    
    - `order_files` : A dictionary mapping the names for the events to the respective prder files. 
    
    - `mapping_files` : A dictionary with the event names as keys and the paths to the event's mapping files (mapping the anthology IDs to the START / order file IDs for the event) as the values.
        
    - `extra_metadata_files` : A dictionary with the event names as keys and the paths non-anthology metadata TSV files for the event as values.  These files contain the title, authors, and abstracts for the event items that are not in the anthology (e.g., TACL papers, non-archival workshop papers, etc.)
    
    - `xml_files` : List of all XML files from the Anthology containing the titles, authors, abstracts, and anthology URLs for all of the items across all of the events

    - `plenary_info_file` : Another optional TSV file containing additional info about some of the plenary sessions (e.g., keynote abstracts etc.)
    
    - `attendees_file` : An optional Excel file containing information about folks who are registered for the conference. This file is generally provided by Priscilla. This file is not available in the repository since it contains personal information about the conference attendees.
    
    - `pdf_links` : A boolean indicating whether to generate links in the agenda to anthology PDFs or PDFs specified in the extra metadata files.
    
    - `video_links` : A boolean indicating whether to generate links in the schedule to the talk videos hosted on Vimeo/YouTube or other video platforms.

The script `generate.py` also relies on two additional files that are assumed to be there in the `appagenda` diretory but aren't explicitly specified as inputs:
    
    - `Agenda_Track_Template.xlsx ` : This template file for the agenda and the speakers can be downloaded from the Whova EMS and is populated by `generate.py` to produce the first output file below.
    
    - `Attendee_list_template.xlsx` : This template file for attendees can also be downlaoded from teh Whova EMS and is populated by `generate.py` to produce the second output file below.

Both of these files are checked into the repository since they are empty and do not contain any actual information.

As output, `generate.py` produces two files:
    
    1. The first is an Excel files containing the detailed agenda and speakers for NAACL 2019 - across the main conference and all workshops. This Excel file contains two main sheets called "Agenda" and "Speaker". The "Agenda" sheet contains the schedule information including dates, start times, end times, session titles, abstracts, names of authors/speakers etc. The "Speaker" sheet contains the names, emails, and affiliations of all of the people who are authors and co-authors on any papers across the main conference and workshops. 
   
    2. The second output file is also an Excel file and contains names, emails, and affiliations for non-speaker attendees. That is, folks who are registered for the conference but aren't authors or co-authors on any papers. 

The script `generate.py` also relies on some utility functions that are defined in `utils.py`. For more details on these two scripts, please refer to the code and the comments in the scripts.

### Generating the Schedule

The following command will generate the agenda and attendee files at `appagenda/naacl19-agenda.xlsx` and `appagenda/naacl19-attendees.xlsx` respectively (without any PDF and video links). This command should be run in the top level of the cloned repository:

```
python appagenda/generate.py appagenda/config.json appagenda/naacl19-agenda.xlsx appagenda/naacl19-attendees.xlsx
```

The configuration file `config.json` is checked into the repository and looks like this:

```json
{
    "order_files": {
        "main": "agenda/data/order/manually_combined_order",
        "*SEM": "agenda/data/order/sem_order",
        "SemEval": "agenda/data/order/SemEval_order",
        "CLPsych": "agenda/data/order/clpsych_order",
        "DISRPT": "agenda/data/order/disrpt_order",
        "ESSP": "agenda/data/order/essp_order",
        "NeuralGen": "agenda/data/order/neuralgen_order",
        "NLP+CSS": "agenda/data/order/nlpcss_order",
        "RepEval": "agenda/data/order/repeval_order",
        "SiVL": "agenda/data/order/sivl_order",
        "SpLU-RoboNLP": "agenda/data/order/splu_order",
        "WASSA": "agenda/data/order/wassa_order",
        "ClinicalNLP": "agenda/data/order/clinicalnlp_order",
        "CMCL": "agenda/data/order/cmcl_order",
        "CRAC": "agenda/data/order/crac2019_order",
        "LaTECH-ClFl": "agenda/data/order/latechclfl_order",
        "WNU": "agenda/data/order/wnu_order",
        "NLLP": "agenda/data/order/nllp_order",
        "SLPAT": "agenda/data/order/slpat_order",
        "SPNLP": "agenda/data/order/spnlp_order",
        "VarDial": "agenda/data/order/vardial_order"
    },
    "mapping_files": {
        "main": "agenda/data/mapping/manually_combined_id_map.txt",
        "*SEM": "agenda/data/mapping/sem_id_map.txt",
        "SemEval": "agenda/data/mapping/SemEval_id_map.txt",
        "CLPsych": "agenda/data/mapping/clpsych_id_map.txt",
        "DISRPT": "agenda/data/mapping/disrpt_id_map.txt",
        "ESSP": "agenda/data/mapping/essp_id_map.txt",
        "NeuralGen": "agenda/data/mapping/neuralgen_id_map.txt",
        "NLP+CSS": "agenda/data/mapping/nlpcss_id_map.txt",
        "RepEval": "agenda/data/mapping/repeval_id_map.txt",
        "SiVL": "agenda/data/mapping/sivl_id_map.txt",
        "SpLU-RoboNLP": "agenda/data/mapping/splu_id_map.txt",
        "WASSA": "agenda/data/mapping/wassa_id_map.txt",
        "ClinicalNLP": "agenda/data/mapping/clinicalnlp_id_map.txt",
        "CMCL": "agenda/data/mapping/cmcl_id_map.txt",
        "CRAC": "agenda/data/mapping/crac2019_id_map.txt",
        "LaTECH-ClFl": "agenda/data/mapping/latechclfl_id_map.txt",
        "WNU": "agenda/data/mapping/wnu_id_map.txt",
        "NLLP": "agenda/data/mapping/nllp_id_map.txt",
        "SLPAT": "agenda/data/mapping/slpat_id_map.txt",
        "SPNLP": "agenda/data/mapping/spnlp_id_map.txt",
        "VarDial": "agenda/data/mapping/vardial_id_map.txt"
    },
    "extra_metadata_files": {
        "main": "agenda/data/extra-metadata/main.tsv",
        "NeuralGen": "agenda/data/extra-metadata/neuralgen.tsv",
        "NLLP": "agenda/data/extra-metadata/nllp.tsv",
        "WNU": "agenda/data/extra-metadata/wnu.tsv"
    },
    "xml_files": [
        "agenda/data/xml/N19.xml",
        "agenda/data/xml/S19.xml",
        "agenda/data/xml/W19.xml"
    ],
    "plenary_info_file": "agenda/data/plenary-info.tsv",
    "attendees_file": "appagenda/2019-NAACL-Registrations-for-App-May20.xlsx",
    "pdf_links": false,
    "video_links": false
}
```

Note that the two output files are _not_ checked into the repository since it contains personal information for conference attendees. You will also need to get the attendees file from Priscilla and modify `attendees_file` in the config file below. To add the PDF and video links where available, modify the above config file to have the values for `pdf_links` and `video_links` fields to be `true`. 

### Manual Tweaking