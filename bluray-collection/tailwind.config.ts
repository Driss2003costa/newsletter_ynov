import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0a0c11",
        panel: "#151922",
        panel2: "#1c212c",
        cream: "#f4f4f6",
        muted: "#9aa0ad",
        line: "#252b37",
        blu: "#3b82f6",
        gold: "#eab308",
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "-apple-system", "Segoe UI", "Roboto", "Helvetica", "Arial", "sans-serif"],
      },
      boxShadow: {
        poster: "0 10px 30px -10px rgba(0,0,0,0.7)",
        glow: "0 0 0 1px rgba(59,130,246,0.5), 0 0 25px -5px rgba(59,130,246,0.4)",
      },
    },
  },
  plugins: [],
};

export default config;
