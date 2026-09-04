import type { ApplicationFormValues } from "@/lib/types";

interface ApplicationFormProps {
  values: ApplicationFormValues;
  disabled: boolean;
  onChange: (values: ApplicationFormValues) => void;
  onLoadDemo: () => void;
}

export function ApplicationForm({
  values,
  disabled,
  onChange,
  onLoadDemo,
}: ApplicationFormProps) {
  function update<Key extends keyof ApplicationFormValues>(
    key: Key,
    value: ApplicationFormValues[Key],
  ) {
    onChange({ ...values, [key]: value });
  }

  return (
    <section className="panel" aria-labelledby="application-heading">
      <div className="panel-heading">
        <div>
          <p className="step-kicker">Step 1</p>
          <h2 id="application-heading">Application details</h2>
          <p className="panel-description">Enter the values the label should contain.</p>
        </div>
        <button className="secondary-button" type="button" onClick={onLoadDemo} disabled={disabled}>
          Load demo application
        </button>
      </div>
      <div className="field-grid">
        <div className="field">
          <label htmlFor="application-id">Application ID (optional)</label>
          <input
            id="application-id"
            value={values.applicationId}
            onChange={(event) => update("applicationId", event.target.value)}
            placeholder="COLA-001"
            disabled={disabled}
            maxLength={100}
          />
        </div>
        <div className="field">
          <label htmlFor="beverage-type">Beverage type</label>
          <select
            id="beverage-type"
            value={values.beverageType}
            onChange={(event) =>
              update("beverageType", event.target.value as ApplicationFormValues["beverageType"])
            }
            disabled={disabled}
          >
            <option value="distilled_spirits">Distilled spirits</option>
            <option value="wine">Wine</option>
            <option value="malt_beverage">Malt beverage</option>
          </select>
        </div>
        <div className="field field-full">
          <label htmlFor="brand-name">Brand name</label>
          <input
            id="brand-name"
            value={values.brandName}
            onChange={(event) => update("brandName", event.target.value)}
            placeholder="OLD TOM DISTILLERY"
            disabled={disabled}
            required
            maxLength={200}
          />
        </div>
        <div className="field field-full">
          <label htmlFor="class-type">Class / type</label>
          <input
            id="class-type"
            value={values.classType}
            onChange={(event) => update("classType", event.target.value)}
            placeholder="Kentucky Straight Bourbon Whiskey"
            disabled={disabled}
            required
            maxLength={200}
          />
        </div>
        <div className="field">
          <label htmlFor="abv">Alcohol by volume (%)</label>
          <input
            id="abv"
            type="number"
            min="0.1"
            max="100"
            step="0.1"
            inputMode="decimal"
            value={values.alcoholByVolume}
            onChange={(event) => update("alcoholByVolume", event.target.value)}
            placeholder="45"
            disabled={disabled}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="net-contents">Net contents</label>
          <div className="input-pair">
            <input
              id="net-contents"
              type="number"
              min="0.01"
              step="0.01"
              inputMode="decimal"
              value={values.netContentsValue}
              onChange={(event) => update("netContentsValue", event.target.value)}
              placeholder="750"
              disabled={disabled}
              required
            />
            <select
              aria-label="Net contents unit"
              value={values.netContentsUnit}
              onChange={(event) =>
                update("netContentsUnit", event.target.value as ApplicationFormValues["netContentsUnit"])
              }
              disabled={disabled}
            >
              <option value="mL">mL</option>
              <option value="L">L</option>
              <option value="fl_oz">fl oz</option>
            </select>
          </div>
        </div>
      </div>
    </section>
  );
}
