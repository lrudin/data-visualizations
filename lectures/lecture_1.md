
### Grammar of Graphics with Altaire

Grammar of Graphics contains theme, coordinates, statistics, facets, geometries, aesthetics, data 

## Types of Data, Strings 

Nominal: "strings" with no order 
    wide range of randomly assigned color

Ordered: grades, rankings
    gradient color makes sense here 

## Types of Data, Quantitatives

Interval: arbitrary zero, dates, location 

Temporal: option specifically for dates and times 

Ratio: zero fixed, physical measurements, counts, amounts 

## Mapping of Variables to Aesthetics

- positions
- length
- angle
- slope
- area
- volume
- density 
- hue
- saturation 
- texture
- connection 
- containment/ grouping
- shape 

## Altair

- Altair is a python visualization library that allows us to work from a grammar of graphics perspective 
- Altair is built on top of Vega-Lite
- Vega-Lite takes JSON and converts them into images 

Altair Example 
``` python 
import pandas as pd
import altair as alt

df = pd.read_csv("cars.csv")
alt.Chart(df).mark_point.encode(
  # shorthand as keyword parameters
  x="Horsepower:Q",
  # or longer form with additional customization
  alt.Y("Miles_per_Gallon:Q"
        ).title("Miles Per Gallon"),
)
```

Use '+' to combine compatible charts (same x and y axis)

First chart goes on first and other one goes on top 

