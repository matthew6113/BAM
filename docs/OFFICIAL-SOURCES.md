# Official-source research: where it stands

Matthew's rule (2026-10-02): only official sources (see CLAUDE.md). This note hands the
research to the next session. Start with a network check:

```sh
for h in sfplanning.org data.sfgov.org codelibrary.amlegal.com ceqanet.lci.ca.gov; do
  printf "%-26s " $h; curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://$h/; done
```

If these still fail, the environment's network access hasn't been broadened. Matthew
changes it in the cloud environment settings.

## Reachable even without broader access

SF Planning keeps its files in an S3 bucket that has been reachable all along. The
subdomain becomes a folder:

- `sfmea.sfplanning.org/<file>` → `https://sfplanning.s3.amazonaws.com/sfmea/<file>`
- `commissions.sfplanning.org/cpcpackets/<file>` → `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/<file>`
- Old site files are under `default/files/...`.

The bucket can't be listed, so you need exact filenames. A missing key returns 403.
Planning Commission minutes follow `cpcpackets/YYYYMMDD_cal_min.pdf` up to about 2022.
Later minutes aren't in the bucket.

## Potrero Power Station: leads

| Need | Official source | Notes |
|---|---|---|
| Approved block heights | Design for Development, approved by Planning Commission Motion 20638 (Jan 30, 2020) | Linked from sfplanning.org/potrero-power-station. Also on file with the Board of Supervisors, File No. 200040. Minutes: new buildings 65 to 240 ft, height district 65/240-PPS on map HT08. |
| Official boundary | Special Use District and zoning layers (data.sfgov.org); parcels 4175/002, 4175/017, 4175/018 (part), 4232/001, 4232/006, plus non-assessed Port and City land | Would replace the traced boundary ("approximate") with official geometry. |
| Affordable share (press: 30%) | Development Agreement (Board ordinance, 2020) | sfplanning.org hosts a DA terms PDF. |
| Construction status | DBI permits; UC Regents approval of the Block 2 building (Sept 2024 meeting, `regents.universityofcalifornia.edu/regmeet/sept24/f5attach6.pdf`); MOHCD (Mayor's Office of Housing) for the Sophie Maxwell Building | Needed before the stage returns to "partly built". |
| 2025–26 amendments | Addendum 2 to the EIR (CEQAnet SCH 2017112005, received 7/29/2026); Planning Commission recommendation; Board of Supervisors action | Search summaries say heights rise (65 to 180 ft, 300 ft on Block 6). Read the official text and check whether the Board adopted them. |

The press-only facts waiting for confirmation are in the project's `reported` record in
`data/projects.json`, and the open items are in its `verify` list.

## The other 24 projects

None are on the map yet; Milestone 3 adds them. For each one:
- Find the official boundary. Prefer GIS (a plan area, Special Use District or parcels) over tracing a figure.
- Confirm each fact in `projects.json` against an agency source.
- Move press-only facts into `reported`.
- `src/projects/official.ts` lists the accepted hosts, and its test enforces the rule once a project is mapped.
