# Lily Rudin

## Description

Generative AI has spread faster than almost any previous technology, but adoption is uneven across countries. This project asks whether AI adoption is following existing economic and digital divides, and whether the countries whose workforces are most exposed to generative AI are the ones adopting it least. 

I will join four international sources by ISO3 country code and year to compare AI investment, adoption, and workforce exposure, using World Bank indicators for economic context and its region/income-group classifications as a hierarchy. Planned visualizations include a world map of workforce exposure, time series of business AI adoption, a treemap by income group and region, and a scatterplot of GDP per capita against AI adoption.

## Data Sources

### Data Source 1: World Bank World Development Indicators (WDI)

URL: https://databank.worldbank.org/source/world-development-indicators

Size: ~33,000 rows, 8 columns (estimated: ~10 indicators × 217 economies × 2010–2024)

The WDI is the World Bank's primary collection of country-level development indicators, available through a free API with no key required. I will pull GDP per capita, internet use, education, and population. Each country includes a region and income group, which I'll use for aggregation and drill-downs.

### Data Source 2: ILO Generative AI Occupational Exposure Index + ILOSTAT Employment by Occupation

URL: https://www.ilo.org/node/706766 (exposure index, ILO Working Paper 140) and https://ilostat.ilo.org/data/ (employment data)

Size: Exposure index: ~430 rows, ~5 columns (one row per ISCO-08 occupation). ILOSTAT employment by sex and occupation: ~100,000 rows, ~8 columns (estimated: ~150 countries × 10 years × ~45 occupation categories × 3 sex categories)

The ILO's 2025 index scores occupations by their exposure to generative AI. Joining it to ILOSTAT employment data will give each country's share of workers in exposed occupations, by sex. Many countries report occupations only at the 1- or 2-digit level, so I may need to aggregate the scores.

### Data Source 3: OECD ICT Access and Usage by Businesses

URL: https://oe.cd/dx/ict-access-usage

Size: ~30,000 rows, ~15 columns (estimated, after filtering to AI-related indicators; SDMX CSV export)

Official survey data on enterprise AI use from 2005–2024, broken down by firm size and industry. Covers only ~40 OECD and partner countries, so detailed adoption analysis will focus on this group.

### Data Source 4: Stanford HAI AI Index Report 2026 (Public Data)

URL: https://hai.stanford.edu/ai-index/2026-ai-index-report

Size: ~3,000 rows, ~5 columns (estimated, after combining ~5 country-level series)

Annual Report on Stanford's Institute for Human-Centered AI that complies dara on AI research, investment, adoption, and policy. Data is published per chart, so I'll select and reshape country-level series such as private AI investment, notable models, and generative AI adoption. Coverage varies by chart.


## Questions

1. All four sources are aggregate indicators rather than individual records. In long format (country × year × indicator × breakdown), the combined dataset is in the tens of thousands of rows. Is this acceptable, or would you like me to add a record-level source, such as the USPTO AI Patent Dataset with inventor country?
2. Country coverage varies a lot between sources (~40 countries for OECD vs. ~200 for the World Bank). Is a two-layer approach (global layer + OECD core) reasonable, or should I limit the whole project to countries covered by all four sources?
3. None of these sources has an obvious network structure. Would a country-to-country network (for example, OECD data on international co-invention) be expected, and if so, is it fine to add it as a fifth source?
4. The sources define "AI use" differently (official firm surveys, population adoption estimates, occupational exposure scores). Is presenting these side by side, rather than combining them into a single index, an appropriate approach for this project?