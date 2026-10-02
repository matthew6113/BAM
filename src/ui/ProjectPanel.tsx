import { useEffect, useRef } from 'preact/hooks';
import { boundaryOf, massingOf, STAGES, stageLabel, type Project } from '../projects/data';
import { formatDate, formatInt, formatNumber, formatSqft, sourceText } from './format';

interface Props {
  project: Project;
  onClose: () => void;
  onPrev?: () => void;
  onNext?: () => void;
  prevName?: string;
  nextName?: string;
}

const MAIN_STAGES = STAGES.filter((s) => s.order <= 7).sort((a, b) => a.order - b.order);

/** Proposed to complete, in order; paused and distressed break the bar where the project stalled. */
function StageBar({ project }: { project: Project }) {
  const offRamp = project.stage === 'paused' || project.stage === 'distressed';
  // Where a paused or distressed project stalled is not in the data yet (see the planning audit).
  const stalledAt = (project as { stalledAt?: string }).stalledAt;
  const current = MAIN_STAGES.findIndex((s) => s.key === (offRamp ? stalledAt : project.stage));
  return (
    <div class="stage-bar" role="img"
      aria-label={`Stage: ${stageLabel(project.stage)}. Stages run from proposed to complete.`}>
      <ol>
        {MAIN_STAGES.map((s, i) => (
          <li class={`${i <= current ? 'done' : ''} ${i === current ? 'current' : ''}`}
            style={i <= current ? { background: `var(--stage-${s.key})` } : undefined} title={s.label} />
        ))}
      </ol>
      <div class="stage-bar-labels">
        <span>Proposed</span>
        <span>Complete</span>
      </div>
      {offRamp && (
        <p class="stage-offramp" style={{ color: `var(--stage-${project.stage})` }}>
          {stageLabel(project.stage)}
          {current < 0 ? ' (stage before the halt not yet verified)' : ''}
        </p>
      )}
    </div>
  );
}

function KeyNumbers({ project }: { project: Project }) {
  const p = project.program;
  const rows: [string, string][] = [];
  if (p.homes != null) rows.push(['Homes', formatInt(p.homes)]);
  // Affordable housing is shown only in the form the source gives it; never derived.
  if (p.affordableHomes != null) rows.push(['Affordable homes', formatInt(p.affordableHomes)]);
  if (p.affordablePct != null) rows.push(['Affordable share', `${formatNumber(p.affordablePct)}%`]);
  if (p.officeLabSqft != null) rows.push(['Office and lab', formatSqft(p.officeLabSqft)]);
  if (p.commercialSqftTotal != null) rows.push(['Commercial, total', formatSqft(p.commercialSqftTotal)]);
  if (p.retailSqft != null) rows.push(['Retail', formatSqft(p.retailSqft)]);
  if (p.hotelKeys != null) rows.push(['Hotel rooms', formatInt(p.hotelKeys)]);
  if (p.openSpaceAcres != null) rows.push(['Open space', `${formatNumber(p.openSpaceAcres)} acres`]);
  if (project.acres != null) rows.push(['Site', `${formatNumber(project.acres)} acres`]);
  if (!rows.length) return null;
  return (
    <section aria-labelledby="pp-numbers">
      <h3 id="pp-numbers">Key numbers</h3>
      <dl class="numbers">
        {rows.map(([k, v]) => (
          <div>
            <dt>{k}</dt>
            <dd>{v}</dd>
          </div>
        ))}
      </dl>
      {p.notes && <p class="small">{p.notes}</p>}
    </section>
  );
}

