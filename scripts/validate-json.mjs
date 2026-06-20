#!/usr/bin/env node
/**
 * CLI validator for JSON/JSONL files against project JSON schemas.
 *
 * Usage:
 *   node scripts/validate-json.mjs --schema <name> --input <file>
 *   node scripts/validate-json.mjs --schema research-plan --input plan.json
 *   node scripts/validate-json.mjs --schema evidence --input records.jsonl
 *
 * Exit codes:
 *   0   All records valid.
 *   1   One or more validation errors.
 *   2   File not found or missing / invalid arguments.
 *   3   Parse or internal error (corrupted file, bad schema).
 *
 * Built-in modules only: fs, path, url.  No npm dependencies.
 */

import { readFileSync, existsSync } from "fs";
import { resolve, dirname, extname, basename } from "path";
import { fileURLToPath } from "url";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(SCRIPT_DIR, "..");
const SCHEMA_DIR = resolve(PROJECT_ROOT, "schemas");

function logError(...args) {
  console.error(...args);
}

function usage(exitCode = 0) {
  const lines = [
    `Usage: node ${basename(process.argv[1])} --schema <name> --input <file> [--format json|jsonl]`,
    "",
    "Validate a JSON or JSONL file against schemas/<name>.schema.json.",
    "",
    "Arguments:",
    "  --schema <name>   Schema name (e.g. research-plan, evidence, claim-review, audit)",
    "  --input <file>    Path to JSON or JSONL input file",
    "  --format <fmt>    Input format: json or jsonl (default: auto-detect from extension)",
    "  --help            Show this message",
    "",
    "Exit codes:",
    "  0  All records valid",
    "  1  Validation error(s)",
    "  2  File / argument error",
    "  3  Parse or internal error",
  ];
  console.log(lines.join("\n"));
  // eslint-disable-next-line n/no-process-exit
  process.exit(exitCode);
}

// ---------------------------------------------------------------------------
// Schema loader with $ref resolution for _defs.json
// ---------------------------------------------------------------------------

/**
 * Load a JSON Schema file and resolve `$ref` references to `_defs.json`.
 *
 * @param {string} schemaName  — e.g. "research-plan"
 * @returns {{ schema: object, defs: object }}
 */
