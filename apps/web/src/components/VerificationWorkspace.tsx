"use client";

import { useEffect, useState } from "react";
import type { FormEvent } from "react";

import { ApplicationForm } from "@/components/ApplicationForm";
import { ResultsPanel } from "@/components/ResultsPanel";
import { UploadPanel } from "@/components/UploadPanel";
import type { ApplicationFormValues, VerificationResponse } from "@/lib/types";
import {
  DEMO_APPLICATION,
  INITIAL_APPLICATION,
  submitVerification,
  VerificationRequestError,
} from "@/lib/verification";

type ProgressStage = "upload" | "ocr" | "compare";

export function VerificationWorkspace() {
  const [values, setValues] = useState<ApplicationFormValues>(INITIAL_APPLICATION);
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [result, setResult] = useState<VerificationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<ProgressStage | null>(null);
  const [activeField, setActiveField] = useState<string | null>(null);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  function handleFile(nextFile: File) {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setFile(nextFile);
    setPreviewUrl(URL.createObjectURL(nextFile));
    setError(null);
    setResult(null);
    setActiveField(null);
  }

  function loadDemo() {
    setValues(DEMO_APPLICATION);
    setError(null);
    setResult(null);
    setActiveField(null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      setError("Choose a label image before starting verification.");
      return;
    }
    setError(null);
    setResult(null);
    setProgress("upload");
    const ocrTimer = window.setTimeout(() => setProgress("ocr"), 250);
    try {
      const response = await submitVerification(values, file);
      setProgress("compare");
      setResult(response);
      setActiveField(response.checks.find((check) => check.boundingBox)?.field ?? null);
      window.setTimeout(() => {
        document.getElementById("verification-results")?.scrollIntoView({ behavior: "smooth" });
      }, 50);
    } catch (requestError) {
      setError(
        requestError instanceof VerificationRequestError
          ? requestError.message
          : "The label could not be processed. Try again.",
      );
    } finally {
      window.clearTimeout(ocrTimer);
      setProgress(null);
    }
  }

  const busy = progress !== null;
  const evidence = result?.checks.find((check) => check.field === activeField) ?? null;

  return (
    <>
      <header className="site-header">
        <div className="header-inner">
          <div className="brand-lockup">
            <span className="brand-mark" aria-hidden="true">LG</span>
            <span>
              <span className="brand-name">LabelGuard AI</span>
              <span className="brand-subtitle">Compliance decision support</span>
            </span>
          </div>
          <span className="header-note">Prototype · U.S. alcohol label verification</span>
        </div>
      </header>
      <main className="main-shell">
        <section className="hero">
          <p className="eyebrow">Alcohol label verification</p>
          <h1>Compare label artwork with application data.</h1>
          <p className="hero-copy">
            Enter expected values, upload one label image, and review clear, evidence-backed checks.
          </p>
        </section>
        <form className="workflow-grid" onSubmit={handleSubmit}>
          <ApplicationForm
            values={values}
            disabled={busy}
            onChange={setValues}
            onLoadDemo={loadDemo}
          />
          <UploadPanel
            file={file}
            previewUrl={previewUrl}
            disabled={busy}
            evidence={evidence}
            imageDimensions={result?.image ?? null}
            onFile={handleFile}
            onError={setError}
          />
          {error && <div className="error-banner" role="alert">{error}</div>}
          {progress && (
            <div className="progress-panel" role="status" aria-label="Verification progress">
              <div className="progress-step complete">1. Uploading label</div>
              <div className={`progress-step ${progress !== "upload" ? "active" : ""}`}>2. Reading label</div>
              <div className={`progress-step ${progress === "compare" ? "active" : ""}`}>3. Comparing fields</div>
            </div>
          )}
          <div className="action-bar">
            <div className="action-copy">
              <strong>Step 3 · Verify label</strong>
              <span>Automated checks support—not replace—human review.</span>
            </div>
            <button className="primary-button" type="submit" disabled={busy || !file}>
              {busy ? "Verifying…" : "Verify Label"}
            </button>
          </div>
        </form>
        {result && (
          <ResultsPanel
            result={result}
            activeField={activeField}
            onSelectCheck={(check) => {
              setActiveField(check.field);
              document.getElementById("upload-heading")?.scrollIntoView({ behavior: "smooth" });
            }}
          />
        )}
        <footer className="page-footer">
          LabelGuard AI is a prototype decision-support tool. It does not approve or reject COLA applications.
        </footer>
      </main>
    </>
  );
}
