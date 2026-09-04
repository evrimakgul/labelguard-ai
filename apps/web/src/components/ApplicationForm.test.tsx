import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { ApplicationForm } from "@/components/ApplicationForm";
import { INITIAL_APPLICATION } from "@/lib/verification";


describe("ApplicationForm", () => {
  it("exposes the demo loader as a normal button", async () => {
    const onLoadDemo = vi.fn();
    const user = userEvent.setup();
    render(
      <ApplicationForm
        values={INITIAL_APPLICATION}
        disabled={false}
        onChange={vi.fn()}
        onLoadDemo={onLoadDemo}
      />,
    );

    await user.click(screen.getByRole("button", { name: "Load demo application" }));
    expect(onLoadDemo).toHaveBeenCalledOnce();
  });
});