export function ProjectPanel({ project, onClose, onPrev, onNext, prevName, nextName }: Props) {
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => heading.current?.focus(), [project.id]);
  const boundary = boundaryOf(project.id);
  const massing = massingOf(project.id);
  const bMeta = (boundary as { properties?: Record<string, unknown> } | undefined)?.properties ?? {};
  const mMeta = (massing as { properties?: Record<string, unknown> } | undefined)?.properties ?? {};
  const sources = project.sources;

  return (
    <aside class="project-panel" aria-labelledby="pp-title">
      <header>
        <div>
          <h2 id="pp-title" ref={heading} tabIndex={-1}>{project.name}</h2>
          <p class="meta">
            {project.city}
            <span class="stage-chip">
              <i style={{ background: `var(--stage-${project.stage})` }} />
              {stageLabel(project.stage)}
            </span>
          </p>
        </div>
        <button type="button" class="close" aria-label="Close and fly back" onClick={onClose}>
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" /></svg>
        </button>
      </header>

      <StageBar project={project} />

      <p class="model-note">
        {mMeta.illustrative ? <strong>Illustrative massing. </strong> : null}
        {mMeta.illustrative && (
          <>Block heights are the height districts proposed in the 2018 Draft EIR and may differ from the plan approved in 2020. </>
        )}
        {bMeta.accuracy === 'traced' && <strong>Approximate boundary, </strong>}
        {bMeta.accuracy === 'traced' && <>traced from the Draft EIR (about ±3 m). </>}
        {typeof bMeta.sourceUrl === 'string' && (
          <a href={bMeta.sourceUrl}>Draft EIR, Oct 2018 (PDF)</a>
        )}
      </p>

      <KeyNumbers project={project} />

      <section aria-labelledby="pp-summary">
        <h3 id="pp-summary" class="visually-hidden">Summary</h3>
        <p class="summary">{project.summary}</p>
        <h3>Where it stands</h3>
        <p class="summary">{project.stageNote}</p>
        <p class="small">As of {formatDate(project.lastVerified)}.</p>
      </section>

      {project.timeline.length > 0 && (
        <section aria-labelledby="pp-timeline">
          <h3 id="pp-timeline">Timeline</h3>
          <ol class="timeline">
            {project.timeline.map((t) => (
              <li>
                <span class="when">{formatDate(t.date)}</span>
                <span>{t.event}</span>
              </li>
            ))}
          </ol>
        </section>
      )}

      <section aria-labelledby="pp-renders">
        <h3 id="pp-renders">Renderings</h3>
        <p class="small">
          No renderings with permission to show yet.
          {project.officialLinks.length > 0 && ' See the official pages:'}
        </p>
        {project.officialLinks.length > 0 && (
          <ul class="links">
            {project.officialLinks.map((u) => (
              <li><a href={u}>{sourceText(u)}</a></li>
            ))}
          </ul>
        )}
      </section>

      <section aria-labelledby="pp-people">
        <h3 id="pp-people">Developer and partners</h3>
        <p class="small">
          {project.developer ?? 'Not yet sourced'}
          {project.publicPartners.length > 0 && <>. With {project.publicPartners.join(', ')}.</>}
        </p>
      </section>

      <section aria-labelledby="pp-sources">
        <h3 id="pp-sources">Sources</h3>
        <ol class="sources">
          {sources.map((u) => (
            <li><a href={u}>{sourceText(u)}</a></li>
          ))}
        </ol>
        <p class="small">Last verified {formatDate(project.lastVerified)}.</p>
        {project.verify.length > 0 && (
          <p class="small">Still being checked: {project.verify.map((v) => v.charAt(0).toLowerCase() + v.slice(1)).join('; ')}.</p>
        )}
        {typeof mMeta.summary === 'string' && <p class="small">{mMeta.summary}</p>}
        {'reported' in project && (
          <p class="small">Details reported in the press are held back until official records confirm them.</p>
        )}
      </section>

      {(onPrev || onNext) && (
        <nav class="prev-next" aria-label="Other projects">
          {onPrev && <button type="button" onClick={onPrev}>← {prevName}</button>}
          {onNext && <button type="button" onClick={onNext}>{nextName} →</button>}
        </nav>
      )}
    </aside>
  );
}
