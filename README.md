# SingleStore Supported Versions Action

This GitHub Action retrieves **SingleStore versions** that are **not End of Life (EOL)** by scraping the official
documentation page.

## Outputs

- `versions`: A **JSON array** containing the supported versions that are not EOL, extracted from the documentation.

## Example Usage

Here’s how to use this action in your GitHub workflows:

```yaml
name: Test

on:
  pull_request:
    types: [ opened, synchronize, reopened ]
  schedule:
    - cron: "0 0 * * 0"

jobs:
  fetch-s2-versions:
    runs-on: ubuntu-latest
    outputs:
      versions: ${{ steps.get_versions.outputs.versions }}
    steps:
      - name: Get supported versions of Singlestore
        id: get_versions
        uses: singlestore-labs/singlestore-supported-versions@main

  test:
    needs: fetch-s2-versions
    runs-on: ubuntu-latest

    strategy:
      matrix:
        singlestore_version: ${{ fromJson(needs.fetch-s2-versions.outputs.versions) }}

    services:
      singlestore:
        image: ghcr.io/singlestore-labs/singlestoredb-dev:latest
        ports:
          - "3306:3306"
        env:
          SINGLESTORE_LICENSE: ${{ secrets.SINGLESTORE_LICENSE }}
          ROOT_PASSWORD: ${{ secrets.SINGLESTORE_PASSWORD }}
          SINGELSTORE_VERSION: ${{ matrix.singlestore_version }}
```
