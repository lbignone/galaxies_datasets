SELECT
    tab.*
FROM
    {simulation:s}_SubHalo as gal,
    {simulation:s}_Aperture as ape,
    {simulation:s}_{table:s} as tab
WHERE
    gal.SnapNum = {snap_number:d} and
    ape.Mass_Star > {min_mass_star:.2e} and
    ape.ApertureSize = 30 and
    gal.GalaxyID = ape.GalaxyID and
    gal.GalaxyID = tab.GalaxyID
