#!/usr/bin/env node

/**
 * CLI Tool for PE Assessment System
 * 
 * Usage: node cli.js --student <student-file> --markscheme <markscheme-file> [--examiner <examiner-file>]
 */

const fs = require('fs');
const path = require('path');
const PEAssessment = require('./index');

function showHelp() {
  console.log(`
PE Assessment CLI Tool

Usage:
  node cli.js --student <file> --markscheme <file> [--examiner <file>] [--output <file>]

Options:
  --student, -s      Path to student script JSON file (required)
  --markscheme, -m   Path to mark scheme JSON file (required)
  --examiner, -e     Path to examiner comments JSON file (optional)
  --output, -o       Path to save output report (optional, prints to console by default)
  --json             Output in JSON format instead of text
  --help, -h         Show this help message

Examples:
  node cli.js -s examples/student-script.json -m examples/mark-scheme.json
  node cli.js -s student.json -m scheme.json -e comments.json -o report.txt
  node cli.js -s student.json -m scheme.json --json -o report.json
  `);
}

function parseArgs(args) {
  const options = {
    studentFile: null,
    markSchemeFile: null,
    examinerFile: null,
    outputFile: null,
    jsonOutput: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    } else if (arg === '--student' || arg === '-s') {
      options.studentFile = args[++i];
    } else if (arg === '--markscheme' || arg === '-m') {
      options.markSchemeFile = args[++i];
    } else if (arg === '--examiner' || arg === '-e') {
      options.examinerFile = args[++i];
    } else if (arg === '--output' || arg === '-o') {
      options.outputFile = args[++i];
    } else if (arg === '--json') {
      options.jsonOutput = true;
    }
  }

  return options;
}

function loadJSON(filePath) {
  try {
    const fullPath = path.resolve(filePath);
    const data = fs.readFileSync(fullPath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error loading file ${filePath}:`, error.message);
    process.exit(1);
  }
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    showHelp();
    process.exit(0);
  }

  const options = parseArgs(args);

  // Validate required arguments
  if (!options.studentFile || !options.markSchemeFile) {
    console.error('Error: Both --student and --markscheme arguments are required\n');
    showHelp();
    process.exit(1);
  }

  // Load data
  console.log('Loading data...');
  const studentScript = loadJSON(options.studentFile);
  const markScheme = loadJSON(options.markSchemeFile);
  const examinerComments = options.examinerFile ? loadJSON(options.examinerFile) : {};

  // Process assessment
  console.log('Processing assessment...\n');
  const peAssessment = new PEAssessment();
  const result = peAssessment.processAssessment(studentScript, markScheme, examinerComments);

  // Generate output
  let output;
  if (options.jsonOutput) {
    output = JSON.stringify({
      assessment: result.assessment,
      feedbackReport: result.feedbackReport
    }, null, 2);
  } else {
    output = result.textReport;
  }

  // Save or display output
  if (options.outputFile) {
    try {
      fs.writeFileSync(options.outputFile, output, 'utf8');
      console.log(`Report saved to: ${options.outputFile}`);
    } catch (error) {
      console.error(`Error saving report:`, error.message);
      process.exit(1);
    }
  } else {
    console.log(output);
  }
}

// Run CLI
if (require.main === module) {
  main();
}

module.exports = { parseArgs, loadJSON };
