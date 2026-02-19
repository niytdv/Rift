"use client";

import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { GraphNode, GraphEdge } from "@/lib/types";

interface GraphVisualizationProps {
  accounts: GraphNode[];
  edges: GraphEdge[];
  onNodeClick: (nodeId: string) => void;
}

export default function GraphVisualization({ accounts, edges, onNodeClick }: GraphVisualizationProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !accounts.length) return;

    const width = 800;
    const height = 600;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    const simulation = d3.forceSimulation(accounts as any)
      .force("link", d3.forceLink(edges).id((d: any) => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("stroke", "#999")
      .attr("stroke-width", 2);

    const node = svg.append("g")
      .selectAll("circle")
      .data(accounts)
      .join("circle")
      .attr("r", 8)
      .attr("fill", (d) => d.suspicion_score > 50 ? "#ef4444" : "#3b82f6")
      .style("cursor", "pointer")
      .on("click", (_, d) => onNodeClick(d.id));

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node
        .attr("cx", (d: any) => d.x)
        .attr("cy", (d: any) => d.y);
    });
  }, [accounts, edges, onNodeClick]);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">Transaction Network Graph</h2>
      <svg ref={svgRef} className="border border-gray-200 rounded"></svg>
    </div>
  );
}
