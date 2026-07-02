# Run Nextflow pipelines

Nextflow is a workflow engine for running pipelines at scale.

To run a pipeline, use the `nextflow run` command. You can pass parameters and options:

- `--input <path>` sets the input samplesheet. It is a pipeline parameter and takes two dashes.
- `-resume` continues a previous run. It is a Nextflow core option and takes a single dash.
- `-profile` selects a configuration profile. It is also a Nextflow core option and takes a single dash.

The `workflow` block composes processes and connects them with channels.

## Troubleshooting

### Error: `Unable to acquire lock on session`

This error occurs when another Nextflow run is using the same session directory (the `.nextflow` directory).

To resolve, confirm no other run is using that directory, then re-run with `-resume`.
