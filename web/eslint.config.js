import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import tseslint from "typescript-eslint";
import { defineConfig, globalIgnores } from "eslint/config";
import simpleImportSort from "eslint-plugin-simple-import-sort";

export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],

    languageOptions: {
      globals: globals.browser,
    },

    plugins: {
      "simple-import-sort": simpleImportSort,
    },

    rules: {
      "simple-import-sort/imports": [
        "error",
        {
          groups: [
            // React and React type imports
            [
              "^react($|/)",
              "^react-dom($|/)",
              "^react\\u0000($|/)",
              "^react-dom\\u0000($|/)",
            ],

            // External packages
            ["^@?\\w"],

            // Absolute imports
            ["^@/"],

            // Relative imports
            ["^\\.(?!.*\\.(css|scss|sass)$)"],

            // Side effects
            ["^\\u0000"],

            // Styles
            ["^.+\\.(css|scss|sass)$"],
          ],
        },
      ],

      "simple-import-sort/exports": "error",
    },
  },
]);
