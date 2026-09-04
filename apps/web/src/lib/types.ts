export type VerificationStatus =
  | "pass"
  | "mismatch"
  | "missing"
  | "review"
  | "not_applicable";

export type VolumeUnit = "mL" | "L" | "fl_oz";

export interface ApplicationFormValues {
  applicationId: string;
  beverageType: "distilled_spirits" | "wine" | "malt_beverage";
  brandName: string;
  classType: string;
  alcoholByVolume: string;
  netContentsValue: string;
  netContentsUnit: VolumeUnit;
}

export interface Point {
  x: number;
  y: number;
}

export interface BoundingBox {
  points: Point[];
}

export interface VerificationCheck {
  field: string;
  label: string;
  group: string;
  status: VerificationStatus;
  expected?: string;
  detected?: string;
  confidence?: number;
  explanation: string;
  boundingBox?: BoundingBox;
}

export interface VerificationResponse {
  requestId: string;
  overallStatus: VerificationStatus;
  processingTimeMs: number;
  checks: VerificationCheck[];
  warnings: string[];
  extractedText: string;
  ocrProvider: string;
  image: { width: number; height: number; format: string };
  stageTimingsMs: {
    imagePrepareMs: number;
    ocrMs: number;
    fieldExtractMs: number;
    verificationMs: number;
  };
}

