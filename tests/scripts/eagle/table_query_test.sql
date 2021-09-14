SELECT
    tab.*
FROM
    RecalL0025N0752_SubHalo as gal,
    RecalL0025N0752_Aperture as ape,
    RecalL0025N0752_Magnitudes as tab
WHERE
    gal.SnapNum = 27 and
    ape.Mass_Star > 1.00e+08 and
    ape.ApertureSize = 30 and
    gal.GalaxyID = ape.GalaxyID and
    gal.GalaxyID = tab.GalaxyID
