import type { VerificationCheck, VerificationResponse } from "@/lib/types";
import { formatDuration, STATUS_LABELS, summarizeChecks } from "@/lib/verification";

interface ResultsPanelProps {
  result: VerificationResponse;
}

function CheckCard({ check }: { check: VerificationCheck }) {
  return (
    <div className="check-card">
      <div className={`check-title status-${check.status}`}>
        <span className="status-dot" aria-hidden="true" />
        <span>{check.label}</span>
      </div>
      <div className="check-values">
        {check.expected && (
          <span><strong>Expected</strong> {check.expected}</span>
        )}
        {check.detected && (
          <span><strong>Detected</strong> {check.detected}</span>
        )}
        {typeof check.confidence === "number" && (
          <span><strong>OCR confidence</strong> {Math.round(check.confidence * 100)}%</span>
        )}
      </div>
      <span className={`status-badge status-${check.status}`}>{STATUS_LABELS[check.status]}</span>
      <p className="check-explanation">{check.explanation}</p>
    </div>
  );
}

export function ResultsPanel({ result }: ResultsPanelProps) {
  const summary = summarizeChecks(result.checks);
  const groups = Array.from(new Set(result.checks.map((check) => check.group)));
  const issueCount = summary.mismatch + summary.missing;
  const summaryText = [
    `${summary.pass} passed`,
    issueCount ? `${issueCount} mismatched or missing` : null,
    summary.review ? `${summary.review} needs review` : null,
  ].filter(Boolean).join(" · ");

  return (
    <section className="results-section" id="verification-results" aria-live="polite">
      <div className="result-summary">
        <div>
          <p className="step-kicker">Verification result</p>
          <h2>Verification complete</h2>
          <p>{summaryText} · Processed in {formatDuration(result.processingTimeMs)}</p>
        </div>
        <span className={`overall-pill status-${result.overallStatus}`}>
          {STATUS_LABELS[result.overallStatus]}
        </span>
      </div>
      <div className="results-body">
        {groups.map((group) => (
          <div className="result-group" key={group}>
            <h3>{group}</h3>
            <div className="check-list">
              {result.checks.filter((check) => check.group === group).map((check) => (
                <CheckCard check={check} key={check.field} />
              ))}
            </div>
          </div>
        ))}
        <ul className="result-warnings">
          {result.warnings.map((warning) => <li key={warning}>{warning}</li>)}
        </ul>
        <details className="evidence-disclosure">
          <summary>View extracted OCR text</summary>
          <pre className="evidence-text">{result.extractedText || "No readable text detected."}</pre>
        </details>
      </div>
    </section>
  );
}

