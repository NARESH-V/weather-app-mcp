# ------------------------------------------------------------------------------------------------
#  Provider Configuration
# ------------------------------------------------------------------------------------------------
LLM_PROVIDER='bedrock' # openai, anthropic, bedrock


# ------------------------------------------------------------------------------------------------
#  Provider Specific Configuration
# ------------------------------------------------------------------------------------------------
OPENAI_API_KEY="YOURE_API_KEY_HERE"
ANTHROPIC_API_KEY="YOURE_API_KEY_HERE"
BEDROCK_MODEL_ID='claude_3_5_sonnet_v2'  # Claude 3.5 Sonnet v2


# ------------------------------------------------------------------------------------------------
#  AWS Region Configuration
# ------------------------------------------------------------------------------------------------
AWS_REGION='us-east-1'  # Or your preferred region


# ------------------------------------------------------------------------------------------------
#  Assume Role Configuration
# ------------------------------------------------------------------------------------------------
AWS_ROLE_ARN='<YOUR_ROLE_ARN>'
AWS_EXTERNAL_ID='<YOUR_EXTERNAL_ID>'
AWS_ROLE_SESSION_NAME='weather-app'  # Optional, defaults to 'weather-app-session'