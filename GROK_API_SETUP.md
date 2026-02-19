# Grok API Integration Setup

The AI Chatbot Panel is now integrated with Grok (xAI) API for real-time fraud investigation assistance.

## Setup Instructions

### 1. Get Your Grok API Key

1. Visit [xAI Console](https://console.x.ai/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key

### 2. Configure Environment Variables

1. Create a `.env.local` file in the `Rift` directory:
   ```bash
   cp .env.local.example .env.local
   ```

2. Open `.env.local` and add your API key:
   ```
   XAI_API_KEY=your_actual_api_key_here
   ```

### 3. Restart the Development Server

```bash
npm run dev
```

## Features

- **Real-time AI Responses**: Powered by Grok's `grok-beta` model
- **Conversation History**: Maintains context from the last 10 messages
- **AML Expert System Prompt**: Configured as an Anti-Money Laundering Lead analyst
- **Loading States**: Visual feedback while AI is processing
- **Error Handling**: Graceful fallback if API is unavailable

## API Endpoint

- **Route**: `/api/chat`
- **Method**: POST
- **Body**:
  ```json
  {
    "message": "Your question here",
    "conversationHistory": [
      { "role": "user", "content": "Previous message" },
      { "role": "assistant", "content": "Previous response" }
    ]
  }
  ```

## Usage

1. Navigate to the dashboard: `http://localhost:3000/dashboard`
2. Use the AI Chatbot Panel on the right side
3. Ask questions about:
   - Fraud patterns and suspicious activities
   - Risk score explanations
   - Transaction analysis
   - Fraud ring investigations

## Troubleshooting

- **"API key not configured" error**: Make sure `.env.local` exists with `XAI_API_KEY`
- **Connection errors**: Check your internet connection and API key validity
- **Slow responses**: Grok API may take a few seconds to respond during high load

## Model Configuration

- **Model**: `grok-beta`
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 500 (concise responses)
