import { expect, test } from './test';
import { expectNoAccessibilityViolations } from './accessibility';

test('homepage loads without automatic accessibility violations', async ({ page }) => {
  const response = await page.goto('/', { waitUntil: 'networkidle' });
  expect(response?.ok()).toBeTruthy();
  await expectNoAccessibilityViolations(page, {
    disabledRules: ['page-has-heading-one', 'landmark-one-main'],
  });
});
