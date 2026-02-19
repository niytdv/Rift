import { NextResponse } from "next/server";
import path from "path";
import { analyzeCsv } from "@/lib/pythonBridge";

export async function POST() {
  console.log("=== /api/sample POST called ===");
  try {
    const samplePath = path.join(process.cwd(), "public", "sample_data.csv");
    console.log("Sample CSV path:", samplePath);
    
    console.log("Calling Python detection engine...");
    const result = await analyzeCsv(samplePath);
    console.log("Python analysis completed successfully");
    console.log("Result summary:", result?.summary);

    // Serialize with custom float formatting
    let jsonString = JSON.stringify(result);
    
    // Replace numeric values with .1 decimal format for specific fields
    jsonString = jsonString.replace(/"(suspicion_score|risk_score|processing_time_seconds)":(\d+\.?\d*)([,\}])/g, (match, field, value, suffix) => {
      const num = parseFloat(value);
      return `"${field}":${num.toFixed(1)}${suffix}`;
    });

    console.log("Returning formatted JSON response");
    return new NextResponse(jsonString, {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error("=== SAMPLE ANALYSIS ERROR ===");
    console.error("Error type:", error?.constructor?.name);
    console.error("Error message:", error instanceof Error ? error.message : String(error));
    console.error("Full error:", error);
    console.error("Stack trace:", error instanceof Error ? error.stack : "No stack trace");
    
    return NextResponse.json(
      { 
        error: error instanceof Error ? error.message : "Sample analysis failed",
        details: error instanceof Error ? error.stack : String(error)
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  console.log("=== /api/sample GET called ===");
  try {
    const samplePath = path.join(process.cwd(), "public", "sample_data.csv");
    console.log("Sample CSV path:", samplePath);
    
    console.log("Calling Python detection engine...");
    const result = await analyzeCsv(samplePath);
    console.log("Python analysis completed successfully");

    // Serialize with custom float formatting
    let jsonString = JSON.stringify(result);
    
    // Replace numeric values with .1 decimal format for specific fields
    jsonString = jsonString.replace(/"(suspicion_score|risk_score|processing_time_seconds)":(\d+\.?\d*)([,\}])/g, (match, field, value, suffix) => {
      const num = parseFloat(value);
      return `"${field}":${num.toFixed(1)}${suffix}`;
    });

    console.log("Returning formatted JSON response");
    return new NextResponse(jsonString, {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error("=== SAMPLE ANALYSIS ERROR (GET) ===");
    console.error("Error type:", error?.constructor?.name);
    console.error("Error message:", error instanceof Error ? error.message : String(error));
    console.error("Full error:", error);
    console.error("Stack trace:", error instanceof Error ? error.stack : "No stack trace");
    
    return NextResponse.json(
      { 
        error: error instanceof Error ? error.message : "Sample analysis failed",
        details: error instanceof Error ? error.stack : String(error)
      },
      { status: 500 }
    );
  }
}
