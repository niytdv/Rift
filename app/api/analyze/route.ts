import { NextRequest, NextResponse } from "next/server";
import { writeFile } from "fs/promises";
import path from "path";
import { analyzeCsv } from "@/lib/pythonBridge";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get("file") as File;

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 });
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    const tmpPath = path.join(process.cwd(), "tmp", `upload-${Date.now()}.csv`);
    await writeFile(tmpPath, buffer);

    const result = await analyzeCsv(tmpPath);

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
    console.error("Analysis error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Analysis failed" },
      { status: 500 }
    );
  }
}
