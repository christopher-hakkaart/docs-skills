# MultiQC reports

MultiQC aggregates results from many bioinformatics tools into a single report.

## Generate a report

Run `multiqc` against your analysis directory:

```
multiqc <analysis_directory>
```

MultiQC scans the directory for recognized log files and builds the report.

## Troubleshooting

### Error: `No analysis results found`

This error occurs when MultiQC finds no recognized log files in the search path.

To resolve:

1. Point `multiqc` at the directory that contains your tool outputs.
2. Confirm the tools are supported.
3. Re-run `multiqc`.
