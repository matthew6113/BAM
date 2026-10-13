import { useEffect, useRef } from 'preact/hooks';
import { DATA_LAST_VERIFIED, MAPPED_PROJECTS, STAGES } from '../projects/data';
import { MapDataCredits } from './Credits';
import { formatDate } from './format';

interface Props {
  onClose: () => void;
}

const STAGE_ORDER = [...STAGES].sort((a, b) => a.order - b.order);

/**
 * The about page: what the map is, how to read it, where the facts come from, and credits.
 * Every claim here describes what the map actually draws (src/map/projectLayers.ts) or comes from
 * the data (counts, stages, dates), so it stays true when those change.
 */
export function AboutPanel({ onClose }: Props) {
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => heading.current?.focus(), []);

  return (
    <aside class="project-panel about-panel" aria-labelledby="about-title">
      <header>
        <h2 id="about-title" ref={heading} tabIndex={-1}>About this map</h2>
        <button type="button" class="close" aria-label="Close about" onClick={onClose}>
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" /></svg>
        </button>
      </header>

      <p class="summary lede">
        An interactive 3D map of the Bay Area's largest development projects, {MAPPED_PROJECTS.length} of
        them so far, by <a href="https://www.matthewhuguet.com/">Matthew Huguet</a>. Click a project, or
        pick one from the Projects list, to fly in and see what it is, where it stands and where each fact
        comes from. The list groups them into buildings and transportation (rail lines and ferry
        terminals).
      </p>

      <section aria-labelledby="about-read">
        <h3 id="about-read">How to read it</h3>
        <p>
          The present is drawn as print, the future in color. Every existing building is a flat footprint
          in quiet ink, raised faintly in 3D where its height is known. Projects are colored by stage, and the more certain a building is, the more solid
          it's drawn.
        </p>
        <ul class="stage-key" aria-label="Stages">
          {STAGE_ORDER.map((s) => (
            <li>
              <i class={s.key === 'proposed' ? 'outline' : undefined}
                style={s.key === 'proposed'
                  ? { borderColor: `var(--stage-${s.key})` }
                  : { background: `var(--stage-${s.key})` }} />
              <span><strong>{s.label}.</strong> {s.meaning}</span>
            </li>
          ))}
        </ul>
        <ul class="notes">
          <li>A proposed site is a dashed outline with no fill; later stages are filled.</li>
          <li>A dotted outline on the water is part of a site that is only dredged, with nothing built on it.</li>
          <li>
            Open a project and its buildings rise in place. A faint envelope above a base shows a
            height limit, not a design.
          </li>
          <li>Plan-scale projects show the plan's land-use zones.</li>
          <li>
            Rail projects are lines: tunnels hollow, shared track lighter, proposed lines dashed. Filled
            dots are new or rebuilt stations, hollow dots existing ones.
          </li>
        </ul>
      </section>

      <section aria-labelledby="about-sources">
        <h3 id="about-sources">Sources and accuracy</h3>
        <p>
          Every fact comes from an official public source: the agencies and public bodies involved, their
          adopted plans, hearing records, permits and GIS. Details only the press or a developer reports
          are held back until an official record confirms them.
        </p>
        <p>
          Shapes that aren't from official GIS say so: “Approximate boundary” where a site is traced from
          planning documents, “Illustrative massing” where buildings are an approximation. Each project
          lists its sources and the date it was last checked, and the map is re-checked about every six
          weeks.
        </p>
      </section>

      <section aria-labelledby="about-photos">
        <h3 id="about-photos">Photos and renderings</h3>
        <p>
          Project photos are openly licensed or public domain, from Wikimedia Commons, and credited in
          each panel. Renderings appear only with permission; until then, each panel links to the
          official pages.
        </p>
      </section>

      <section aria-labelledby="about-credits">
        <h3 id="about-credits">Credits</h3>
        <p class="small"><MapDataCredits /></p>
        <p class="small">
          Type in Libre Franklin and Megaprojects Serif, a subset of Source Serif 4 (both SIL Open Font
          License). Built with MapLibre GL JS, PMTiles, Preact and Vite; tiles made with Tippecanoe.
        </p>
      </section>

      <p class="small updated">Project data last checked {formatDate(DATA_LAST_VERIFIED)}.</p>
    </aside>
  );
}
