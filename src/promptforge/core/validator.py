from dataclasses import dataclass, field
from .models import TaskIR
from .rules import AMBIGUOUS, CONFLICTS, SCOPE_SYSTEMS
@dataclass
class Finding:
    severity: str
    code: str
    message: str
@dataclass
class ValidationResult:
    findings: list[Finding] = field(default_factory=list)
    @property
    def valid(self): return not any(f.severity in {"ERROR", "BLOCKER"} for f in self.findings)
def validate(task: TaskIR) -> ValidationResult:
    result=ValidationResult()
    for error in task.validate(): result.findings.append(Finding("ERROR", "required_field", error))
    text=" ".join(task.requirements).casefold()
    techs={str(x).casefold() for x in task.environment.get("technologies", [])}
    for a,b in CONFLICTS:
        if a.casefold() in techs and b.casefold() in techs: result.findings.append(Finding("BLOCKER", "technology_conflict", f"{a} and {b} are specified for the same scope."))
    for phrase in AMBIGUOUS:
        if phrase in text: result.findings.append(Finding("WARNING", "ambiguity", f"Clarify measurable meaning of: {phrase}"))
    for system in SCOPE_SYSTEMS:
        if system in text: result.findings.append(Finding("WARNING", "scope_creep", f"{system.upper()} appears to expand the MVP scope."))
    if not task.acceptance_criteria: result.findings.append(Finding("WARNING", "missing_acceptance", "Add measurable acceptance criteria."))
    if not task.tests: result.findings.append(Finding("WARNING", "missing_tests", "Add verification tests."))
    return result
