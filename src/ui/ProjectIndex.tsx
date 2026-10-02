import { useState } from 'preact/hooks';
import { MAPPED_PROJECTS, stageLabel } from '../projects/data';

interface Props {
  openId: string | null;
  onOpen: (id: string, opener: HTMLElement) => void;
}

/**
 * The keyboard route into the projects: a short list that opens each one with the fly-in.
 * Milestone 3 grows this into the searchable, filterable index.
 */
export function ProjectIndex({ openId, onOpen }: Props) {
  const [expanded, setExpanded] = useState(false);
  return (
    <nav class="project-index" aria-label="Projects">
      <button type="button" class="index-toggle" aria-expanded={expanded} aria-controls="project-index-list"
        onClick={() => setExpanded((e) => !e)}>
        Projects
        <svg viewBox="0 0 12 12" aria-hidden="true"><path d={expanded ? 'M3 7.5 6 4.5l3 3' : 'M3 4.5 6 7.5l3-3'} /></svg>
      </button>
      <div id="project-index-list" hidden={!expanded}>
        <ul>
          {MAPPED_PROJECTS.map((p) => (
            <li>
              <button type="button" aria-current={p.id === openId ? 'true' : undefined}
                onClick={(e) => onOpen(p.id, e.currentTarget as HTMLElement)}>
                <span class="name">{p.name}</span>
                <span class="stage">
                  <i style={{ background: `var(--stage-${p.stage})` }} />
                  {stageLabel(p.stage)}
                </span>
              </button>
            </li>
          ))}
        </ul>
        <p class="small">More projects are being mapped.</p>
      </div>
    </nav>
  );
}
