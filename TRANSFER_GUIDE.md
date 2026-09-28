# Transfer without ZIP

1. On your laptop create a folder named `MedTrace_AI`.
2. Save `setup_project_structure.ps1` and `FILE_MANIFEST.md` there first. Review the PowerShell script; it only creates folders. Run it if your organization's policy permits scripts, or create the listed folders manually. Do not change organizational execution policy.
3. Download each delivered file into its exact relative path from the manifest. Preserve names, extensions and package `__init__.py` files. Use VS Code to create a file and paste its full contents if direct download is unavailable.
4. Copy `.env.example` to `.env` locally. The leading dot is intentional. Do not share credentials.
5. Follow the README virtual-environment commands. An approved Git repository is another ordinary transfer option if your organization permits it; it is not required.
6. Start Streamlit and run the example. No additional dataset upload is needed for the bundled demonstration.

No archive is required. Do not rename an archive to evade transfer restrictions. If installation or download is blocked by managed-device policy, request the approved Python/package/data transfer route from your IT team.

## Required versus optional
Core run: root requirements/config, all application and source Python files, bundled `data/sample/maude_sample.csv`, recall JSON, processed regulatory chunks. Original FDA raw records and source HTML support reproducibility. Advanced requirements/model weights, notebooks, tests, Docker and generated reports are optional for the first run but included for research and development.

Never transfer `.venv`, caches, local database, downloaded private model secrets or `.env` credentials. Recreate dependencies on the destination computer.
