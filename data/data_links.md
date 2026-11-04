# ECON 499R data download links

Checked Nov 1, 2026. "Script" = fetched by download_all.py. "Browser" = the site blocks scripts or needs a login; download by hand into raw/.

## 1. Core panel (Methods Memo Steps 1 to 4)

| Data | Direct link | Used for | How |
| --- | --- | --- | --- |
| EIA net generation by state, fuel, producer (1990-2025) | https://www.eia.gov/electricity/data/state/annual_generation_state.xlsx | Renewable share (ES), solar/wind shares, fossil-to-renewable ratio | Script |
| EIA capacity by state and fuel (1990-2025) | https://www.eia.gov/electricity/data/state/existcapacity_annual.xlsx | New renewable MW | Script |
| EIA planned capacity by state | https://www.eia.gov/electricity/data/state/plancapacity_annual.xlsx | Georgia outlook | Script |
| EIA retail sales, revenue, customers by state and sector (2010-2025) | https://www.eia.gov/electricity/data/state/xls/861/HS861%202010-.xlsx | Consumption (EC), efficiency (EE), price control | Script |
| EIA power-sector emissions by state | https://www.eia.gov/electricity/data/state/emission_annual.xlsx | CO2 check (ends 2024) | Script |
| EIA fuel use for generation by state | https://www.eia.gov/electricity/data/state/annual_consumption_state.xlsx | Optional | Script |
| EIA SEDS, all-fuel energy use (1960-2024) | https://www.eia.gov/state/seds/sep_use/total/csv/use_all_btu.csv | Paper-matching consumption check (series TETCB) | Script |
| BLS QCEW, data centers (NAICS 518210) | https://data.bls.gov/cew/data/api/2025/a/industry/518210.csv (swap the year, 2014-2025) | AI measure | Script |
| BLS QCEW, computer systems design (NAICS 5415) | https://data.bls.gov/cew/data/api/2025/a/industry/5415.csv | Tech-worker share (H2a) | Script |
| BLS QCEW, all industries (code 10) | https://data.bls.gov/cew/data/api/2025/a/industry/10.csv | AI denominator | Script |
| BEA GDP by state and industry (SAGDP, 1997-2025) | https://apps.bea.gov/regional/zip/SAGDP.zip | GDP, real GDP, manufacturing and farm GDP | Script |
| BEA income and population by state (SAINC) | https://apps.bea.gov/regional/zip/SAINC.zip | Population | Script |
| Census 2020 county Gazetteer | https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip | Land area, state centroids (distance matrix) | Script |
| Census county adjacency 2023 | https://www2.census.gov/geo/docs/reference/county_adjacency/county_adjacency2023.txt | Shared-border matrix | Script |

## 2. Utility and company financials

