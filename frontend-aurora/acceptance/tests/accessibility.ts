import AxeBuilder from '@axe-core/playwright';
import { expect, type Page } from '@playwright/test';
import type { RunOptions, SerialFrameSelector } from 'axe-core';

type AccessibilityCheckOptions = {
  include?: SerialFrameSelector[];
  exclude?: SerialFrameSelector[];
  axeOptions?: RunOptions;
  disabledRules?: string[];
};

export async function expectNoAccessibilityViolations(
  page: Page,
  options: AccessibilityCheckOptions = {},
) {
  const builder = new AxeBuilder({ page });
  for (const selector of options.include ?? []) builder.include(selector);
  for (const selector of options.exclude ?? []) builder.exclude(selector);
  if (options.axeOptions) builder.options(options.axeOptions);
  if (options.disabledRules?.length) builder.disableRules(options.disabledRules);

  const { violations } = await builder.analyze();
  expect(
    violations.map(({ id, impact, description, help, nodes }) => ({
      id,
      impact,
      description,
      help,
      nodes: nodes.map(({ target, failureSummary }) => ({ target, failureSummary })),
    })),
  ).toEqual([]);
}
