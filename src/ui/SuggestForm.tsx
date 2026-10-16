import { useRef, useState } from 'preact/hooks';

/**
 * Where suggestions are sent: Matthew's Google Apps Script receiver (scripts/suggest/), which adds
 * each one to a Sheet and emails him. Set at build time from the repository variable SUGGEST_URL.
 * Without it, the form opens a prefilled GitHub issue instead.
 */
const SUGGEST_URL = (import.meta.env.VITE_SUGGEST_URL as string | undefined) || '';
const ISSUE_URL = 'https://github.com/matthew6113/BAM/issues/new';

const LIMITS = { project: 200, place: 200, link: 500, notes: 2000, email: 200 } as const;
type Field = keyof typeof LIMITS;

export function issueUrl(f: Record<Field, string>): string {
  const body = [
    `**Project:** ${f.project}`,
    `**Where:** ${f.place}`,
    f.link && `**Official link:** ${f.link}`,
    f.notes && `\n${f.notes}`,
  ].filter(Boolean).join('\n');
  return `${ISSUE_URL}?${new URLSearchParams({ title: `Suggest: ${f.project}`, body })}`;
}

/** A short form for suggesting a project to add. It never publishes anything on the map. */
export function SuggestForm() {
  const [status, setStatus] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');
  const shownAt = useRef(Date.now());

  const onSubmit = async (e: Event) => {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const data = new FormData(form);
    const f = Object.fromEntries(
      (Object.keys(LIMITS) as Field[]).map((k) => [k, String(data.get(k) ?? '').trim().slice(0, LIMITS[k])]),
    ) as Record<Field, string>;
    if (!SUGGEST_URL) {
      window.open(issueUrl(f), '_blank', 'noopener');
      return;
    }
    setStatus('sending');
    try {
      // The receiver answers without CORS headers, so the response is opaque: a network error is
      // the only failure the page can see.
      await fetch(SUGGEST_URL, {
        method: 'POST',
        mode: 'no-cors',
        body: new URLSearchParams({
          ...f,
          website: String(data.get('website') ?? ''), // a honeypot: people never see it
          elapsed: String(Date.now() - shownAt.current),
        }),
      });
      form.reset();
      setStatus('sent');
    } catch {
      setStatus('error');
    }
  };

  return (
    <form class="suggest-form" onSubmit={onSubmit}>
      <label>
        <span>Project name</span>
        <input name="project" required maxLength={LIMITS.project} autoComplete="off" />
      </label>
      <label>
        <span>City or location</span>
        <input name="place" required maxLength={LIMITS.place} autoComplete="off" />
      </label>
      <label>
        <span>Official link <em>(optional)</em></span>
        <input name="link" type="url" inputMode="url" maxLength={LIMITS.link} placeholder="https://"
          autoComplete="off" />
      </label>
      <label>
        <span>Anything else <em>(optional)</em></span>
        <textarea name="notes" rows={3} maxLength={LIMITS.notes} />
      </label>
      {SUGGEST_URL && (
        <label>
          <span>Your email <em>(optional, only to reply)</em></span>
          <input name="email" type="email" maxLength={LIMITS.email} autoComplete="email" />
        </label>
      )}
      <div class="honeypot" aria-hidden="true">
        <label>Website <input name="website" tabIndex={-1} autoComplete="off" /></label>
      </div>
      <button type="submit" disabled={status === 'sending'}>
        {status === 'sending' ? 'Sending…' : SUGGEST_URL ? 'Send suggestion' : 'Suggest on GitHub'}
      </button>
      <p class="small" role="status">
        {status === 'sent' && 'Thanks. Matthew will look into it against official sources.'}
        {status === 'error' && 'That didn’t send. Check your connection and try again.'}
        {status === 'idle' && !SUGGEST_URL && 'Opens a prefilled GitHub issue (needs a GitHub account; issues are public).'}
      </p>
    </form>
  );
}
