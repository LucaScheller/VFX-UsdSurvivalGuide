# Documentation

If you want to locally build this documentation, you'll have to download [mdBook](https://github.com/rust-lang/mdBook), [mdBook-admonish](https://github.com/tommilligan/mdbook-admonish) and [mdBook-mermaid](https://github.com/badboy/mdbook-mermaid) and add their parent directories to the `PATH`env variable so that the executables are found.

You can do this via bash (after running `source setup.sh`):
```bash
export MDBOOK_VERSION="0.4.28"
export MDBOOK_ADMONISH_VERSION="1.9.0"
export MDBOOK_MERMAID_VERSION="0.12.6"
curl -L https://github.com/rust-lang/mdBook/releases/download/v$MDBOOK_VERSION/mdbook-v$MDBOOK_VERSION-x86_64-unknown-linux-gnu.tar.gz | tar xz -C ${REPO_ROOT}/tools
curl -L https://github.com/tommilligan/mdbook-admonish/releases/download/v$MDBOOK_ADMONISH_VERSION/mdbook-admonish-v$MDBOOK_ADMONISH_VERSION-x86_64-unknown-linux-gnu.tar.gz | tar xz -C ${REPO_ROOT}/tools
curl -L https://github.com/badboy/mdbook-mermaid/releases/download/v$MDBOOK_MERMAID_VERSION/mdbook-mermaid-v$MDBOOK_MERMAID_VERSION-x86_64-unknown-linux-gnu.tar.gz | tar xz -C ~/tools
export PATH=${REPO_ROOT}/tools:$PATH
```

You then can just run the following to build the documentation in html format:
```bash
./docs.sh
```

The documentation will then be built in docs/book.