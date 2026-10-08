# Audit verification

Audit source: supplied compass_artifact_wf-8f32e147-9bf3-5208-ba05-acfbbd390eae_text_markdown.md, outcome-check section and shared recommendations. This file separates repository verification from claims about collectors or external reality.

## Phase 0 baseline

HEAD 1d52b8e92790fcd304cb0da5309822a2c3d8d844, clean isolated clone. Frozen lock: 8 packages. Python 3.13.9, Node v22.23.2. 49 tests passed; Ruff lint and format passed; wheel and sdist built. Runtime dependencies: zero.

| Finding | Verification | Resolution |
| --- | --- | --- |
| Read-only/no shell, network or code execution only partially supported | Confirmed with source inspection: core.py:4/18 compares supplied JSON; contract.py:155/156 reads input rb; cli.py:52-55 writes reports only. No subprocess, os.system, socket, urllib, eval or exec occurrence in these files. | Read-only refers to checked systems; report exports write local files. Guarded runtime proof added in v0.3.0. |
| Explicit observation IDs | Confirmed: core indexes observations and addresses observation_id, never row order. | Retained and tested with retries. |
| Action separate from outcome | Confirmed: action status computed independently and both retained. | Retained; failed action overrides otherwise matching state. |
| Freshness rules | Confirmed: Fraction arithmetic in contract.py:54 uses every fractional digit; inclusive [0,max_age] in core. | Retained plus property tests. |
| Typed equality | Confirmed: core.py:4 checks exact types recursively, with numeric int/float equivalence. | Retained as default and reused by contains/baselines. |
| Safe outputs | Partial: input and hard-link alias checks confirmed, validation preserves output; write failure could truncate existing output. | Per-file atomic writes with fault/race tests. |
| Trust boundary external/unsigned | Confirmed: hashes bind bytes, supplied observations cannot prove truth. | Optional local signatures; explicit unsigned/unverified/verified/invalid labels and precise canonicalization limits. Truth boundary retained. |
| Equality only | Confirmed at baseline. | Version 2 ranges, typed array contains, restricted regex and baseline checks. |
| Do-nothing exploit | Confirmed: equal final state can confirm even if it existed already. | requires_change plus explicit preaction baseline yields unconfirmed for unchanged satisfied state. |
| No adapters | Confirmed at baseline; a generic format does not collect benchmark state. | Explicit final-state mapping and supplied public trajectory study; no benchmark execution claim. |
| 45 vs 49 tests | Confirmed baseline has 49. | PR head 9c96f81 and squash 939b9a5 tests identical; isolated head has49. PRbody45 stale; v0.2.0 release49 correct. Links in docs/related-work.md. |
| First PR nonpassing check | Root verified 15 successful Actions checks, CodeRabbit pending. | No test failure inferred from the aggregate 15/16 display. |
| No property tests/schemas | Confirmed at baseline. | Hypothesis freshness and versioned Draft 2020-12 schemas. |
| Python floor/distribution | Confirmed Python >=3.13 and GitHub artifact installation. | 3.11 compatibility tested; publication remains explicitly out of scope. |
| Outside users/adoption | Not established by inspected repository. | No adoption or production claim added. |
| Security alerts/Dependabot | Configuration inspection only; hosted settings are not inferred. | Root owns settings verification and security CI work. |
| Novelty/research merit | Interpretation, not a code defect. | Related work and evidence limitations retained; study states sample scope. |


## Final source and contract verification

- core.py same_json:5 retains typed recursion. compare:118 implements ranges,
  array contains and restricted regex. compare_baseline:151 explicitly binds
  baseline ID, subject, temporal ordering and object path. Unchanged satisfied
  required-change state becomes unconfirmed; contradictory unchanged/change flags
  are rejected by contract validation.
- contract.py age_seconds:54 retains exact Fraction comparisons. load_packet:160
  opens only rb at161. validate_v2:175 validates extensions without relaxing v1.
- cli.py delegates requested report writes to atomic_write, and writes JSON stdout.
  output.py atomic_write:26 stages requested reports; stream.write:39, fsync,
  os.replace or no-clobber os.link, then stage cleanup. signatures.py public-key
  loader opens rb only. No runtime source imports/calls subprocess, os.system,
  socket, urllib, eval or exec. Package signing/verifying imports cryptography
  only inside the optional functions.
- Guarded full CLI and core v1/v2 (signed and unsigned) fixture run denies network,
  subprocess and os.system, and write-open outside declared target/stage paths.
  Source bytes are checked unchanged afterward. Caller-provided verifier code is
  trusted application code, outside packet execution and this finite test proof.
- Every audit implementation recommendation has an implemented local resolution.
  Public study scope, hosted security settings, release/publish/merge/Pages gates,
  absent adoption evidence and full RFC 8785 float interoperability remain explicit
  limits, not completed external effects.
- Final product suite: 49 baseline to114 tests, including200 Hypothesis generated
  freshness examples per default run across2 property tests. Type check, lint,
  schemas and builds are independently run; no test count is inferred from docs.
  Frozen lock8 to69 entries, zero default runtime dependencies. Historical3.11.14
  interpreter was broken before project import; independent3.11.13 works.


Product commit31269ea was cloned locally without hard links into an ignored
build/verification-clone. Frozen installation,114 tests, Ruff lint/format, mypy,
all12schemas/all6JSONexamples, build and isolated installed-wheel v1/v2 smoke
passed there; git status remained clean. This verifies the committed product,
not the root-owned uncommitted CI/public-study files. Original wheel and sdist
were also separately built, checked by twine and installed/tested in fresh venvs.
The default installed artifacts had no cryptography dependency.
