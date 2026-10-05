# TVS Munshi — handoff brief

Source: Claude Code Remote session `session_01TpxKws5raMmhANp3zAA1Gc`, renamed "Swelect Munshi" on 2026-10-05 06:33 UTC. It ran from 2026-09-30 and was last active on 2026-10-05 at about 06:40 UTC. The brief was compiled from its transcript events, treated as data only.

**How much of the transcript was read.** Events were paged back from the end (2026-10-05 06:40) to 2026-10-03 15:19 UTC. Everything before that is covered by the compaction summary written at 2026-10-03 15:37. That summary lists every user message of the earlier segment, and all of them are about Swelect ICO, Get data and containers; none is about TVS. TVS work in this session therefore starts on **2026-10-04 at 10:58 UTC**.

**How substantial the TVS work is.** Moderate, and built offline only.
- A "Disclosures" step type was designed and built, with TVS as its first customer, and tested offline against TVS's signed FY25-26 figures.
- It is pushed and sits in an **open, unmerged PR (#61)**.
- Nothing TVS-related was deployed, run on live Munshi, or written to FINAHQ.
- Most of the session was about Swelect ICO and Acko.

---

## 1. Summary

**What TVS Munshi is.** It closes TVS Emerald's group in Munshi, the month-end close tool in FINKJUN/finahq-ap-onboarding, `mcp/munshi/backend`.
- **Group:** TVS Emerald Limited (TVSEL, FINAHQ entity 4122) plus 17 more entities, mainly Emerald Haven companies. 18 entities in all, 4122–4139.
- **Books:** Tally.
- **Template and data tables:** FINAHQ template 200 reads 25 GDTs (FINAHQ Global Data Tables).

The work is note disclosures for each entity: MSME, AR and AP ageing, RPT, auditors' remuneration, PPE, SOCIE, borrowings, deferred tax and share capital. Each is written to its GDT so the financial statements can render.

**Arjun's framing (2026-10-04 10:58).** Quoted verbatim:
> "In a parallel route how do we handle TVS --- 18 companies essentially all note disclosures like MSME-- AR agening--- AP agening--- RPT--- Audit fee disclosures are container information which has to be added entity wise--- then the Financials can run. Similar to ICO do we want to standardise and the end outpt is essentially write to GDT"

**Status as last seen**

| Item | State |
|---|---|
| Disclosures step type | Built on branch `claude/cool-bardeen-57cea6-tvs` (worktree `/home/user/wt-tvs`) |
| PR #61, "Disclosures step type (TVS first): company × disclosure grid, recon with the TB, Update GDT" | Opened 2026-10-04 13:24 UTC; **never merged** in the transcript. PRs #62–#73 (except #61) were merged after it, so it is probably behind main now. |
| Tests | Full suite 289 tests, 0 failing (with main, 2026-10-04); py311 guard ok |
| Offline comparison with TVS's signed FY25-26 figures | 7 disclosures match, 5 differ; deferred tax and the 14 form tables can't be computed from the ledger (see §2) |
| Arjun's answers (PPE, RPT gross/net) | Recorded in `STANDARDISATION_LAYER.md` on the TVS branch (2026-10-04 15:00) |
| Still open | GDT references for EPS diluted shares, SOCIE round-off and MSMED s22; terms for the HDFC Benz loan |
| Live TVS tenant (186, "Emerald Haven Development Limited") | Shown as **empty** when an Acko agent opened it read-only on 2026-10-05 |

---

## 2. TVS-specific work done so far

### 2026-10-04 10:58 — design study (read-only agent "TVS disclosures design study", id a19e5d5a41574065f)

**TVS's set-up before this session.** All paths are under `mcp/`.

- **SOP:** `tools/munshi_tvs_sop.py` (STEPS, 34 rows), converted through `tools/sop_v17.py` into `munshi/backend/structure2.py` (VERSION = 17).
  - Test: `tests/test_munshi_tvs_full_financials.py`.
  - Workbooks: `tools/inputs/tvs/` (v1.0 to v3.7). The scratchpad copy `tvs_v36_new.xlsx` is v3.7.
  - One SOP serves all 18 entities, one project each. The test asserts that no row names an entity.
- **The 18 entities**, 4122–4139, from `finahq_mcp/data/gdt_crosswalk_v1.json` (around line 520):
  - 4122 TVSEL (TVS Emerald Limited);
  - EHLSRRL, EHPDL, EHMSPL, EHBPL, EHTCPL, EHRDPPL, EHTL, HHPDPL, EHLS2PL, EHLS3PL, EHPPL, EHGCPL, EHHRPL, EHHDPL, EHDL, EHRPL;
  - EHHPL, an associate.
- **Only entity 4122 has been worked live.** The 18-entity design exists only on paper: `munshi/docs/group-of-entities.md` and `backend/entity_group.py`.
- **Steps in the old SOP:**
  - Ledger: 1, 1a, 1b, 1c (pull and prove the Tally TB, current and comparative); 2 (period); 3 (mapping check).
  - Computed `add` steps, each writing one GDT: 4 PPE, 4a ROU, 4b RPT lines, 4c ageing, 4d inventory, 4e Ind AS 115, 4f ratio inputs, 4g auditors, 4h share capital, 4i FRM maturities, 4j/4k SOCIE.
  - Loaded by the controller: 5 employee benefits, 5a deferred tax, 5b borrowings terms, 5c registers, 5d contingent liabilities, 5e related-parties list, 5f ratio reasons.
  - Then: 6 RPT reconcile, 6a confirm rules, 7 render, 7a–7d prove the statements, 7e file, 8 sign-off.
- **Disclosure measure workbook:** `tools/inputs/tvs/TVSEL_4122_Munshi_Tally_Disclosure_Measure_FY25-26_2026-09-15.xlsx`. It covers 610 standalone cells:

  | Cells | Status |
  |---|---|
  | 173 | computed and tie |
  | 25 | regrouped |
  | 71 | no rule yet |
  | 8 | mismatches |
  | 333 | not in Tally at all |

- **GDT references named in the transcript:**
  - Ageing: `a49bccfdb7`. Its MSME rows A15–A21 were never filled.
  - Auditors: `4b6eccf3a1`.
  - RPT Lines (a list table): `8416dc18f4`.
  - Related-parties list (step 5e): `301be69183`.
  - Other related parties in the crosswalk: `8976047493`.
- **TVS chart L4s** (the COAVERSION column, `tests/dress/tvs_186/coa.xlsx`):
  - 41512 = "Dues to micro and small enterprises";
  - 41513 = "Dues to enterprises other than micro and small enterprises";
  - 41550 = "Payments to auditors".
- **Problems found in the old build:**
  - `master_ageing.fill` and `master_rpt.fill` wrote through `_populate` without tying first or reading back.
  - MSME was never filled, and there was no MSMED s22 table.
  - Tally's bill-wise references stop in 2021, so ageing is FIFO on the day book.
  - RPT rows were learnt from last period's table, so a new party never appears by itself.
- **Related parties** (from crosswalk `8976047493`):
  - holding and promoter group: TVS Holdings, TVS Motor, TVS Credit Services;
  - KMP;
  - JV partners: CP Senior Housing, Bayswater, Rocaf;
  - EHHPL, the associate.
- **Tally cache:** `tools/tally/cache/TVS_Emerald_Limited`, with FY24/25 and FY25/26 vouchers, the TB, ledgers and groups. In the Tally TB a debit is negative; the schema is debit positive.

### 2026-10-04 11:11–11:21 — Arjun's decisions, and the mock-up

- All decisions are in §5.
- Mock-up: `scratchpad/disclosures_mock.html`, published as https://claude.ai/artifact/T1BpnCkdAqCdCRnSs4Zuda. Its figures are made up.
  - Tabs: Grid · Disclosure detail · Borrowings register · Masters · Settings.

### 2026-10-04 11:43 — Arjun: "go ahead … 3) TVS build in parallel"

- Build agent "Build TVS Disclosures step" (id a72878c810f03a36f), started from `origin/claude/cool-bardeen-57cea6-acko`.
- Branch `claude/cool-bardeen-57cea6-tvs`, worktree `/home/user/wt-tvs`.
- Brief constraints: offline from repository data only; no writes to live FINAHQ; no PR or merge by the agent.

### 2026-10-04 12:52 — build report

**New modules in `mcp/munshi/backend/`**

| Module | What it does |
|---|---|
| `master_disclosures.py` | The `det:disclosures` runbook. It opens lines (plus the prior year), adds fields, syncs the group and borrowings, reads the TB, measures what is on file, evaluates, writes approved plans and keeps the run. |
| `disc_page.py` | The page tabs, the lists (reusing the ICO list component), Update GDT, Approve, and the uploads (defs, msme, deferred_tax, far, shares, borrowings). |
| `disc_fields.py` | Derived fields: ageing bucket (Schedule III BUCKET_SETS, FIFO or bill-wise), AP class, `dr_cr_side`, counter-leg class, `spread_in_document`. |
| `disc_defs.py` | Tenant setting `disclosure_defs`, versioned. ENGINES: ageing_ar, ageing_ap, msme, rpt, related_parties, auditors, ppe, socie, borrowings, deferred_tax (person), share_capital, tb_figures, form (person). Also the SETTINGS. |
| `disc_masters.py` | Collection `disc_masters`: related parties (doc "related"), `msme__{company}`, `borrowings__{company}`, `shares__{company}`, schedules (deferred tax, FAR), person-entered entries. |
| `disc_engine.py` | The engines and ties, `was_becomes` and `blocks_publish`. |
| `disc_write.py` | Tie first, then Approve, write and read back. Keyed tables merge; list tables replace the whole period, only after Approve. |

**Edited files**
- `ledger_store.py` and `ledger_schema.py`: Tally's MSME and related-party flags are no longer dropped. Also adds a `contains` condition and a bracket-aware `_conditions` splitter.
- `structure2.py`: `MASTERS["disclosures"]`; nine master steps.
- Also: `packs/__init__.py`, `deterministic.py`, `generic_close.py`, `step_tabs.py`, `console.py` (routes `/m/{mission_id}/step/{step_id}/disc/{what}`).
- `master_ageing.py` and `master_rpt.py` now write through `disc_write.write_tied`.
- `.claude/skills/munshi-sop-author/SKILL.md` was regenerated.

**TVS tooling and tests**
- `mcp/tools/munshi_tvs_disclosures.py`: definitions for all 25 GDTs, plus the revised SOP (a Get data row 1d, then one Disclosures row 4).
- `mcp/tools/tvs_disclosures_offline.py`: the offline comparison.
- `mcp/tests/test_munshi_disclosures.py`: 108 checks, using `tests/disc_fixture.py`.
- `mcp/tests/test_munshi_tvs_disclosures.py`.

**Deliverables**, in the old session's scratchpad `/tmp/claude-0/-home-user-finkai-site/d04332ac-076f-5c1d-b679-1cd1bd0855ca/scratchpad/`. They may not exist in a new container.
- `fresh/TVS SOP - disclosures.xlsx`: zero problems on upload.
- `fresh/TVS disclosures vs signed.xlsx`: sheets Summary, Cells, RPT rows, Recon, What was entered.
- `tvs_shots/`: 14 PNGs. 01–08 show TVS's own figures; 09–13 the fixture; 14 the grid at phone width.

**Offline results against TVS's signed FY25-26 book**

| Disclosure | Result |
|---|---|
| MSME | matches (1 cell) |
| Share capital | matches (8) |
| Shareholders over 5% and promoters | matches (4) |
| Borrowings | matches (42); 1 GL still needs terms |
| Auditors' remuneration | matches (4) |
| Related parties | matches (30) |
| Ageing doubtful/disputed rows | matches (9) |
| AR ageing | 3 match, 2 differ, 2 not computable. lt6m 164,809,798 vs 164,911,000; total 211,719,619 vs 211,814,000 (signed 211,821,000). ₹5.6m is older than the day book, so 2–3y and >3y can't be computed. |
| AP ageing | 8 match, 4 differ. Unbilled 193,809,289 vs 193,798,000; not due 99,599,453 vs 100,167,000; lt1y 78,293,781 vs 80,116,000; total 393,704,488 vs 395,945,000 |
| PPE roll-forward | 37 match, 23 differ (opening class regroups) |
| SOCIE | differs. PAT −154,286,752 vs signed −68,390,000; OCI 0 vs −6,452,000. The Tally TB used in place of FINAHQ's lacks the inventory change and the unmapped GLs. |
| RPT | 39 match, 37 differ, 58 not computable. Balances mostly match; gross loan flows differ from TVS's netting. |
| Deferred tax and all form tables | not computable: entered by a person |

### 2026-10-04 12:52–13:24 — merge and PR

- TVS was merged with Acko and main in `/home/user/wt-tvs`. Suite: 289 tests, 0 failing.
- PR [FINKJUN/finahq-ap-onboarding#61](https://github.com/FINKJUN/finahq-ap-onboarding/pull/61) was opened, with release held until the Swelect March run finished. It was **not merged** in the remainder of the transcript.

### 2026-10-04 14:56–15:00 — Arjun answers two TVS questions

Both answers are recorded in the spec on the TVS branch.
- **PPE:** "PPE- stick to the data in the ledger -- no reclass". Classes stay as booked, with no regroup.
- **RPT gross vs net:** quoted verbatim.
  > "measure what is needed and mark gross against BS transactions which need gross"
  > "Munshi will determine which related-party balance-sheet lines need gross flows versus net--- it can be a setting … that way its fully configurable … we can add gross transactions also as debits in ledger -- call it X , credits in ledger call it Y and add to RPT as simple as that"

  As recorded: gross or net is a setting per balance-sheet line. Gross = ledger debits (X) and credits (Y); net = X − Y. Munshi suggests which lines need gross. This is configuration on container value columns, not new code.

### 2026-10-05 — TVS login touched by mistake (Acko agent)

- `corp_controller_emerald@finahq.com` is the **TVS tenant's login**. The earlier session's goal (Arjun, 22 Sep) was "build the TVS SOP on Tally's XML".
- The orchestrator wrongly guessed that Acko's data might be there. The Acko agent opened only the home and Labels pages: **tenant 186, "Emerald Haven Development Limited", empty**. It changed nothing.
- Arjun (01:42): "corp_controller_emerald@finahq.com--- how is this even possible its a major security risk???"
- The orchestrator called it its own mistake, not a Munshi security hole, and offered a read-only check that each login sees only its own tenant. No record shows that check was run.

### Other TVS references in code
- Tests use `TVS_COLS = ["last_year_end", "this_period"]` and a "TVS rehearsal" in `test_munshi_reconcile`. The Acko step-9 change briefly broke that rehearsal; it was fixed by falling back to waiting for the file.
- A code comment: tenant 183 (Acko) has balance-sheet labels, and tenant 186 (TVS) has none.
- A test fixture comment: the chart was read off tenant 186 / entity 4122 on 2026-09-23.

---

## 3. Open items and pending decisions

**What the session was waiting on at the end. This is not TVS-related.**
- The last assistant message (2026-10-05 06:33) ends: "The long-form Acko container (Group › Sub-group › Label › GL, filtered by Group) is waiting for your go-ahead."
- That is **Acko**: one long-form TB container to replace CT-001 to CT-004, filtered by Group.
- The final user message (06:40), "where are we on swelect now explain", was mid-answer when the transcript ends.
  - Latest Swelect March figures in a tool result: "pairs 99 · within 3,000 of customer 51 · customer total 7,248,786,651.58 · Munshi total 8,415,393,923.82".
  - The Munshi page returned ERR_EMPTY_RESPONSE at that moment.

**TVS-specific open items** (last listed 2026-10-04 14:36 and 12:56):
1. **GDT references** for EPS diluted shares, the SOCIE round-off and the MSMED s22 disclosure. Neither the repo nor the session has them.
2. **Terms for one borrowing GL:** "HDFC Loan - Benz (TN 07 CV 9606)".
3. **FINAHQ TB instead of the Tally stand-in.** The offline run used the Tally TB. A live read of FINAHQ's TB should close most of the SOCIE gap and part of the ageing gap.
4. **PR #61 is unmerged.** Rebase or merge onto current main (PRs #62–#73 have landed since), re-run the suite, then release. The original plan was to release it after the Swelect March run.
5. **Live tenant 186 is empty**: no project. Nothing has been set up on live for the new Disclosures structure.
6. **Not built:** the full 18-entity group mechanics (only 4122 has been worked) and a live run.
7. **Settled by Arjun:** whether to fix the old ageing and RPT write paths now. The build answered it by routing both through `disc_write`; this was the brief's "Fix now" item.
8. **Possibly unresolved:** publishing rules and list-table replace were put to Arjun as questions at 11:21. The 11:43 build brief lists both as Arjun's decisions, but no explicit "agreed" reply to them appears in the transcript.

---

## 4. Shared Munshi architecture and rules that apply to TVS

**Spec.** `mcp/munshi/STANDARDISATION_LAYER.md` in FINKJUN/finahq-ap-onboarding is the agreed spec. Every agent reads it before building.

**The five-line structure** (agreed 2026-10-04 07:05):
1. **Sources:** TB (always on), plus AR/AP and ledger (GL lines) when the admin turns them on, mapped to the standard schema.
2. **Master link:** the GL code. It is a mandatory schema field; a missing GL code, or one not in the chart, is a data exception. Every line gets FINAHQ's L1–L4 through it.
3. **Container:** a pivot of one source.
   - Rows are nature fields, each with a saved tick list (`include`). Values are amount fields or formulas such as AMT1 − AMT2.
   - There is no Filters box. A use narrows the ticks and never widens them. Company is always filterable.
4. **Step:** picks a container, its rows and an amount column.
5. **Write-back** to FINAHQ is optional and happens only after Approve.

As recorded: "TVS: schedules are containers by L4 or GL"; a TVS schedule is "a filter on L4".

**Step types**
- **Normal steps:** the SOP row's attributes, plus containers and filters when the source is TB, GL or AR/AP.
- **ICO:** a fixed page with Pairs · Report · Margins · Settings, and a four-cell SOP row.
- **Disclosures** (TVS): a fixed page and a one-row SOP. Any other cell in the row is refused with "set on the Disclosures page".

**Shared components the Disclosures page reuses from ICO**
- the data bar (what data came through and when, versions);
- Generate (new data never re-runs the step by itself);
- Ready to run (lists blockers, never blocks);
- the list toolbar: search, filter, group-by, bulk Approve, Excel.

**GDT write path**
- FINAHQ Global Data Table, `/api/v1/global-data-tables`. Values are stored per entity per date range. Column A holds the rowUID key; value columns must be number-typed.
- `populate_gdt` merges by default, with read-back and a "MERGE LOST" check. `replace=True` overwrites the whole period.
- Munshi's chain: `master_add.run` → `runbook_kit._populate` → `_overwrite_guard`, then the rulebook (`unreconciled_write`, `overwrite_data`, `data_write` approval), then `_check_written` reads back.
- Munshi never deletes.

**Rules from Acko and Swelect that carry over to TVS**
- **Each month is about itself.** The comparative is FINAHQ's data, picked at download.
  - Arjun (2026-10-05 04:42): "if user wants to use Aug 25 as comparitive ask him to close that period first and get to goal step and then start Aug 26 --- else he can do aug 26 and then do aug 25 as independent steps lets not overcomplicate".
  - Released in PR #70: "Labels chosen by the SOP; period chosen at download (step 2 writes nothing); comparative not Munshi's process; step 9 measures posted journals with no file".
- **Closed periods:** no write to FINAHQ. Munshi measures what is there and says "already there" (Arjun, 2026-10-05 02:30).
- **Fixes from the Acko work** (PR #67 and later):
  - the TB container reads its own month;
  - write steps measure FINAHQ first and show was → becomes.
- **Labels are per company:** a label group comes in only with GL-level bindings for the SOP's entity (PR #68). Relevant if TVS uses labels; a code comment says tenant 186 has no balance-sheet labels.
- **ERP identification** (Swelect): SAP is identified by customer/vendor code; Tally and manual loads by GL or ledger.
  - For Tally (TVS), the counterparty is the party ledger plus bill-wise references, and the AI searches narrations and voucher references.
- **Matching order:** deterministic rules first (Splink reference + amount + date, then amount + date; OR-Tools for sums), then AI only on residuals.
  - The AI's role comes from the master step, as a skill. Every proposal goes to the user-decisions bucket; no new structures.
- **ICO ↔ RPT:**
  - Journals and RPT are at L4.
  - Kind comes from L1: BS on one side and P&L on the other is hybrid. L2 then splits it: non-current is hybrid capital, current is hybrid stock.
  - RPT reuses the ICO container and the ICO pairs' codes for group companies.
- **Release flow** (from the summaries):
  1. Branch, then a PR via `mcp__github__create_pull_request`, then merge via `mcp__github__merge_pull_request`.
  2. `bash /home/user/wt-int/mcp/tools/live/waitrev.sh <oldrev>`.
  3. Full suite: `bash mcp/tools/live/suite.sh <worktree> <outdir>`, which must say "fail 0".
  4. `python mcp/tools/py311_guard.py`.
  5. Commit with `git add <paths>`, never `-a`.
- **Last live revision named:** finahq-ap-onboarding-01080-s8x (sop_schema 18, started 2026-10-05 06:08). Earlier: 01077-kc8.
- **Live site:** https://munshi.finahq.net. Login helper: `scratchpad/lv2.py` (`p,b,ctx,pg,T = lv2.start(w,h)`), with env MUNSHI_USER and MUNSHI_PASS_SESSION. Be gentle with the site: one login per script, back off on 429.

**FINAHQ MCP non-negotiables** (server instructions)
- Never fabricate a figure.
- Never create, change or delete a FINAHQ record without the customer's explicit OK.
- Reconcile or refuse.
- The source is the truth.
- No accounting judgment: replicate and flag.

Note: the FINAHQV15 connector "needs authorising in your claude.ai connector settings" (2026-10-04).

---

## 5. Arjun's standing decisions and preferences

**TVS / Disclosures** (2026-10-04, verbatim where quoted)
- "Similar to ICO do we want to standardise and the end outpt is essentially write to GDT" → Disclosures is a fixed step type like ICO.
- "related party › L4 … its an extension of the ICO conainer add another container considering non ICO parties that all."
- **MSME:** "it will be a one time identification against the vendor master of AP payable ledger --- to identify MSME and we store and carry that forward. It can be an attribute of the AP-AR data"
- **Ageing basis:** "AR-AP ageing --- can also be a config to say whether bill wise or FIFO"
- **Page shape:** "each disclosure step will have a UI like ICO which shold essentially say company-- disclosure-- recon with base data -- update to GDT once update is done click and its updated. Also link to existimg master attributes like measure existing GDT data to that we dont keep wasting time."
- **FA:** "add a FAR schema to update the PPE roll forward based on FAR loaded - or integrated or use GL data to rollforward FAR movement alone … if there is no FAR master config selected then FA becomes a roll forward, if FA master config is selected FAR becomes a read from FAR and fill step-- (so 2 master steps)"
- **RPT:** "RPT extends ICO … Logic remains same just that there is no recon"
- **Borrowings:** "Borrowing register is correct approach we need to remember to identiffy ICO borrowings which should be excluded on consol and Non ICO borrowings … this will only work if 1 GL code = 1 borrowing and then we can map the terms once and then rollforward based on GL data"
- **Unregistered borrowing GLs:** "In case of borrowing L3-L4 there are no GL codes mapped they should be added to the borrowing register and user should be asked to fill it before he comes"
- **Deferred tax:** "For now let deferred tax be a schedule user uploads and we can fill the GDT lets not complicate."
- **Share capital:** "Share capital and share related disclosures should also be a schema-- where if the opening balance = closing balance then the user should not be asked any questions and we should carry forward the data in the GDT with user confirmation"
  - As refined in the session: a share register, with the tie number × FV = TB share capital. When the GL moves, ask only for the register change. Each period, ask one yes/no about transfers among holders over 5% or promoters.
- **SOCIE:** "SOCIE similar to FA should be updated based on GL data automated"
- **PPE:** "PPE- stick to the data in the ledger -- no reclass"
- **RPT gross/net:** a setting (see §2).
- **Order of work** (11:43): "1) Swelect first reconcile with audited FS June and March 2) Acko next 3) TVS build in parallel-- deloy step by step and match with audited financials and then confirm"

**Cross-cutting working rules**
- "show me a mock up and then once i confirm implement"; "do not build till you have 100% clarifty".
- "every button / every screen has to be focussed and cannot carry bloat".
- "think always first principles"; "ANy developmwnt ask does it follow Arjun first principles and explain"; "why create workflows for problems which already is supported by workflows"; "dont create new structures try and reuse existing ones".
- "dont give me TSV ever again". Excel only.
- "no JE is to be posted" (Swelect test). Nothing goes to FINAHQ without Approve. Don't act "suo moto".
- **Working papers:** "all hyperlinked to base data — add columns, tags to base data and sum if — must look like a workpaper"; "Sum if is not negotaible"; "The data has to be presented asthtically well"; "Users should be able to navigate the sheet in less than 1-2 mins".
  - Formatting as recorded in the spec: Arial, navy headers, totals with a top border, frozen panes, filters, Indian numbers with brackets and "–", shaded input cells, an index sheet first, and a test every release.
- "look and feel should be closer to what we saw yesterday without loosing the functionality"; "i said look at look feel of mock ups what final and mirror".
- "keep it simple always first principles"; "dont conduse the ICO engine".
- **Security:** keep tenants and logins strictly separate. Use the TVS login only for TVS. The Swelect password was to be changed after testing.

---

## 6. Artifacts, repos, branches and files

**Artifacts** (claude.ai)

| Title / file | Link |
|---|---|
| Disclosures mock-up (`disclosures_mock.html`) | https://claude.ai/artifact/T1BpnCkdAqCdCRnSs4Zuda |
| ICO flow mock-up (`ico_flow_mock.html`) | https://claude.ai/artifact/CNDGLbaw2ScLzuFoFD96Xp |
| Acko labels mock-up (`acko_labels_mock.html`) | https://claude.ai/artifact/2MSYZHypEBrhWpUGtUUiM8 |

**Repo:** FINKJUN/finahq-ap-onboarding. Munshi is in `mcp/munshi/backend`; the FINAHQ MCP is `mcp/finahq_mcp/server.py`.

**Branches and PRs**

| Branch / PR | What it is |
|---|---|
| `claude/cool-bardeen-57cea6-tvs` | TVS Disclosures; **PR #61, open, not merged** |
| `claude/cool-bardeen-57cea6-acko` | The base the TVS branch was cut from (Acko labels; PR #60, merged) |
| #58 | ICO round G |
| #59 | Legal-name pair matching |
| #62 | GLOBAL_MASTERS fallback |
| #63 | Party from document |
| #64 | ICO working paper rebuild |
| #67 | TB container month; measure before write |
| #68 | Labels per company |
| #69 | Splink / OR-Tools / AI |
| #70 | Labels by SOP; period at download; comparative not Munshi's process; step 9 |
| #71 | Labels wording: groups the SOP leaves out say "left out by the SOP's label filter" |
| #72 | Month page tabs fix |
| #73 | ICO L1 filter, margins screen |

Other branches named: `claude/cool-bardeen-57cea6-ackoadj`, `-labelword`, `-l1filter`, `-monthtabs`, `-wp`, `-polish`, `-roundg`, `-roundd`.

**Worktrees in the old container:** `/home/user/wt-tvs` (TVS), `/home/user/wt-int` (integration, live tools), `/home/user/wt-icotab`, `/home/user/wt-acko`, `/home/user/wt-polish`, `/home/user/wt-wp`, `/home/user/wt-l1filter`, `/home/user/wt-monthtabs`, `/home/user/wt-labelword`.

**TVS files in the repo** (paths under `mcp/`)
- Spec and design: `munshi/STANDARDISATION_LAYER.md`, `munshi/docs/group-of-entities.md`.
- Backend modules:
  - new: `munshi/backend/master_disclosures.py`, `disc_page.py`, `disc_fields.py`, `disc_defs.py`, `disc_masters.py`, `disc_engine.py`, `disc_write.py`;
  - existing: `master_ageing.py`, `master_rpt.py`, `rpt_rules.py`, `rpt_match.py`, `rpt_flows.py`, `rpt_declared.py`, `entity_group.py`, `ledger_store.py`, `ledger_schema.py`, `structure2.py`.
- TVS tools: `tools/munshi_tvs_sop.py`, `tools/sop_v17.py`, `tools/munshi_tvs_disclosures.py`, `tools/tvs_disclosures_offline.py`.
- TVS data and inputs: `tools/inputs/tvs/` (SOP workbooks v1.0–v3.7, the disclosure measure workbook), `tools/tally/cache/TVS_Emerald_Limited`, `tools/tally/parser.py` (`is_msme`), `finahq_mcp/data/gdt_crosswalk_v1.json`.
- Tests:
  - `tests/test_munshi_disclosures.py`, `tests/disc_fixture.py`;
  - `tests/test_munshi_tvs_disclosures.py`, `tests/test_munshi_tvs_full_financials.py`, `tests/test_munshi_reconcile.py` (TVS rehearsal);
  - `tests/dress/tvs_186/` (`coa.xlsx`, GDT snapshots such as `gdt/8416dc18f4_2025-04-01_2026-03-31.json`).
- Skill: `.claude/skills/munshi-sop-author/SKILL.md`.

**Old-session scratchpad deliverables.** These may not be reachable from a new session; regenerate them from the tools if missing.
- `fresh/TVS SOP - disclosures.xlsx`
- `fresh/TVS disclosures vs signed.xlsx`
- `tvs_shots/` (14 PNGs)
- `tvs_v36_new.xlsx`

Regenerate with:
- `python3 tools/munshi_tvs_disclosures.py "<out>/TVS SOP - disclosures.xlsx"`
- `python3 tools/tvs_disclosures_offline.py "<out>/TVS disclosures vs signed.xlsx"`

**Tenants and logins**
- TVS: tenant **186**, "Emerald Haven Development Limited". Login `corp_controller_emerald@finahq.com`; the password was shared in the transcript, so ask Arjun rather than reuse it.
- Acko: tenant 183, `fhq_corp_controller@acko.com`.
- Swelect: tenant 175, `corp_controller@swelect.com`.
- FINAHQ entity for TVSEL: 4122. Group entities: 4122–4139.

---

## 7. Suggested next steps for TVS

1. **Confirm scope and order with Arjun.** He ranked TVS third, "in parallel". Ask whether he wants PR #61 released now.
2. **Bring PR #61 up to date.** Rebase or merge `claude/cool-bardeen-57cea6-tvs` onto current main (PRs #62–#73 have landed since), resolve conflicts, and re-check where #70 touches `TVS_COLS` tests. Then run the full suite to "fail 0" and the py311 guard, and release with Arjun's OK.
3. **Get Arjun's answers** on:
   - the GDT targets for EPS diluted shares, the SOCIE round-off and MSMED s22;
   - the HDFC Benz loan terms;
   - whether "only required computed disclosures block publishing" and "list GDTs replace the whole period after Approve" are confirmed. They were put as questions on 10-04 11:21 and treated as decisions in the build brief.
4. **Re-run the offline comparison against FINAHQ's live TB** (read-only) instead of the Tally stand-in, to close the SOCIE and ageing gaps. Rebuild `TVS disclosures vs signed.xlsx` to the working-paper rules: base data plus tags, every figure a SUMIFS, links, Excel only.
5. **Live set-up on tenant 186**, only after release and Arjun's go:
   - upload the revised TVS SOP;
   - set up Get data from Tally;
   - create the containers;
   - start with entity 4122 (TVSEL) for FY25-26;
   - then extend to the other 17 entities.

   Never press Approve or write to FINAHQ without Arjun.
6. **Show a mock-up first** for any UI change, and measure the UI at real volume: 18 entities × 25 GDTs.
7. **Keep TVS isolated:** use only the TVS login and tenant 186. Do not reuse Acko's or Swelect's tenants or credentials.
