OPENAI_API_KEY="YOURE_API_KEY_HERE"
ANTHROPIC_API_KEY="YOURE_API_KEY_HERE"


AWS_REGION='us-east-1'  # Or your preferred region
LLM_PROVIDER='bedrock' # openai, anthropic, bedrock

BEDROCK_MODEL_ID='amazon.nova-micro-v1:0:128k'


# Option 2: Assume Role (with external ID support)
# Uncomment and fill in to assume a role instead of using direct credentials
AWS_ROLE_ARN='AWS_ROLE_ARN_HERE'
AWS_EXTERNAL_ID='AWS_EXTERNAL_ID_HERE'  # Required if role trust policy specifies ExternalId
# AWS_ROLE_SESSION_NAME='weather-app-session'  # Optional, defaults to 'weather-app-session'