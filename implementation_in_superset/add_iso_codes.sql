-- ISO 3166-2 codes are needed to create a country map in superset.
-- For more information, see https://apache.github.io/superset/visualization.html.

-- Add column
ALTER TABLE production_sites ADD COLUMN iso_code varchar(10);

-- Add values according to city
UPDATE production_sites
SET iso_code =
    CASE
        WHEN city = 'Husum' THEN 'DE-NI'
        WHEN city = 'Grimma' THEN 'DE-SN'
        WHEN city = 'Barleben' THEN 'DE-ST'
        WHEN city = 'Sömmerda' THEN 'DE-TH'
        WHEN city = 'Eisenberg' THEN 'DE-TH'
        WHEN city = 'Kolkwitz' THEN 'DE-BB'
    END
WHERE city IN ('Husum','Grimma','Barleben','Sömmerda','Eisenberg','Kolkwitz');