import "@testing-library/jest-dom/vitest";
import { expect } from "vitest";
import * as matchers from "vitest-axe/matchers";

expect.extend(matchers);

// Type augmentation for vitest-axe (v0.1.0 extend-expect.js is empty)
declare module "vitest" {
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  interface Assertion {
    toHaveNoViolations(): void;
  }
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  interface AsymmetricMatchersContaining {
    toHaveNoViolations(): void;
  }
}
