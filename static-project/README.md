# Exposed, but Adopting? Generative AI Across Economic Divides

Lily Rudin

## Description

Generative AI has spread faster than almost any previous technology, but adoption is uneven across countries. This project asks two questions: does AI adoption follow existing economic divides, and are the countries whose workforces are most exposed to generative AI the ones adopting it least?

The project combines international data on workforce exposure and business adoption:

- **Exposure:** using ILO occupation data, it maps where clerical work, the occupation group the ILO finds most exposed to generative AI, makes up a large share of employment. It also looks at how the occupation mix changes with country income and how exposure differs between women and men.
- **Adoption:** using the OECD's survey of businesses, it compares the share of firms using AI across countries, against GDP per capita, between small and large firms, and across industries.

The final report (`static-project/static-viz/report.pdf`) presents eight static charts with a narrative and citations.

![World map of the share of employment in clerical jobs, by country](static-project/static-viz/figures/clerical_map.png)

## Data Sources

- **International Labour Organization (ILO), ILOSTAT.** Employment by sex and occupation, ISCO-08 major groups. https://ilostat.ilo.org/data/ (accessed {date}).
- **Gmyrek, P., Berg, J., Kamiński, K., Konopczyński, F., Ładna, A., Nafradi, B., Rosłaniec, K., & Troszyński, M. (2025).** *Generative AI and Jobs: A Refined Global Index of Occupational Exposure.* ILO Working Paper 140. Geneva: International Labour Office. https://doi.org/10.54394/HETP0387
- **OECD, ICT Access and Usage by Businesses database.** Share of enterprises using artificial intelligence, by industry and firm size. OECD Data Explorer, https://data-explorer.oecd.org/ (accessed {date}).
- **World Bank, World Development Indicators.** GDP per capita, PPP (current international $), indicator `NY.GDP.PCAP.PP.CD`. https://databank.worldbank.org/source/world-development-indicators (accessed {date}).
- **World Bank, country and lending group classifications.** Income groups. https://datahelpdesk.worldbank.org/knowledgebase/articles/906519 (accessed {date}).
- **Natural Earth**, 1:110m country boundaries, via vega-datasets `world-110m.json`. https://www.naturalearthdata.com/

## Reproducing the Report

From `static-project/`:

1. Install dependencies: `uv add altair pandas pycountry vl-convert-python reportlab svglib`
2. Run `src/final_static_graphs.ipynb` top to bottom (Restart Kernel → Run All). This saves every chart to `figures/` as PNG and SVG.
3. Build the PDF: `uv run python static-viz/make_report.py`
