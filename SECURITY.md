# Security Policy

## Scope

`indie-game-ai-forge` generates full indie game projects from a design prompt: ingest → processors → output drivers. The attack surface is:

- **Ingest handlers** — they read user-supplied prompts, reference files, and asset packs. Malformed input is the most likely vector.
- **Output drivers** — they write to a destination directory. Path traversal in a driver is a real bug class.
- **The native bridge** (`native/forge_native`) — optional C++ accelerator, loaded via ctypes when `FORGE_NATIVE=1`. A bad `.dll` next to the exe is a load-order risk.
- **Plugin processors** — third-party processors are imported dynamically. They are trusted-by-default; do not enable untrusted plugin dirs.

## Reporting

Open a private security advisory on GitHub, or email `security@indie-game-ai-forge.dev`. Include: forge version, OS, a minimal repro (prompt + config), and the traceback.

We aim to respond within 72h. We do not run a bounty.

## Hardening notes for users

- Run the forge against a scratch directory. Output drivers overwrite files they own.
- Do not point `FORGE_PLUGIN_DIR` at a directory you don't trust — plugin processors execute Python.
- The native bridge is optional; if you don't build it, set `FORGE_NATIVE=0`.
- Generated projects are untrusted input for whatever engine you open them in. Treat generated scripts like any downloaded mod.

## Known non-issues

- Processors making no network calls is by design.
- `igpack` files are not signed; signing is out of scope for v1.