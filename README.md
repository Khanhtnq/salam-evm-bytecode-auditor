# Salam EVM Bytecode & EIP-1967 Proxy Security Auditor

An offline, deterministic command-line security auditor for EVM contract manifests and hex bytecode, **built with the [Salam Programming Language](https://github.com/SalamLang/Salam)**.

Repository link to official Salam compiler & language: https://github.com/SalamLang/Salam

## Overview

`salam-evm-bytecode-auditor` reads a pipe-delimited EVM contract record (`NAME|CHAIN|ADDRESS|HEX_BYTECODE|HAS_PROXY_SLOT|VERIFIED_SOURCE`) and runs four independent, deterministic security checks written in modular Salam (`src/*.salam`):

1. **Dangerous Opcode Scan (`src/opcode_check.salam`)**: Flags `DELEGATECALL` (`0xf4`) and `SELFDESTRUCT` (`0xff`) patterns in runtime bytecode.
2. **EIP-1967 Proxy Upgradeability Check (`src/proxy_check.salam`)**: Evaluates proxy implementation slot exposure (`0x360894...`).
3. **Source Verification Check (`src/proxy_check.salam`)**: Penalizes unverified opaque bytecode deployments.
4. **Bytecode Footprint Check (`src/score.salam`)**: Detects minimal proxy stubs vs. full contract implementations and computes a `0–100` risk score (`LOW_RISK`, `ELEVATED_MONITORING`, `CRITICAL_REVIEW`).

## Project Structure (Multi-File Salam Architecture)

- `salam.salam` — CLI entry point and exit-code dispatcher (`0` safe/monitoring, `2` critical review, `64` invalid manifest)
- `src/model.salam` — Strongly typed Salam `struct` definitions (`ContractRecord`, `ParseResult`, `FindingCheck`, `AuditSummary`)
- `src/hexclean.salam` — Hex normalization and field sanitizer
- `src/parser.salam` — Manifest record parser and even-length hex validator
- `src/opcode_check.salam` — `DELEGATECALL` / `SELFDESTRUCT` pattern inspector
- `src/proxy_check.salam` — EIP-1967 proxy and source verification evaluator
- `src/score.salam` — Composite risk scorer (`0–100`) and security posture classifier
- `src/report.salam` — Human- and CI-friendly report formatter
- `samples/` — Sample EVM contract records (`aave_v3_pool_proxy.txt`, `unverified_selfdestruct_vault.txt`)
- `Dockerfile` & `docker-compose.yml` — Ready-to-run Docker setup using `basemax/salam:latest`

## How to Run

### Using Salam CLI Directly

```bash
salam exec salam.salam samples/aave_v3_pool_proxy.txt
salam exec salam.salam samples/unverified_selfdestruct_vault.txt
```

### Using Docker (`basemax/salam`)

```bash
docker compose run --rm salam-evm-auditor samples/aave_v3_pool_proxy.txt
```

## Example Output

```text
Contract: AaveV3Pool (ethereum 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2)
Security Posture: ELEVATED_MONITORING | Risk Score: 45/100
[FLAG] EVM-OP-02 (+25): contains DELEGATECALL (0xf4) execution path
[FLAG] EIP1967-PROXY (+20): active EIP-1967 upgradeable proxy slot detected; monitor implementation changes
[PASS] SOURCE-VERIFIED (+0): contract source code is publicly verified
[PASS] STANDARD-SIZE (+0): bytecode size 126 bytes within normal contract range
```

## License

MIT
