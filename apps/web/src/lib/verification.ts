import type {
  ApplicationFormValues,
  VerificationCheck,
  VerificationResponse,
  VerificationStatus,
} from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

export const INITIAL_APPLICATION: ApplicationFormValues = {
  applicationId: "",
  beverageType: "distilled_spirits",
  brandName: "",
  classType: "",
  alcoholByVolume: "",
  netContentsValue: "",
  netContentsUnit: "mL",
};

export class VerificationRequestError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "VerificationRequestError";
  }
}

export function buildApplication(values: ApplicationFormValues) {
  return {
    applicationId: values.applicationId.trim() || undefined,
    beverageType: values.beverageType,
    brandName: values.brandName.trim(),
    classType: values.classType.trim(),
    alcoholByVolume: Number(values.alcoholByVolume),
    netContents: {
      value: Number(values.netContentsValue),
      unit: values.netContentsUnit,
    },
  };
}

export async function submitVerification(
  values: ApplicationFormValues,
  image: File,
): Promise<VerificationResponse> {
  const body = new FormData();
  body.set("application", JSON.stringify(buildApplication(values)));
  body.set("image", image);
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 15_000);
  try {
    const response = await fetch(`${API_URL}/api/v1/verify`, {
      method: "POST",
      body,
      signal: controller.signal,
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      const message = payload?.error?.message;
      throw new VerificationRequestError(
        typeof message === "string" ? message : "The label could not be processed. Try again.",
      );
    }
    return payload as VerificationResponse;
  } catch (error) {
    if (error instanceof VerificationRequestError) throw error;
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new VerificationRequestError("Processing took too long. Try again with a clearer image.");
    }
    throw new VerificationRequestError("The service could not be reached. Check the API and try again.");
  } finally {
    window.clearTimeout(timeout);
  }
}

export function summarizeChecks(checks: VerificationCheck[]) {
  return checks.reduce(
    (summary, check) => {
      summary[check.status] += 1;
      return summary;
    },
    { pass: 0, mismatch: 0, missing: 0, review: 0, not_applicable: 0 } satisfies Record<
      VerificationStatus,
      number
    >,
  );
}

export function formatDuration(milliseconds: number) {
  if (milliseconds < 1000) return `${milliseconds} ms`;
  return `${(milliseconds / 1000).toFixed(1)} seconds`;
}

export const STATUS_LABELS: Record<VerificationStatus, string> = {
  pass: "Pass",
  mismatch: "Mismatch",
  missing: "Missing",
  review: "Needs review",
  not_applicable: "Not evaluated",
};

