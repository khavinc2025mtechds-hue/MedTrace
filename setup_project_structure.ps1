# Creates directories only; does not overwrite project files.
$ProjectRoot = $PSScriptRoot
$Folders = @(
    'app',
    'app\components',
    'app\pages',
    'config',
    'data',
    'data\processed',
    'data\raw',
    'data\sample',
    'data\synthetic_optional',
    'datasets',
    'docs',
    'models',
    'models\classifiers',
    'models\embeddings',
    'models\priority',
    'notebooks',
    'regulatory_docs',
    'regulatory_docs\processed',
    'regulatory_docs\raw',
    'reports',
    'reports\evaluation',
    'reports\figures',
    'reports\sample_reports',
    'src',
    'src\agents',
    'src\analytics',
    'src\api',
    'src\database',
    'src\evaluation',
    'src\ingestion',
    'src\nlp',
    'src\preprocessing',
    'src\rag',
    'src\recalls',
    'src\reports',
    'src\retrieval',
    'tests',
    'vector_store'
)
foreach ($Folder in $Folders) {
    New-Item -ItemType Directory -Path (Join-Path $ProjectRoot $Folder) -Force | Out-Null
}
Write-Host 'MedTrace_AI folders are ready. Copy files using FILE_MANIFEST.md.'
