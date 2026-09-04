import { describe, expect, it } from "vitest";

import { buildApplication, formatDuration, summarizeChecks } from "@/lib/verification";

describe("verification helpers", () => {
  it("builds the API application shape", () => {
    expect(
      buildApplication({
        applicationId: "  COLA-001 ",
        beverageType: "distilled_spirits",
        brandName: " Old Tom ",
        classType: " Bourbon ",
        alcoholByVolume: "45",
        netContentsValue: "750",
        netContentsUnit: "mL",
      }),
    ).toEqual({
      applicationId: "COLA-001",
      beverageType: "distilled_spirits",
      brandName: "Old Tom",
      classType: "Bourbon",
      alcoholByVolume: 45,
      netContents: { value: 750, unit: "mL" },
    });
  });

  it("summarizes each result status", () => {
    const checks = ["pass", "pass", "review", "missing"].map((status, index) => ({
      field: String(index),
      label: String(index),
      group: "Test",
      status: status as "pass" | "review" | "missing",
      explanation: "test",
    }));
    expect(summarizeChecks(checks)).toMatchObject({ pass: 2, review: 1, missing: 1 });
  });

  it("formats sub-second and second durations", () => {
    expect(formatDuration(418)).toBe("418 ms");
    expect(formatDuration(2840)).toBe("2.8 seconds");
  });
});