| Data | Direct link | Used for | How |
| --- | --- | --- | --- |
| FERC Form 1 income statements (PUDL) | https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/stable/out_ferc1__yearly_income_statements_sched114.parquet | Utility revenue, expenses, net income | Script |
| FERC Form 1 plant in service by type (PUDL) | https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/stable/out_ferc1__yearly_plant_in_service_sched204.parquet | Steam, nuclear, hydro, other, solar, wind, storage plant value | Script |
| FERC Form 1 plant-level costs (PUDL) | https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/stable/out_ferc1__yearly_all_plants.parquet | Capital cost per kW, fuel and O&M per MWh by technology | Script |
| FERC Form 1 steam plant fuel mix (PUDL) | https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/stable/out_ferc1__yearly_steam_plants_fuel_by_plant_sched402.parquet | Split coal vs gas steam plants | Script |
| Other PUDL tables (rate base, utility plant summary, EIA utilities, co-op RUS 7/12) | https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/stable/ + table name + .parquet (catalog: https://data.catalyst.coop/) | Optional | Script |
| SEC XBRL company facts | https://data.sec.gov/api/xbrl/companyfacts/CIK0000092122.json (Southern Co; swap the 10-digit CIK) | 58 utility, clean and fossil companies | Script (scripts/sec_fin.py; set SEC_USER_AGENT) |
| RMI Utility Transition Hub | https://utilitytransitionhub.rmi.org/data-download/ | Utility finances, investments, emissions (CSV) | Browser |
| Lazard LCOE+ 2026 (Jul 13, 2026) | https://www.lazard.com/media/kcfconhf/lazards-lcoeplus_vf.pdf | New-build cost per MWh by technology | Script |
| Stock prices and returns | Bloomberg terminal, Goizueta Business Library: https://libraries.emory.edu/business/research-learning/databases/bloomberg | Finance side | Browser (Emory licenses forbid scripts) |

## 3. Georgia case box

| Data | Direct link | How |
| --- | --- | --- |
| 2025 IRP main document (SELC-hosted copy of the Docket 56002 filing) | https://www.selc.org/wp-content/uploads/2025/03/2025-IRP-Main-Document.pdf | Script |
| 2025 IRP full filing with technical appendices | https://psc.ga.gov/search/facts-document/?documentId=221233 | Browser |
| 2025 IRP table of contents (SELC) | https://www.selc.org/wp-content/uploads/2025/02/2025-IRP-TOC.pdf | Script |
| 2025 IRP one-page summary | https://www.georgiapower.com/content/dam/georgia-power/pdfs/about/2025-irp-one-page-summary.pdf | Script |
| 2023 IRP Update main document | https://georgiapower.com/content/dam/georgia-power/pdfs/company-pdfs/2023-irp-update-main-document.pdf | Script |
| Large Load Economic Development Report, Q1 2026 (May 15, 2026) | https://services.psc.ga.gov/api/v1/External/Public/Get/Document/DownloadFile/226607/107887 | Script |
| Later large-load reports (Q2, Q3 2026) | Docket pages https://psc.ga.gov/search/facts-docket/?docketId=55378 and https://psc.ga.gov/search/facts-docket/?docketId=56002 | Browser |
| Large-load reports Q1 2024 to Q1 2026 as one table (third party; check against PDFs) | https://www.kadoa.com/datacenter/power/georgia | Browser |
| Certification of about 10,000 MW (Dec 19, 2025) | Dockets 56298 and 56310: https://psc.ga.gov/search/facts-docket/?docketId=56298 | Browser |

## 4. Stretch variables and alternative AI measures

| Data | Direct link | Used for | How |
| --- | --- | --- | --- |
| NOAA heating and cooling degree days by state | https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/9/hdd/12/12/2010-2025.csv (9 = Georgia; codes 1-48 = contiguous states alphabetically; swap hdd/cdd) | Weather control | Script (no AK or HI) |
| NSF state R&D, Table 10, one year per edition | https://ncses.nsf.gov/pubs/nsf26313/assets/data-tables/tables/nsf26313-tab010.xlsx (2023); nsf25326 (2022), nsf24318 (2021), nsf23321 (2020), nsf22320 (2019), nsf21325 (2018), nsf20307 (2017), same pattern | R&D moderator | Script |
| Census ACS S2801 broadband (percent of households) | https://api.census.gov/data/2024/acs/acs1/subject?get=NAME,S2801_C02_014E&for=state:*&key=YOUR_KEY (free key: https://api.census.gov/data/key_signup.html) | Broadband moderator; 2015 uses S2801_C02_012E because 014E means mobile broadband that year; no 2020 1-year release | Script with CENSUS_KEY |
| LBNL RPS and CES targets (June 2026 data update) | https://emp.lbl.gov/projects/renewables-portfolio ("RPS & CES Targets and Demand" XLSX); also https://eta-publications.lbl.gov/publications/us-state-electricity-resource-0 | Renewable mandate control | Browser for emp.lbl.gov; the eta-publications host works by script |
| Epoch AI frontier data centers | https://epoch.ai/data/data_centers/data_centers.csv | Data-center MW (large AI campuses only) | Script |
| Cleanview data center tracker | https://www.cleanview.co/data-centers ; 50-state capacity report https://cleanview.co/reports/geography-of-compute ; sample CSVs https://www.cleanview.co/samples | Data-center MW by state | Browser (full export may need an account) |
| More Than Just Parks tracker | https://morethanjustparks.com/data-center-tracker | Data-center sites by state | Browser |
| USPTO AI Patent Dataset 2023 | https://www.uspto.gov/ip-policy/economic-research/research-datasets/artificial-intelligence-patent-dataset (bulk: https://data.uspto.gov/bulkdata/datasets/ecopatai) | Alternative AI measure (patents through 2023) | Browser (about 764 MB) |
| PatentsView inventor locations (now on USPTO Open Data Portal) | https://data.uspto.gov/support/transition-guide/patentsview | Assign AI patents to states | Browser |
| Stanford AI Index 2026 (AI job postings by state, Lightcast) | https://hai.stanford.edu/ai-index | Alternative AI measure; selected states only | Browser |
| LBNL Utility-Scale Solar (for a solar cost projection) | https://emp.lbl.gov/utility-scale-solar | Georgia solar cost module | Browser |
