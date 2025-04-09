# SingleStore Supported Versions Action

This GitHub Action retrieves **SingleStore versions** that are **not End of Life (EOL)** by scraping the official
documentation page.

## Outputs

- `versions`: A **JSON array** containing the supported versions that are not EOL, extracted from the documentation.

## Example Usage

Here’s how to use this action in your GitHub workflows:

```yaml
name: Fetch Supported SingleStore Versions

on:
  workflow_dispatch:

jobs:
  fetch-supported-versions:
    runs-on: ubuntu-latest
    steps:
      - name: Get supported versions of SingleStore
        id: get_versions
        uses: your-username/singlestore-active-versions@v1

      - name: Display the supported versions
        run: echo "Supported SingleStore Versions: ${{ steps.get_versions.outputs.versions }}"
