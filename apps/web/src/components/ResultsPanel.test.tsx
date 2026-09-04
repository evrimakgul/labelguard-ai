import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { ResultsPanel } from "@/components/ResultsPanel";

describe("ResultsPanel", () => {
  it("renders words, explanations, and selectable evidence for every status", async () => {
    const onSelectCheck = vi.fn();
    const user = userEvent.setup();
    render(
      <ResultsPanel
        activeField="brandName"
        onSelectCheck={onSelectCheck}
        result={{
          requestId: "req_test",
          overallStatus: "review",
          processingTimeMs: 1250,
          ocrProvider: "test",
          extractedText: "OLD TOM",
          warnings: ["Decision support only."],
          image: {
            width: 100,
            height: 100,
            format: "PNG",
            processingSteps: ["metadata_removed"],
          },
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
              boundingBox: {
                points: [
                  { x: 1, y: 1 },
                  { x: 20, y: 1 },
                  { x: 20, y: 10 },
                  { x: 1, y: 10 },
                ],
              },
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
    const evidenceButton = screen.getByRole("button", { name: /Brand name/ });
    expect(evidenceButton).toHaveAttribute("aria-pressed", "true");
    await user.click(evidenceButton);
    expect(onSelectCheck).toHaveBeenCalledWith(expect.objectContaining({ field: "brandName" }));
  });

  it("handles responses created before processing steps were added", async () => {
    const user = userEvent.setup();
    render(
      <ResultsPanel
        activeField={null}
        onSelectCheck={vi.fn()}
        result={{
          requestId: "req_legacy",
          overallStatus: "review",
          processingTimeMs: 5,
          ocrProvider: "test",
          extractedText: "",
          warnings: [],
          image: { width: 100, height: 100, format: "PNG" },
          stageTimingsMs: {
            imagePrepareMs: 1,
            ocrMs: 1,
            fieldExtractMs: 1,
            verificationMs: 1,
          },
          checks: [],
        }}
      />,
    );

    await user.click(screen.getByText("View processing details"));
    expect(screen.getByText("None")).toBeInTheDocument();
  });
});
