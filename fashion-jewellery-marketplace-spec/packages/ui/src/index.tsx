import type { ButtonHTMLAttributes } from "react";

/** Scaffold button. The design-system library (module 01) replaces this with the full set. */
export function Button(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className="auralis-button" {...props} />;
}
