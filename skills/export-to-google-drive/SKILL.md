---
name: export-to-google-drive
description: Upload or re-export locally generated deliverables to Google Drive with project folders, consistent names, and duplicate-aware revision handling. Use when sending generated presentations, documents, spreadsheets, PDFs, images, or other local outputs to Drive, including native Google Workspace imports. Does not cover downloading from Drive or bulk cleanup of existing files.
---

# Export to Google Drive

Keep related outputs together under `Projects/<project>`, with recognizable names
and one current export per deliverable and format. Use the connected Google Drive
tools and the installed Google Drive skill; use its Docs, Sheets, or Slides
workflow when native conversion is needed. Inspect live tool schemas before use.

## Choose the destination

- Honor an explicit folder or an established project destination first. Otherwise
  use `My Drive/Projects/<project>`. Infer the project from the task or artifact;
  ask only when the choice would put files in the wrong project or account.
- Resolve the connected account and verify any saved folder IDs. A browser account
  or screenshot does not establish which account the connector uses. Home,
  Recent, and Suggested files do not establish a file's parent folder.
- Find `Projects` within My Drive root, then the exact project folder within it.
  Search by parent, name, folder MIME type, and `trashed = false`; follow returned
  page tokens before concluding that a folder is absent. Reuse verified IDs.
  Resolve multiple matching folders from task context or ask; do not choose one
  arbitrarily or create another duplicate.
- Create only missing folders needed for the selected exports. Folder creation
  is part of an authorized export and needs no separate confirmation. Pass the
  project folder ID to the upload/import instead of leaving outputs in root.
- Keep the hierarchy shallow: current deliverables go directly in the project
  folder. Create `Archive` inside that folder only when retaining superseded
  copies. Do not create empty type, date, or status folders for each export.

For example, a project can contain these requested deliverables:

```text
Projects/
  AI应用创新/
    AI应用创新 — 演示文稿
    AI应用创新 — 讲稿
    AI应用创新 — 行动清单
    AI应用创新 — 演示文稿.pdf
    Archive/                         # only when needed
```

The extensionless names above are native Google files. This example does not
require producing or uploading every listed format.

## Select files and names

- Upload the requested finished deliverables. Local builds, previews, extracted
  assets, logs, and intermediate drafts stay local unless requested.
- Prefer `<project> — <deliverable>` for new Drive titles. Preserve the user's
  language, terminology, explicit titles, and meaningful reporting dates. Avoid
  build timestamps, temporary basenames, and `final-final-v3` suffixes on current
  exports. Change the Drive title without renaming the local source unnecessarily.
- Preserve the correct extension for stored files; omit Office extensions from
  native Docs, Sheets, and Slides titles. Use the representation requested by the
  user or established by the active authoring workflow. For generic file storage,
  preserve the source format. Upload both native and original copies only when
  both are requested.
- State the destination, intended titles, and whether this creates or updates
  files briefly before writing. Proceed within the existing export authorization;
  do not add a routine approval checkpoint.

## Re-export without accumulating duplicates

Identify an artifact by its project, deliverable, representation, and any reporting
period, not by a temporary local path. First reuse file IDs recorded by an earlier
export or explicitly supplied by the user. Otherwise inspect candidates within
the destination folder. A matching name alone does not authorize replacement.

Read the target's metadata before deciding. A changed remote version takes
precedence over the update cases below:

| Situation | Action |
| --- | --- |
| No existing export of this artifact | Create it in the project folder. |
| Local source hash and recorded remote version are unchanged | Reuse the existing file after verifying its title, type, and location. |
| A known stored file needs an authorized update | Replace its bytes with `update_file`, preserving its Drive ID and link. |
| A native Google file needs an edit that the native tools support | Use the matching Docs, Sheets, or Slides workflow to preserve its ID. |
| A generated native export must be rebuilt from the local Office file | Reimport, verify the new file, then archive the mapped predecessor when superseding it is within scope. Report the new link. |
| The target has changed in Drive since the recorded export | Inspect the change. Preserve remote edits; clarify before replacing content if the intended source of truth is unresolved. |
| Identity is ambiguous, or same-named files are unrelated | Resolve the target or give the new deliverable a distinguishing title; do not overwrite by name. |

Native import creates a new file; it does not update an existing native document.
Do not send Office bytes to `update_file` for a native Google file. If the user
requires the same native link, use supported native edits or explain the limitation
before substituting a new file. Do not silently lose collaborative edits or comments
by replacing a document with a fresh import.

Archive only a verified predecessor belonging to the current export workflow,
after its replacement passes readback. Keep its file ID, append a timestamp in
the user's timezone to its title, and move it into this project's `Archive`.
Read its parents first, add the archive folder, and remove only the verified
project parent. Do not delete earlier files, archive unrelated matches, or move
a user-specified file outside the established project as incidental cleanup.

## Use the connector correctly

- `create_folder` uses `parent_folder`; uploads and native imports use
  `parent_folder_id`. Supply the resolved folder ID for the latter, not a folder
  name, URL, or local path. Exact search uses `special_filter_query_str`; escape
  names for Drive query syntax and use the live pagination fields.
- Use `upload_file` for new stored files and `import_document`,
  `import_spreadsheet`, or `import_presentation` for native imports. `export_file`
  is the opposite direction: exporting an existing native Drive file.
- Pass local bytes through the runtime's supported file input. If the live schema
  accepts an absolute local path, use the verified path; if it requires an
  authenticated file reference, obtain that reference first. Do not invent a
  reference, send inline base64, or publish the file elsewhere to obtain a URL.
- If an action cannot place a new file directly in the target folder, record its
  returned ID, read its current parents, then move that same file with
  `update_file(addParents=..., removeParents=...)`. Verify the destination;
  uploading a second copy is not a move.
- After a timeout or ambiguous result, reconcile by returned ID or a targeted
  destination search before retrying a creation. If its outcome remains unknown,
  stop that write and report the uncertainty instead of creating more copies.

## Verify and remember the export

Keep a small local `drive-export.json` beside the project's output files, reusing
an existing publication manifest when it serves the same purpose. Record the
connected account, project folder ID and URL, and for each artifact its stable
key, local path, source SHA-256, Drive file ID, title, MIME type, URL, remote
version or modification time, and export time. Do not upload this bookkeeping file
unless requested or store authentication material in it.

Record returned IDs after successful creation so a failed move or readback can
resume with the same file. Retain the predecessor mapping until replacement and
placement are verified; mark incomplete operations clearly rather than recording
them as successful exports. Update the manifest from final readback, not predicted
IDs or links.

Before reporting success, read back the file's title, MIME type, parent folder,
URL, and version. For stored files, compare available byte size or checksum with
the local source. For native conversion, use an appropriate content or structural
readback against the source and disclose any observed conversion loss. Verify any
archive move too. Report partial successes individually.

Return the project folder link and concise links to the verified deliverables,
noting whether each was created, updated, reused, or replaced with a new native
link. Preserve sharing settings. Bulk reorganization, deletion, and sharing are
separate tasks and are not implied by an export request.
