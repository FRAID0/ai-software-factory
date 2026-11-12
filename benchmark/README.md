# Model Benchmarking & Evaluation Suite

This module establishes the quantitative evaluation harness for assessing LLM provider performance within the AI Software Factory.

## Evaluation Criteria
1. **Code Generation Pass Rate**: % of generated solutions passing isolated unit test suites (HumanEval / custom factory scenarios).
2. **Reasoning & Planning Quality**: Correctness of dependency DAG resolution and boundary condition analysis.
3. **Latency Profile**:
   - Time to First Token (TTFT)
   - Total Response Time (RTT)
4. **Token Efficiency**: Number of tokens required to successfully deliver verified working code.
5. **Cost Metric**: Monetary cost per successful task completion.

## Guidelines
- **Do not fabricate benchmark results**: All metrics are captured dynamically during real execution runs against vetted problem sets.
- Results are saved with timestamp, model name, provider, and full prompt metadata for reproducibility.

