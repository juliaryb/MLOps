# Lab 13 - LLMOps

"This lab will cover building LLM-based systems, including efficient LLM inference, enabling tool usage, and securing them with guardrails."

## Hardware constraints
CPU-only machine, 16GB RAM
Decisions: 
- smaller model: Qwen3-0.6B
- deleted "bitsandbytes>=0.49.1" from the pyproject.toml file

## vLLM inference:
after installing the venv I'm using: 
```
vllm serve Qwen/Qwen3-0.6B --port 8000 --max-model-len 2048
``` 
for the hardware constraints mentioned.

That didn't work..
```
raise RuntimeError(
RuntimeError: Failed to infer device type, please set the environment variable `VLLM_LOGGING_LEVEL=DEBUG` to turn on verbose logging to help debug the issue.
```

So I'll use a cloud-hosted LLM - tried OpenAI API but it needs billing to be set up. I'll use Gemini API.

## Exercise 1
I unfortunately cannot run it without the GPU present and vLLM not working (or at least not quickly/cost-free enough)

## Tool usage
