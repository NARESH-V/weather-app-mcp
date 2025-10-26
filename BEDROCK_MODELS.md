# AWS Bedrock Available Models

This document lists all available foundation models in AWS Bedrock (us-east-1 region).

## 🔥 Recommended Text Models

### Amazon Nova Models (Your Current Choice)
- **`amazon.nova-micro-v1:0`** ⭐ (You're using this)
  - Ultra-fast, lowest cost
  - Text-only
  - Best for: Simple tasks, high-volume workloads
  
- **`amazon.nova-lite-v1:0`**
  - Multimodal (text, images, video)
  - Low cost
  - Best for: General use with multimodal needs

- **`amazon.nova-pro-v1:0`**
  - Multimodal (text, images, video)
  - Most capable Nova model
  - Best for: Complex reasoning with multimodal inputs

- **`amazon.nova-premier-v1:0`**
  - Most advanced Nova model
  - Multiple context sizes available (8k, 20k, 1000k)
  - Multimodal capabilities

### Anthropic Claude Models (Premium Quality)
- **`anthropic.claude-3-5-sonnet-20241022-v2:0`**
  - Best overall quality
  - Multimodal (text + images)
  - Industry-leading performance

- **`anthropic.claude-3-5-haiku-20241022-v1:0`**
  - Fast and cost-effective
  - Text-only
  - Good balance of speed and quality

- **`anthropic.claude-3-haiku-20240307-v1:0`**
  - Fastest Claude model
  - Multimodal (text + images)
  - Most economical Claude option

- **`anthropic.claude-sonnet-4-20250514-v1:0`**
  - Latest Claude Sonnet 4
  - Cutting-edge capabilities
  - Multimodal (text + images)

- **`anthropic.claude-opus-4-20250514-v1:0`**
  - Highest quality Claude
  - Best for complex reasoning
  - Multimodal (text + images)

### Meta Llama Models (Open Source)
- **`meta.llama3-3-70b-instruct-v1:0`**
  - Latest Llama 3.3
  - 70B parameters
  - Great open-source alternative

- **`meta.llama4-scout-17b-instruct-v1:0`**
  - New Llama 4 Scout
  - Multimodal (text + images)
  - Good for specialized tasks

- **`meta.llama3-1-8b-instruct-v1:0`**
  - Smaller, faster
  - Lower cost
  - Good for simpler tasks

### Mistral AI Models
- **`mistral.mistral-large-2402-v1:0`**
  - High performance
  - Good for enterprise use

- **`mistral.mixtral-8x7b-instruct-v0:1`**
  - Mixture of experts architecture
  - Efficient and capable

### Cohere Models
- **`cohere.command-r-plus-v1:0`**
  - Optimized for RAG (Retrieval Augmented Generation)
  - Great for search and knowledge tasks

- **`cohere.command-r-v1:0`**
  - Balanced performance
  - Good for general use

## 💰 Cost Comparison (Approximate)

### Economy Tier
1. **`amazon.nova-micro-v1:0`** - Lowest cost ⭐ You're using this
2. `meta.llama3-2-1b-instruct-v1:0` - Very low cost
3. `mistral.mistral-7b-instruct-v0:2` - Low cost

### Balanced Tier
1. `amazon.nova-lite-v1:0` - Good value
2. `anthropic.claude-3-5-haiku-20241022-v1:0` - Fast & affordable
3. `meta.llama3-3-70b-instruct-v1:0` - Open-source quality

### Premium Tier
1. `anthropic.claude-3-5-sonnet-20241022-v2:0` - Best quality/price
2. `amazon.nova-pro-v1:0` - Multimodal premium
3. `anthropic.claude-sonnet-4-20250514-v1:0` - Latest generation

### Enterprise Tier
1. `anthropic.claude-opus-4-20250514-v1:0` - Highest capability
2. `amazon.nova-premier-v1:0` - Advanced reasoning
3. `anthropic.claude-opus-4-1-20250805-v1:0` - Top-tier performance

## 🎯 Model Selection Guide

### Your Current Setup
```python
BEDROCK_MODEL_ID='amazon.nova-micro-v1:0'
```

### When to Use What

**For Cost Optimization (Your Current Choice)**
```python
BEDROCK_MODEL_ID='amazon.nova-micro-v1:0'  # Lowest cost
```

**For Best Quality**
```python
BEDROCK_MODEL_ID='anthropic.claude-3-5-sonnet-20241022-v2:0'
```

**For Balanced Performance**
```python
BEDROCK_MODEL_ID='amazon.nova-lite-v1:0'  # or
BEDROCK_MODEL_ID='anthropic.claude-3-5-haiku-20241022-v1:0'
```

**For Multimodal (Images + Video)**
```python
BEDROCK_MODEL_ID='amazon.nova-pro-v1:0'
```

**For Open Source**
```python
BEDROCK_MODEL_ID='meta.llama3-3-70b-instruct-v1:0'
```

## 🔧 How to Switch Models

### Method 1: Update env.py
```python
BEDROCK_MODEL_ID='anthropic.claude-3-5-sonnet-20241022-v2:0'
```

### Method 2: Environment Variable
```bash
export BEDROCK_MODEL_ID='amazon.nova-pro-v1:0'
```

## 📊 All Text Generation Models Available

### Amazon Nova Family
- `amazon.nova-micro-v1:0` (text-only) ⭐
- `amazon.nova-micro-v1:0:24k` (24K context)
- `amazon.nova-micro-v1:0:128k` (128K context)
- `amazon.nova-lite-v1:0` (multimodal)
- `amazon.nova-lite-v1:0:24k`
- `amazon.nova-lite-v1:0:300k`
- `amazon.nova-pro-v1:0` (multimodal)
- `amazon.nova-pro-v1:0:24k`
- `amazon.nova-pro-v1:0:300k`
- `amazon.nova-premier-v1:0` (multimodal)
- `amazon.nova-premier-v1:0:8k`
- `amazon.nova-premier-v1:0:20k`
- `amazon.nova-premier-v1:0:1000k`
- `amazon.nova-sonic-v1:0` (speech-to-text)

### Anthropic Claude Family
**Latest Generation (Claude 4)**
- `anthropic.claude-sonnet-4-20250514-v1:0` (multimodal)
- `anthropic.claude-sonnet-4-5-20250929-v1:0` (multimodal)
- `anthropic.claude-haiku-4-5-20251001-v1:0` (multimodal)
- `anthropic.claude-opus-4-20250514-v1:0` (multimodal)
- `anthropic.claude-opus-4-1-20250805-v1:0` (multimodal)

**Claude 3.x Generation**
- `anthropic.claude-3-7-sonnet-20250219-v1:0` (multimodal)
- `anthropic.claude-3-5-sonnet-20241022-v2:0` (multimodal)
- `anthropic.claude-3-5-sonnet-20240620-v1:0` (multimodal)
- `anthropic.claude-3-5-haiku-20241022-v1:0` (text-only)
- `anthropic.claude-3-sonnet-20240229-v1:0` (multimodal)
- `anthropic.claude-3-haiku-20240307-v1:0` (multimodal)
- `anthropic.claude-3-opus-20240229-v1:0` (multimodal)

**Legacy Models**
- `anthropic.claude-v2:1:200k`
- `anthropic.claude-instant-v1:2:100k`

### Meta Llama Family
**Llama 4**
- `meta.llama4-scout-17b-instruct-v1:0` (multimodal)
- `meta.llama4-maverick-17b-instruct-v1:0` (multimodal)

**Llama 3.3**
- `meta.llama3-3-70b-instruct-v1:0`

**Llama 3.2**
- `meta.llama3-2-90b-instruct-v1:0` (multimodal)
- `meta.llama3-2-11b-instruct-v1:0` (multimodal)
- `meta.llama3-2-3b-instruct-v1:0`
- `meta.llama3-2-1b-instruct-v1:0`

**Llama 3.1**
- `meta.llama3-1-70b-instruct-v1:0`
- `meta.llama3-1-8b-instruct-v1:0`

**Llama 3**
- `meta.llama3-70b-instruct-v1:0`
- `meta.llama3-8b-instruct-v1:0`

### Mistral AI Family
- `mistral.pixtral-large-2502-v1:0` (multimodal)
- `mistral.mistral-large-2402-v1:0`
- `mistral.mistral-small-2402-v1:0`
- `mistral.mixtral-8x7b-instruct-v0:1`
- `mistral.mistral-7b-instruct-v0:2`

### Cohere Family
- `cohere.command-r-plus-v1:0`
- `cohere.command-r-v1:0`

### Other Providers
- `openai.gpt-oss-120b-1:0` (OpenAI)
- `openai.gpt-oss-20b-1:0` (OpenAI)
- `qwen.qwen3-32b-v1:0` (Qwen)
- `qwen.qwen3-coder-30b-a3b-v1:0` (Qwen - coding)
- `deepseek.r1-v1:0` (DeepSeek)
- `ai21.jamba-1-5-large-v1:0` (AI21 Labs)
- `ai21.jamba-1-5-mini-v1:0` (AI21 Labs)

## 🔍 List Models via CLI

### All Models
```bash
aws bedrock list-foundation-models --region us-east-1
```

### Text Generation Only
```bash
aws bedrock list-foundation-models --region us-east-1 --by-output-modality TEXT
```

### By Provider
```bash
aws bedrock list-foundation-models --region us-east-1 --by-provider Anthropic
aws bedrock list-foundation-models --region us-east-1 --by-provider Amazon
aws bedrock list-foundation-models --region us-east-1 --by-provider Meta
```

## 📝 Notes

- **Context Windows**: Models with suffixes like `:24k`, `:128k`, `:300k` indicate different context window sizes
- **Multimodal**: Models supporting images/video in addition to text
- **Cost**: Amazon Nova Micro is the most cost-effective option
- **Quality**: Anthropic Claude Opus 4 provides the highest quality
- **Speed**: Haiku models and Nova Micro are the fastest
- **Role Assumption**: You're currently set up to assume role with external ID


You're using the **most cost-effective** model (Nova Micro) with role assumption configured! 🎉

