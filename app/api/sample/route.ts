import { NextResponse } from "next/server";
import path from "path";
import { analyzeCsv } from "@/lib/pythonBridge";

export async function POST() {
  try {
    const samplePath = path.join(process.cwd(), "public", "sample_data.csv");
    const result = await analyzeCsv(samplePath);

    // Serialize with custom float formatting
    let jsonString = JSON.stringify(result);
    
    // Replace numeric values with .1 decimal format for specific fields
    jsonString = jsonString.replace(/"(suspicion_score|risk_score|processing_time_seconds)":(\d+\.?\d*)([,\}])/g, (match, field, value, suffix) => {
      const num = parseFloat(value);
      return `"${field}":${num.toFixed(1)}${suffix}`;
    });

    return new NextResponse(jsonString, {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error("Sample analysis error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Sample analysis failed" },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    const samplePath = path.join(process.cwd(), "public", "sample_data.csv");
    const result = await analyzeCsv(samplePath);

    // Serialize with custom float formatting
    let jsonString = JSON.stringify(result);
    
    // Replace numeric values with .1 decimal format for specific fields
    jsonString = jsonString.replace(/"(suspicion_score|risk_score|processing_time_seconds)":(\d+\.?\d*)([,\}])/g, (match, field, value, suffix) => {
      const num = parseFloat(value);
      return `"${field}":${num.toFixed(1)}${suffix}`;
    });

    return new NextResponse(jsonString, {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error("Sample analysis error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Sample analysis failed" },
      { status: 500 }
    );
  }
}
