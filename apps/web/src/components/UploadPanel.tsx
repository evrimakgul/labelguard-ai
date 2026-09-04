"use client";

import Image from "next/image";
import { useRef, useState } from "react";

interface UploadPanelProps {
  file: File | null;
  previewUrl: string | null;
  disabled: boolean;
  onFile: (file: File) => void;
  onError: (message: string) => void;
}

const ALLOWED_TYPES = new Set(["image/jpeg", "image/png"]);
const MAX_BYTES = 10 * 1024 * 1024;

export function UploadPanel({
  file,
  previewUrl,
  disabled,
  onFile,
  onError,
}: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function selectFile(candidate?: File) {
    if (!candidate) return;
    if (!ALLOWED_TYPES.has(candidate.type)) {
      onError("We could not read this file. Upload a JPEG or PNG image.");
      return;
    }
    if (candidate.size > MAX_BYTES) {
      onError("The image is too large. The maximum size is 10 MB.");
      return;
    }
    onFile(candidate);
  }

  return (
    <section className="panel" aria-labelledby="upload-heading">
      <div className="panel-heading">
        <div>
          <p className="step-kicker">Step 2</p>
          <h2 id="upload-heading">Upload label artwork</h2>
          <p className="panel-description">Use a clear, well-lit view of the complete label.</p>
        </div>
      </div>
      <div
        className={`drop-zone${dragging ? " dragging" : ""}${previewUrl ? " has-preview" : ""}`}
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-label={file ? `Replace ${file.name}` : "Choose a label image"}
        onClick={() => !disabled && inputRef.current?.click()}
        onKeyDown={(event) => {
          if (!disabled && (event.key === "Enter" || event.key === " ")) {
            event.preventDefault();
            inputRef.current?.click();
          }
        }}
        onDragEnter={(event) => {
          event.preventDefault();
          if (!disabled) setDragging(true);
        }}
        onDragOver={(event) => event.preventDefault()}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          if (!disabled) selectFile(event.dataTransfer.files[0]);
        }}
      >
        {previewUrl ? (
          <>
            <Image
              className="preview-image"
              src={previewUrl}
              alt="Selected label preview"
              fill
              sizes="(max-width: 820px) 100vw, 42vw"
              unoptimized
            />
            <div className="preview-overlay">
              <strong>{file?.name}</strong>
              <span>Click or drop another image to replace</span>
            </div>
          </>
        ) : (
          <div>
            <div className="upload-icon" aria-hidden="true">↑</div>
            <strong>Drop label image here</strong>
            <span>or choose an image · JPEG or PNG · up to 10 MB</span>
          </div>
        )}
        <input
          ref={inputRef}
          className="hidden-input"
          type="file"
          accept="image/jpeg,image/png"
          disabled={disabled}
          onChange={(event) => selectFile(event.target.files?.[0])}
        />
      </div>
      <p className="privacy-note">
        <span aria-hidden="true">◆</span>
        Images are processed in memory and are not retained by LabelGuard AI.
      </p>
    </section>
  );
}

