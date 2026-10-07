import { useEffect, useState } from 'preact/hooks';
import { OVERTURE_RELEASE } from '../map/config';

interface Props {
  /** Collapse once the viewer starts using the map (OSM attribution guidelines allow this). */
  collapse: boolean;
}

export function Credits({ collapse }: Props) {
  const [open, setOpen] = useState(true);

  useEffect(() => {
    const t = window.setTimeout(() => setOpen(false), 5000);
    return () => window.clearTimeout(t);
  }, []);

  useEffect(() => {
    if (collapse) setOpen(false);
  }, [collapse]);

  return (
    <div class={`credits ${open ? 'open' : ''}`}>
      <p id="credits-body" class="credits-body" hidden={!open}>
        Map data <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a> and{' '}
        <a href="https://overturemaps.org">Overture Maps Foundation</a> (release {OVERTURE_RELEASE}, ODbL).
        Building footprints from OpenStreetMap, Microsoft and Esri Community Maps contributors; heights
        from OpenStreetMap and USGS lidar. Project boundaries come from city and county GIS (DataSF;
        Menlo Park; Mountain View; San José, CC-BY; Sunnyvale; Brisbane; Oakland; East Palo Alto; Santa
        Clara, Alameda, San Mateo and Marin counties) or are traced from public planning documents, cited in each project's panel. Project
        photos from Wikimedia Commons contributors, credited with their licenses in each panel.
      </p>
      <button type="button" class="credits-toggle" aria-expanded={open} aria-controls="credits-body"
        onClick={() => setOpen(!open)}>
        {open ? 'Hide credits' : '© OpenStreetMap contributors, Overture Maps · Credits'}
      </button>
    </div>
  );
}