function loadSchema(schemaName) {
  const schemaPath = resolve(SCHEMA_DIR, `${schemaName}.schema.json`);
  const defsPath = resolve(SCHEMA_DIR, "_defs.json");

  if (!existsSync(schemaPath)) {
    logError(`Schema not found: ${schemaPath}`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(2);
  }

  let schema, defs;
  try {
    schema = JSON.parse(readFileSync(schemaPath, "utf-8"));
  } catch (err) {
    logError(`Failed to parse schema file: ${schemaPath} — ${err.message}`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(3);
  }

  try {
    defs = JSON.parse(readFileSync(defsPath, "utf-8"));
  } catch (err) {
    logError(`Failed to parse shared definitions: ${defsPath} — ${err.message}`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(3);
  }

  return { schema, defs };
}

/**
 * Inline-resolve `$ref` nodes that point to `_defs.json#/definitions/<key>`.
 * Mutates the schema tree in place.
 *
 * @param {object} node  — schema fragment (mutated)
 * @param {object} defs  — parsed _defs.json content
 */
function resolveRefs(node, defs) {
  if (!node || typeof node !== "object") return;
  if (Array.isArray(node)) {
    for (const item of node) resolveRefs(item, defs);
    return;
  }

  // If this node is a $ref, inline the referenced definition
  if (node.$ref && typeof node.$ref === "string") {
    const ref = node.$ref;
    const match = ref.match(/^_defs\.json#\/definitions\/(\w+)$/);
    if (match) {
      const key = match[1];
      if (defs.definitions && defs.definitions[key]) {
        // Copy properties from the referenced definition into this node
        const resolved = JSON.parse(JSON.stringify(defs.definitions[key]));
        Object.keys(node).forEach((k) => delete node[k]);
        Object.assign(node, resolved);
        // $ref is resolved; clear it to avoid re-processing
        // but we keep the resolved structure
        delete node.$ref;
      }
    }
    // If $ref couldn't be resolved, keep it but leave it dangling
    return;
  }

  for (const key of Object.keys(node)) {
    // Skip non-schema properties at the top level
    if (key.startsWith("$")) continue;
    resolveRefs(node[key], defs);
  }
}

// ---------------------------------------------------------------------------
// Validator
// ---------------------------------------------------------------------------

/**
 * Validate a data value against a resolved schema node.
 *
 * @param {*}       data      — the value to check
 * @param {object}  sch       — resolved schema node (type, properties, items, enum, …)
 * @param {string}  path      — dot-path prefix for error reporting (e.g. "root.products")
 * @param {Array}   errors    — accumulator: { field: string, message: string }[]
 */
function validateNode(data, sch, path, errors) {
  if (!sch || typeof sch !== "object") return;

  // ---- $ref (unresolved — skip) -------------------------------------------
  if (sch.$ref) {
    // Could not resolve this $ref — skip validation for this branch
    return;
  }

  // ---- type check ----------------------------------------------------------
  const expectedType = sch.type;
  if (expectedType) {
    const actualType = getActualType(data);
    if (actualType !== expectedType) {
      // Special case: schema says "number" but data is a numeric string — still flag it
      // Some schemas may have integer type; check for that too
      if (!(expectedType === "number" && actualType === "integer")) {
        errors.push({
          field: path || "(root)",
          message: `Expected type "${expectedType}" but got "${actualType}"`,
        });
        return; // Don't validate further if type is wrong
      }
    }
  }

  // ---- enum check (strings only for our schemas) ---------------------------
  if (sch.enum && Array.isArray(sch.enum)) {
    // Coerce data to string for comparison, as enums in schemas are strings
    if (!sch.enum.includes(data)) {
      errors.push({
        field: path || "(root)",
        message: `Value "${data}" is not one of the allowed values: [${sch.enum
          .map((v) => `"${v}"`)
          .join(", ")}]`,
      });
    }
  }

  // ---- pattern check on strings --------------------------------------------
  if (sch.pattern && typeof data === "string") {
    const re = new RegExp(sch.pattern);
    if (!re.test(data)) {
      errors.push({
        field: path || "(root)",
        message: `String "${data}" does not match required pattern ${sch.pattern}`,
      });
    }
  }

  // ---- required fields (object) --------------------------------------------
  if (expectedType === "object" && typeof data === "object" && !Array.isArray(data) && data !== null) {
    if (Array.isArray(sch.required)) {
      for (const field of sch.required) {
        if (!(field in data)) {
          errors.push({
            field: path ? `${path}.${field}` : field,
            message: `Missing required field "${field}"`,
          });
        }
      }
    }

    // ---- nested properties --------------------------------------------------
    if (sch.properties && typeof sch.properties === "object") {
      for (const [propName, propSchema] of Object.entries(sch.properties)) {
        if (propName in data) {
          const childPath = path ? `${path}.${propName}` : propName;
          validateNode(data[propName], propSchema, childPath, errors);
        }
      }
    }
  }

  // ---- array checks --------------------------------------------------------
  if (expectedType === "array" && Array.isArray(data)) {
    if (typeof sch.minItems === "number" && data.length < sch.minItems) {
      errors.push({
        field: path || "(root)",
        message: `Array has ${data.length} item(s), minimum required is ${sch.minItems}`,
      });
    }

    if (sch.items && typeof sch.items === "object") {
      for (let i = 0; i < data.length; i++) {
        const itemPath = path ? `${path}[${i}]` : `[${i}]`;
        validateNode(data[i], sch.items, itemPath, errors);
      }
    }
  }
}

/**
 * Get the JSON Schema type string for a JavaScript value.
 */
function getActualType(value) {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  if (typeof value === "number") {
    return Number.isInteger(value) ? "integer" : "number";
  }
  return typeof value; // "string", "boolean", "object", etc.
}

// ---------------------------------------------------------------------------
// Input reader
// ---------------------------------------------------------------------------

/**
 * Read and parse an input file as either JSON or JSONL.
 *
 * @param {string} filePath
 * @param {"json"|"jsonl"|null} format  — if null, auto-detect from extension
 * @returns {{ records: any[], format: string, rawLines?: string[] }}
 */
function readInput(filePath, format) {
  if (!existsSync(filePath)) {
    logError(`File not found: ${filePath}`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(2);
  }

  // Determine format
  const ext = extname(filePath).toLowerCase();
  const fmt = format || (ext === ".jsonl" ? "jsonl" : "json");

  let content;
  try {
    content = readFileSync(filePath, "utf-8");
  } catch (err) {
    logError(`Failed to read file: ${filePath} — ${err.message}`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(2);
  }

  if (fmt === "jsonl") {
    return parseJSONL(content, filePath);
  } else if (fmt === "json") {
    return parseJSON(content, filePath);
  } else {
    logError(`Unknown format: "${fmt}". Use "json" or "jsonl".`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(2);
  }
}

function parseJSON(content, filePath) {
  try {
    const records = [JSON.parse(content)];
    return { records, format: "json" };
  } catch (err) {
    logError(`Invalid JSON in ${filePath}: ${err.message}`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(3);
  }
}

function parseJSONL(content, filePath) {
  const lines = content.split(/\r?\n/).filter((line) => line.trim() !== "");
  const records = [];
  for (let i = 0; i < lines.length; i++) {
    try {
      records.push(JSON.parse(lines[i]));
    } catch (err) {
      logError(`Invalid JSON on line ${i + 1} of ${filePath}: ${err.message}`);
      // eslint-disable-next-line n/no-process-exit
      process.exit(3);
    }
  }
  return { records, format: "jsonl" };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);

  // ---- Parse CLI -----------------------------------------------------------
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    usage(0);
  }

  let schemaName = null;
  let inputPath = null;
  let format = null;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--schema":
        schemaName = args[++i];
        break;
      case "--input":
        inputPath = args[++i];
        break;
      case "--format":
        format = args[++i];
        break;
      default:
        logError(`Unknown argument: ${args[i]}`);
        usage(2);
    }
  }

  // Validate required args
  if (!schemaName) {
    logError("Missing required argument: --schema <name>");
    usage(2);
  }
  if (!inputPath) {
    logError("Missing required argument: --input <file>");
    usage(2);
  }
  if (format && format !== "json" && format !== "jsonl") {
    logError(`Invalid format "${format}". Use "json" or "jsonl".`);
    // eslint-disable-next-line n/no-process-exit
    process.exit(2);
  }

  // ---- Load schema ---------------------------------------------------------
  const { schema, defs } = loadSchema(schemaName);
  resolveRefs(schema, defs);

  // ---- Read input ----------------------------------------------------------
  const { records } = readInput(inputPath, format);

  // ---- Validate ------------------------------------------------------------
  const errors = [];
  for (let i = 0; i < records.length; i++) {
    const record = records[i];
    const recordLabel = records.length === 1 ? "(root)" : `Line ${i + 1}`;
    validateNode(record, schema, recordLabel, errors);
  }

  // ---- Report --------------------------------------------------------------
  if (errors.length > 0) {
    logError(`FAIL: ${errors.length} validation error(s)`);
    for (const err of errors) {
      logError(`  ${err.field}: ${err.message}`);
    }
    return 1;
  }

  const countLabel = records.length === 1 ? "1 record" : `${records.length} records`;
  console.error(`PASS: ${countLabel} validated against "${schemaName}" schema`);
  return 0;
}

// eslint-disable-next-line n/no-process-exit
process.exit(main());
