import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ResultsPanel } from "@/components/ResultsPanel";

describe("ResultsPanel", () => {
  it("renders words, explanations, and evidence for every status", () => {
    render(
      <ResultsPanel
        result={{
          requestId: "req_test",
          overallStatus: "review",
          processingTimeMs: 1250,
          ocrProvider: "test",
          extractedText: "OLD TOM",
          warnings: ["Decision support only."],
          image: { width: 100, height: 100, format: "PNG" },
          stageTimingsMs: { imagePrepareMs: 1, ocrMs: 2, fieldExtractMs: 1, verificationMs: 1 },
          checks: [
            {
              field: "brandName",
              label: "Brand name",
              group: "Application checks",
              status: "pass",
              expected: "Old Tom",
              detected: "OLD TOM",
              confidence: 0.99,
              explanation: "Names match.",
            },
            {
              field: "warning",
              label: "Warning wording",
              group: "Label requirements",
              status: "review",
              explanation: "Review needed.",
            },
          ],
        }}
      />,
    );
    expect(screen.getByRole("heading", { name: "Verification complete" })).toBeInTheDocument();
    expect(screen.getByText("Pass")).toBeInTheDocument();
    expect(screen.getByText("Needs review", { selector: ".status-badge" })).toBeInTheDocument();
    expect(screen.getByText("Names match.")).toBeInTheDocument();
    expect(screen.getByText("Decision support only.")).toBeInTheDocument();
  });
});

