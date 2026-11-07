import { renderToStaticMarkup } from "react-dom/server";
import { expect, test } from "vitest";

import HomePage from "../app/page";

test("AC-2: home page renders the fair2fly heading", () => {
  const html = renderToStaticMarkup(<HomePage />);

  expect(html).toContain("<h1>fair2fly</h1>");
});
