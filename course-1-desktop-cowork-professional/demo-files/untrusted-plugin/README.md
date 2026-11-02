# quick-notes (Demo 7 teaching sample)

A fictional third-party plugin written to be reviewed, never installed. Everything suspicious in it is deliberate. All hosts use the reserved `.invalid` name and cannot resolve.

Do not install it, do not start a Claude session with it loaded, and do not run `bin/qn-sync`. Review it with `claude plugin validate` and `claude --plugin-dir <this folder> plugin details quick-notes`, which only read the folder.
