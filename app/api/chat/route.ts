import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const { message, conversationHistory } = await request.json();

    if (!message) {
      return NextResponse.json({ error: "No message provided" }, { status: 400 });
    }

    // Get Grok API key from environment variable
    const apiKey = process.env.XAI_API_KEY;
    
    if (!apiKey) {
      return NextResponse.json(
        { error: "Grok API key not configured" },
        { status: 500 }
      );
    }

    // Prepare messages for Grok API
    const messages = [
      {
        role: "system",
        content: "You are an expert AI AML (Anti-Money Laundering) Lead analyst. You help investigate fraud patterns, explain risk scores, analyze suspicious transactions, and provide insights on fraud rings. Be concise, professional, and focus on actionable insights."
      },
      ...(conversationHistory || []),
      {
        role: "user",
        content: message
      }
    ];

    // Call Grok API (xAI)
    const response = await fetch("https://api.x.ai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: "grok-beta",
        messages: messages,
        temperature: 0.7,
        max_tokens: 500
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Grok API error:", errorData);
      return NextResponse.json(
        { error: "Failed to get response from Grok API" },
        { status: response.status }
      );
    }

    const data = await response.json();
    const aiResponse = data.choices[0]?.message?.content || "I apologize, but I couldn't generate a response.";

    return NextResponse.json({ response: aiResponse });
  } catch (error) {
    console.error("Chat API error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Internal server error" },
      { status: 500 }
    );
  }
}
