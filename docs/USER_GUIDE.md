# User Guide: PE Assessment for Learning System

## Quick Start

### Installation

```bash
git clone https://github.com/hind450/pe-revision-checklist.git
cd pe-revision-checklist
pip install -r requirements.txt
```

### Running the Example

```bash
python examples/example_workflow.py
```

This demonstrates the complete system workflow with sample data.

## Basic Usage

```python
import sys
sys.path.insert(0, 'src')
from main import PEAssessmentSystem

# Initialize system
system = PEAssessmentSystem(output_dir="./output")

# Load mark scheme
mark_scheme = system.load_mark_scheme('markscheme.pdf')

# Process student scripts
reports = system.process_batch(
    file_paths=['student1.pdf', 'student2.pdf'],
    student_ids=['S001', 'S002'],
    student_names=['Alice', 'Bob']
)

# Generate class analytics
analytics = system.generate_class_analytics('MyClass', reports)

# Export reports
system.export_reports(reports, analytics)
```

## Understanding Reports

### Traffic Light System

- 🟢 **Green (70%+)**: Strong performance, mastery achieved
- 🟡 **Amber (50-69%)**: Satisfactory, needs improvement
- 🔴 **Red (<50%)**: Significant gaps, priority revision

### Assessment Objectives

- **AO1 (Knowledge)**: Recall of facts and concepts
- **AO2 (Application)**: Use of knowledge in context
- **AO3 (Evaluation)**: Analysis and critical thinking

## Configuration

Edit `config/config.yaml` to customize:
- Marking thresholds
- Performance levels
- Topics and misconceptions

## Best Practices

1. **Quality Scans**: Use 300 DPI or higher for PDFs
2. **Clear Numbering**: Match question numbers exactly
3. **Detailed Mark Schemes**: Include multiple acceptable answers
4. **Review Results**: Check low confidence scores manually

For detailed documentation, see the repository README.
