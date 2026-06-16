# cleanup_garbage.ps1 - audited removal of temp / QA / extraction / scratch files.
# Run from the project folder:
#     powershell -ExecutionPolicy Bypass -File .\cleanup_garbage.ps1
$ErrorActionPreference = "SilentlyContinue"
Set-Location $PSScriptRoot
function Del($p){ if (Test-Path -LiteralPath $p) { Write-Host ("  del " + $p); Remove-Item -LiteralPath $p -Recurse -Force } }

Write-Host "=== Tier 1: garbage temp / QA / backup files ==="
Get-ChildItem -Path . -Filter "_check_*.jpg" -File | ForEach-Object { Del $_.FullName }
Get-ChildItem -Path . -Recurse -Include *.bak -File | ForEach-Object { Del $_.FullName }
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | ForEach-Object { Del $_.FullName }
Del "sequence_tests\corpus\_try.txt"
Del "sequence_tests\corpus\_saj_raw.txt"
Del "sequence_tests\corpus\_saj_hariri_raw.txt"
Get-ChildItem -Path "sequence_tests\corpus" -Filter "*.raw.txt" -File | ForEach-Object { Del $_.FullName }
Del "Hingham_media\_view"
Del "Hingham_media\_frames"
Del "Hingham_media\_PUT_FILES_HERE.txt"

Write-Host ""
Write-Host "=== Tier 2: redundant downloads (already extracted to ar_large_classical.txt) ==="
Del "sequence_tests\corpus\Nahjul Balagha Part 1 - The Sermons.epub"
Del "sequence_tests\corpus\Nahjul Balagha Part 2, Letters and Sayings.epub"
Del "sequence_tests\corpus\nahjul_balagha_part_1_-_the_sermons.pdf"
Del "sequence_tests\corpus\nahjul_balagha_part_2_letters_and_sayings.pdf"

Write-Host ""
Write-Host "=== Tier 3: LARGE / personal - NOT auto-deleted. Delete by hand if you want ==="
if (Test-Path "Hingham_media") { Write-Host "  Hingham_media  approx 257 MB original HEIC/MOV. Delete only if copies exist on D drive:" }
Write-Host "      Remove-Item Hingham_media -Recurse -Force"
if (Test-Path "presentations") { Write-Host "  presentations  approx 2.3 MB your pptx decks. Keep unless unwanted:" }
Write-Host "      # Remove-Item presentations -Recurse -Force"

Write-Host ""
Write-Host "=== Tier 4: orphan research scripts + unref output CSVs (NOT app code) ==="
Write-Host "These are not used by the app and are recoverable from git history."
$ans = Read-Host "Delete the ~36 research scratch files? Type YES to proceed"
if ($ans -eq "YES") {
  $orphans = @(
    "fusion_scan.py","fusion_fdr.py","fusion_motif.py","fusion_communities.py",
    "synergy_test.py","synergy_acrossverse.py","synergy_freqcontrol.py",
    "within_surah_rasm.py","within_surah_content2.py","confound_controls.py","control_corpus.py",
    "drift_control.py","surface_provenance.py","scale_adjudicate.py","seq_derisk.py","te_vs_app.py",
    "tensor_test.py","xscale_test.py","refcal_test.py","mi_decay_poc.py","ideas_batch1.py",
    "ideas_batch2_slim.py","content_confirm2.py","harvest_en.py","parse_fetch.py","finalize.py",
    "audit_deepdives.py","check_syntax.py",
    "importance_INTEGRATED.csv","importance_RANKED.csv","importance_TWO_SCALE.csv","importance_two_axis.csv",
    "root_importance_final.csv","root_importance_global.csv","SEAL_DEVIANTS.csv","SEAL_DICTIONARY.csv"
  )
  foreach ($f in $orphans) { Del $f }
  Write-Host "Tier 4 removed. (Recover any with: git checkout HEAD~1 -- <file>)"
} else {
  Write-Host "Tier 4 skipped (research files kept)."
}

Write-Host ""
Write-Host "Done. Run 'git status' to confirm. Next deploy will drop the removed files from the repo too."
