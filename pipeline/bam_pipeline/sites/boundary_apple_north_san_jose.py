"""Apple North San José campus: the development agreement's property as the County's six parcels.

The City of San José's memorandum for City Council file 26-1159 (Nov 5, 2026; DA26-001 and ER26-132, the
First Amendment to the Amended and Restated Development Agreement with Apple Inc.), with the Planning
Commission staff report of Oct 28, 2026 attached, names the property: "APNs 101-03-004, 007, 008;
101-02-011, -016, -017", "86.35 gross acres", four development sites west of Orchard Parkway on both
sides of Orchard Place (formerly Atmel Way) and east of Orchard Parkway on both sides of Component Drive.
The boundary is the union of those six parcels in the Santa Clara County parcel layer (data.sccgov.org
ubcd-cewv). Orchard Parkway and Orchard Place, which the City has conditionally vacated, are public
streets today and are not drawn.

The First Amendment takes an approximately 9.7-acre parcel on North First Street (to be conveyed to PG&E)
out of the agreement once the conveyance is recorded. It is still part of APN 101-02-011 in the County's
layer and is drawn inside the site; cut it out when the County maps the new parcel.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_apple_north_san_jose
"""

from __future__ import annotations

from . import official_boundaries as ob

PROJECT = "apple-north-san-jose"
APNS = ["10103004", "10103007", "10103008", "10102011", "10102016", "10102017"]  # staff report, p. 2
MEMO = "https://legistar.granicus.com/sanjose/attachments/33a546b0-cfda-4031-8f27-5211a4e444f3.pdf"

SPEC = {
    "label": "Santa Clara County parcels",
    **ob.socrata(*ob.SCC_PARCELS, f"apn in ({ob._sql_list(APNS)})"),
    "layer": ("Santa Clara County parcels (data.sccgov.org ubcd-cewv): APNs 101-03-004, -007 and -008 and "
              "101-02-011, -016 and -017, the six parcels the City of San José's memorandum and Planning "
              "Commission staff report for the First Amendment to the Apple development agreement name "
              "(City Council file 26-1159, DA26-001, Nov 10, 2026)"),
    "accuracy": "official",
    "note": ("The six parcels the City names as the property under the 2016 Amended and Restated Development "
             "Agreement with Apple Inc. (\"86.35 gross acres\"; four sites of about 43, 16.4, 15.1 and 11.1 "
             "acres), as Santa Clara County maps them. It includes the approximately 9.7-acre parcel on North "
             "First Street at Component Drive that the First Amendment removes from the agreement once Apple "
             "conveys it to PG&E; that parcel is still part of APN 101-02-011 in the County's layer, so it "
             "can't be cut out yet. Orchard Parkway and Orchard Place (formerly Atmel Way), conditionally "
             "vacated but still open public streets, are not drawn. Against the City's 86.35 gross acres:"),
    "license": "Santa Clara County open data (terms of use)",
}


def main() -> None:
    ob.SPECS[PROJECT] = SPEC
    ob.build(PROJECT)


if __name__ == "__main__":
    main()
