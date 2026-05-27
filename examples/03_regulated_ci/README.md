# Regulated/CI Environment Example

This example demonstrates how to use langgraph-evals in completely regulated, air-gapped, or zero-trust environments with **zero external dependencies** and **no API key requirements**.

## Features

- **Fully Offline Operation**: No network calls, no external services required
- **Zero API Keys**: Works without any LLM API keys or external service credentials
- **CI/CD Integration**: Example GitHub Actions workflow for regulated environments
- **Compliance Reporting**: JSON reporter for audit trails and compliance documentation
- **Failure Detection**: Offline failure classification for issue identification
- **Regulation Friendly**: Suitable for SSLF, HIPAA, GDPR, FINRA, and other regulated industries

## Files in This Example

1. `test_regulated.py` - Demonstrates offline usage of:
   - FailureClassifier for detecting issues without external dependencies
   - JsonReporter for generating compliance-ready JSON reports
   - All operations run completely offline

2. `ci_workflow_example.yml` - GitHub Actions workflow showing:
   - How to run langgraph-evals in CI with zero external API calls
   - Self-hosted runner compatibility for air-gapped networks
   - Artifact upload for compliance reporting
   - No API key requirements whatsoever

## Running the Example

```bash
# Run the regulated environment tests
python -m pytest examples/03_regulated_ci/ -v

# Or run the test directly
python examples/03_regulated_ci/test_regulated.py
```

## Using in Regulated Environments

langgraph-evals is designed to work in environments where:
- Outbound network calls are restricted or prohibited
- No external API keys are permitted
- All software must be pre-approved and vetted
- Audit trails and compliance reporting are required
- Air-gapped or isolated networks are mandatory

## Key Benefits for Regulated Use

1. **No External Dependencies**: All functionality works with locally installed packages only
2. **Deterministic Behavior**: Same inputs produce same outputs for reproducibility
3. **No Data Exfiltration**: Evaluation data remains within your secure environment
4. **Compliance Ready**: JSON reports can be archived for audit purposes
5. **FIPS/HIPAA/GDPR Compatible**: No external service calls that might violate regulations

## Workflow Example

The included `ci_workflow_example.yml` shows how to:
- Check out code in a secure environment
- Install dependencies from approved/local sources only
- Run tests and evaluations without external API calls
- Generate JSON reports for compliance tracking
- Upload artifacts for long-term storage (within your secure network)
- Perform compliance checks as part of the CI pipeline

This example demonstrates that langgraph-evals can be used in even the most restrictive environments without compromising functionality or requiring external service integrations.