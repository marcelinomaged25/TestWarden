from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
import arabic_reshaper
from bidi.algorithm import get_display

OUT = r"E:\marc\GP\TestWarden_Weekly_Sprint_Team_Plan.pdf"
pdfmetrics.registerFont(TTFont("Tahoma", r"C:\Windows\Fonts\tahoma.ttf"))
pdfmetrics.registerFont(TTFont("Tahoma-Bold", r"C:\Windows\Fonts\tahomabd.ttf"))

def rtl(t): return get_display(arabic_reshaper.reshape(t))
def P(t, s): return Paragraph(rtl(t), s)

styles = getSampleStyleSheet()
title = ParagraphStyle("title", parent=styles["Title"], fontName="Tahoma-Bold", fontSize=25, leading=32, alignment=TA_CENTER, textColor=colors.HexColor("#0B3558"), spaceAfter=15)
sub = ParagraphStyle("sub", parent=styles["Normal"], fontName="Tahoma", fontSize=13, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#40566A"), spaceAfter=10)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Tahoma-Bold", fontSize=18, leading=24, alignment=TA_RIGHT, textColor=colors.HexColor("#0B3558"), spaceBefore=8, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Tahoma-Bold", fontSize=13, leading=19, alignment=TA_RIGHT, textColor=colors.HexColor("#1769AA"), spaceBefore=7, spaceAfter=5)
body = ParagraphStyle("body", parent=styles["BodyText"], fontName="Tahoma", fontSize=10.2, leading=16, alignment=TA_RIGHT, textColor=colors.HexColor("#1E2933"), spaceAfter=4)
small = ParagraphStyle("small", parent=body, fontSize=9.2, leading=14)
header = ParagraphStyle("header", parent=body, fontName="Tahoma-Bold", textColor=colors.white, fontSize=9.5, leading=14)
file_small = ParagraphStyle("file_small", parent=body, fontSize=8.0, leading=10.5)

def table(rows, widths):
    t=Table(rows,colWidths=widths,repeatRows=1,hAlign="RIGHT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0B3558")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Tahoma-Bold"),
        ("FONTNAME",(0,1),(-1,-1),"Tahoma"),
        ("FONTSIZE",(0,0),(-1,-1),9.2),
        ("LEADING",(0,0),(-1,-1),14),
        ("ALIGN",(0,0),(-1,-1),"RIGHT"),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("GRID",(0,0),(-1,-1),.3,colors.HexColor("#B8C9D6")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F7FA")]),
        ("TOPPADDING",(0,0),(-1,-1),7),
        ("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def footer(canvas,doc):
    page_w, page_h = landscape(A4)
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor("#D2DEE7")); canvas.line(1.4*cm,1.0*cm,page_w-1.4*cm,1.0*cm)
    canvas.setFont("Tahoma",8); canvas.setFillColor(colors.HexColor("#6B7D8B")); canvas.drawRightString(page_w-1.4*cm,.62*cm,rtl("TestWarden - Weekly Sprint Plan")); canvas.drawString(1.4*cm,.62*cm,str(doc.page)); canvas.restoreState()

weeks = [
("Week 1 - Project Setup", "End product: running project skeleton and team contracts.", [
"Create Git repository, branches, issue labels, and contribution rules.", "Create FastAPI project structure and health endpoint.", "Create PostgreSQL schema draft and environment configuration.", "Create basic LLM client prototype and safe configuration.", "Select two sample Python/pytest repositories and document setup.", "Create Docker sandbox that runs a Python command.", "Define standard JSON result formats for jobs and test runs.", "Write initial README, architecture notes, and a smoke-test checklist."]),
("Week 2 - Repository Connection", "End product: a user can submit a Git URL and prepare a local project.", [
"Implement Git clone and branch/commit selection.", "Detect Python files and project root.", "Detect pytest, pyproject.toml, requirements, and test folders.", "Build repository context summary for the AI.", "Define unsupported repository cases and sample error messages.", "Install dependencies inside Docker with timeout handling.", "Parse clone/build/run logs into structured job results.", "Create API endpoint and simple page for repository connection."]),
("Week 3 - Code Analysis", "End product: a complete analysis report for a Python repository.", [
"Extract Git commit metadata and changed files.", "Implement AST extraction for functions, classes, imports, and calls.", "Run pytest-cov and map coverage to files/functions.", "Create complexity calculation and analysis fixtures.", "Detect database, HTTP, filesystem, and external-service calls.", "Run analysis steps inside the sandbox.", "Test analyzer outputs on the selected sample repositories.", "Store and expose analysis results through the API."]),
("Week 4 - Risk Ranking", "End product: deterministic ranked list of risky functions.", [
"Calculate change-frequency features from Git history.", "Improve AST relationships between functions and modules.", "Implement coverage-gap and complexity features.", "Design risk explanation text and AI explanation prompt.", "Define rules for mapping targets to Unit/Integration/API tests.", "Run ranking as a background job in Docker.", "Write ranking unit tests and repeatability checks.", "Display ranked targets and factor explanations in the UI/API."]),
("Week 5 - AI Unit Test Generation", "End product: generated pytest tests for selected high-risk functions.", [
"Provide source files and target metadata to the generation pipeline.", "Build a reliable AST-to-context serializer.", "Add coverage gaps and risk reasons to the prompt context.", "Implement Unit Test Agent and structured test output.", "Collect existing fixtures, helpers, and nearby tests for context.", "Save generated tests in a temporary sandbox workspace.", "Validate generated code format and create failure categories.", "Add Generate Test action and test preview endpoint/page."]),
("Week 6 - Assumptions and Basic Verification", "End product: generated tests are reviewed with evidence and execution results.", [
"Implement temporary test-file and artifact management.", "Link generated assertions to source context where possible.", "Measure coverage contribution of each generated test.", "Implement assumption extraction and Needs Review status.", "Review generated tests for integration/API boundary cases.", "Implement compile/import checks and pytest execution.", "Implement repeated runs and stable/unstable status.", "Display test code, assumptions, logs, and verification status."]),
("Week 7 - Regression and Mutation", "End product: tests are evaluated for real bug-catching value.", [
"Implement safe temporary branch/workspace handling.", "Select mutation targets from AST and high-risk functions.", "Compare coverage before and after generated tests.", "Use surviving-mutant feedback to request stronger tests.", "Define mutation categories for logic and boundary bugs.", "Run mutants inside isolated Docker jobs.", "Implement killed/survived results and mutation score.", "Add mutation results to the verification report."]),
("Week 8 - Integration and API Tests", "End product: first multi-level testing prototype.", [
"Prepare repository environment files and test branches.", "Improve dependency/call relationships for target selection.", "Analyze external calls and integration coverage.", "Add integration scenarios to the AI context.", "Implement Integration and API Test Agent prototypes.", "Create Docker Compose test database/mock-service environment.", "Run and verify integration/API tests with pytest.", "Add test-type selection and results to the dashboard."]),
("Week 9 - Approval and Git Output", "End product: user-controlled test acceptance and branch/patch output.", [
"Implement accepted-test branch creation and commit preparation.", "Check imports and target references before approval output.", "Show quality metrics before the approval decision.", "Implement regeneration after user feedback.", "Review approval behavior for Integration/API tests.", "Run a final sandbox verification before writing output.", "Run complete verification again after accepted tests are added.", "Implement Accept/Reject/Edit and approval history UI/API."]),
("Week 10 - Benchmark Evaluation", "End product: reproducible evaluation on BugsInPy/Tests4Py.", [
"Implement benchmark checkout adapter for buggy/fixed subjects.", "Analyze benchmark subjects with the normal analyzer.", "Prepare metric schemas and result tables.", "Run generated tests on buggy and fixed versions.", "Classify detected bugs by type and test level.", "Execute benchmark subjects reproducibly in Docker.", "Calculate detection rate, mutation score, and coverage change.", "Create evaluation report and benchmark dashboard view."]),
("Week 11 - Integration and Hardening", "End product: complete end-to-end demo with error handling.", [
"Test the full Git-to-branch workflow and fix integration issues.", "Fix AST edge cases and unsupported syntax handling.", "Validate risk ranking against known benchmark targets.", "Improve prompts, reduce hallucinated imports, and handle repair loops.", "Stabilize integration/API scenarios and mocks.", "Test timeouts, resource limits, dependency failures, and isolation.", "Run end-to-end verification and regression suite.", "Connect all features into one demo flow and track remaining bugs."]),
("Week 12 - Final Delivery", "End product: final release, report, presentation, and live demonstration.", [
"Finalize Git integration documentation.", "Finalize code-analysis documentation and examples.", "Document risk formula, metrics, and limitations.", "Document AI prompts, assumptions, and generation limitations.", "Document Unit/Integration/API test behavior.", "Document sandbox security and deployment instructions.", "Finalize verification and mutation-testing results.", "Prepare final dashboard demo, report, slides, and release checklist."]),
]

files_by_week = [
[
".git/; CONTRIBUTING.md; .github/",
"app/main.py; app/api/health.py",
"app/core/config.py; .env.example; migrations/",
"app/ai/llm_client.py; app/ai/config.py",
"benchmarks/samples/; docs/sample-repositories.md",
"docker/sandbox/Dockerfile; docker/sandbox/run.py",
"app/schemas/jobs.py; app/schemas/results.py",
"README.md; docs/architecture.md; docs/smoke-test.md"],
[
"app/services/repository_connector.py; app/api/routes_repositories.py",
"app/analyzers/project_detector.py",
"app/analyzers/framework_detector.py; pyproject.toml",
"app/ai/context_builder.py",
"app/schemas/support.py; docs/supported-projects.md",
"docker/sandbox/install_dependencies.sh",
"app/execution/log_parser.py; app/schemas/execution.py",
"app/api/routes_repositories.py; frontend/repositories/"],
[
"app/analyzers/git_history_analyzer.py",
"app/analyzers/ast_parser.py",
"app/analyzers/coverage_analyzer.py; app/analyzers/complexity_analyzer.py",
"tests/fixtures/analysis/; app/analyzers/analysis_context.py",
"app/analyzers/dependency_detector.py; app/analyzers/api_detector.py",
"app/services/analysis_service.py; workers/analysis_tasks.py",
"tests/unit/analyzers/; tests/integration/analyzer/",
"app/models/analysis.py; app/schemas/analysis.py; app/api/routes_analysis.py"],
[
"app/analyzers/git_history_analyzer.py",
"app/analyzers/call_graph.py; app/models/code_entity.py",
"app/services/risk_service.py; app/risk/features.py",
"app/ai/risk_explainer.py; prompts/risk_explanation.txt",
"app/routing/test_type_router.py; app/routing/rules.py",
"workers/risk_tasks.py; app/orchestration/orchestrator.py",
"tests/unit/test_risk_service.py; tests/integration/test_ranking.py",
"app/api/routes_risk.py; frontend/risk/"],
[
"app/ai/context_builder.py; app/ai/source_context.py",
"app/ai/serializers/ast_serializer.py",
"app/ai/prompt_builder.py; prompts/unit_test.txt",
"app/agents/unit_test_agent.py; app/agents/base_agent.py",
"app/ai/fixture_collector.py; app/ai/test_style.py",
"app/services/generation_service.py; workers/generation_tasks.py",
"app/verification/generated_code_validator.py",
"app/api/routes_generation.py; frontend/generated-tests/"],
[
"app/services/artifact_service.py; storage/generated/",
"app/ai/assumption_extractor.py; app/ai/assertion_sources.py",
"app/analyzers/test_coverage_delta.py",
"app/ai/assumption_extractor.py; prompts/assumptions.txt",
"app/agents/integration_test_agent.py; app/agents/api_test_agent.py",
"app/verification/compile_checker.py; app/execution/pytest_runner.py",
"app/verification/stability_checker.py; tests/unit/verification/",
"app/api/routes_verification.py; frontend/verification/"],
[
"app/execution/worktree_manager.py; app/services/repository_connector.py",
"app/verification/mutation_target_selector.py; app/verification/ast_mutator.py",
"app/analyzers/coverage_analyzer.py; app/analyzers/coverage_delta.py",
"app/ai/test_repair.py; prompts/repair.txt",
"app/verification/mutation_operators.py",
"app/verification/mutation_runner.py; docker/sandbox/mutation.sh",
"app/verification/mutation_score.py; app/models/mutation.py",
"app/api/routes_verification.py; frontend/mutation/"],
[
"app/services/repository_connector.py; docker/test-environments/",
"app/analyzers/dependency_graph.py",
"app/analyzers/external_call_detector.py; app/analyzers/integration_coverage.py",
"app/ai/integration_context.py; prompts/integration.txt",
"app/agents/integration_test_agent.py; app/agents/api_test_agent.py",
"docker-compose.test.yml; docker/test-environments/",
"app/verification/integration_runner.py; tests/integration/",
"app/routing/test_type_router.py; app/api/routes_tests.py; frontend/test-types/"],
[
"app/services/git_output_service.py; app/services/branch_service.py",
"app/verification/target_reference_checker.py",
"frontend/metrics/; app/schemas/quality.py",
"app/services/regeneration_service.py; app/ai/feedback_context.py",
"tests/integration/approval/; app/approval/test_approval_rules.py",
"app/approval/final_verification.py; workers/approval_tasks.py",
"app/verification/post_approval_runner.py",
"app/api/routes_approval.py; app/models/approval.py; frontend/approval/"],
[
"app/evaluation/bugsinpy_adapter.py; app/evaluation/checkout.py",
"app/evaluation/benchmark_analyzer.py",
"app/evaluation/metrics_schema.py; reports/templates/",
"app/evaluation/benchmark_runner.py; workers/evaluation_tasks.py",
"app/evaluation/bug_classifier.py; app/evaluation/test_level.py",
"docker/benchmark/Dockerfile; docker/benchmark/run_subject.sh",
"app/evaluation/metrics.py; app/evaluation/statistics.py",
"app/api/routes_evaluation.py; frontend/evaluation/; reports/"],
[
"tests/e2e/test_git_workflow.py; docs/git-workflow.md",
"tests/unit/analyzers/test_edge_cases.py; app/analyzers/compatibility.py",
"reports/risk_validation.csv; docs/risk-validation.md",
"prompts/; app/ai/guardrails.py",
"tests/integration/test_api_and_integration.py; docker/test-environments/",
"tests/security/test_sandbox_limits.py; docker/sandbox/limits.py",
"tests/e2e/test_full_verification.py; tests/regression/",
"app/orchestration/orchestrator.py; frontend/demo/; docs/demo-script.md"],
[
"docs/git-integration.md; app/services/repository_connector.py",
"docs/analysis.md; app/analyzers/README.md",
"docs/metrics.md; docs/limitations.md",
"docs/ai-generation.md; docs/prompts.md",
"docs/testing-levels.md; docs/integration-testing.md",
"docs/sandbox-security.md; deployment/README.md",
"docs/verification.md; docs/mutation-testing.md",
"docs/final-demo.md; docs/final-checklist.md; presentation/"],
]

S=[Spacer(1,1.4*cm),P("TestWarden",title),P("Weekly Agile Sprint Plan and Task Distribution",sub),P("The 8 team members are reallocated every week. No permanent ownership is assumed.",sub),Spacer(1,.7*cm),P("How to use this plan",h1),P("Each week is one Sprint. Every member receives one concrete task. The team reviews the end product at the end of the week. Tasks can be adjusted during planning, but the weekly deliverable must remain clear.",body),P("Team labels",h2),P("M1 to M8 are temporary labels. Replace them with the actual team member names before sharing the plan.",body),PageBreak()]

S += [P("System Architecture",h1), P("The architecture below shows the complete TestWarden flow from repository connection to verification and approval.",body)]
arch = Image(r"E:\marc\GP\mermaid-diagram.png", width=25.0*cm, height=15.5*cm)
S += [arch, Spacer(1,.3*cm), P("Important MVP note: Unit Test Agent is implemented first. Integration and API Agents follow. Security, E2E, and Performance Agents remain future extensions.",small), PageBreak()]

S += [P("Project File Architecture",h1), P("The file structure below is the target structure. The weekly tables identify exactly which files or artifacts are touched by each task.",body)]
file_tree = """testwarden/\n├── app/\n│   ├── api/              FastAPI routes\n│   ├── models/           Database models\n│   ├── schemas/          Request/result contracts\n│   ├── analyzers/        AST, coverage, Git, dependencies\n│   ├── agents/           Unit, Integration, API agents\n│   ├── ai/               LLM client, prompts, assumptions\n│   ├── execution/        Docker and pytest runners\n│   ├── verification/     Stability, regression, mutation\n│   ├── orchestration/    Workflow and background jobs\n│   └── evaluation/       BugsInPy/Tests4Py and metrics\n├── workers/              Redis/Celery tasks\n├── frontend/             Dashboard pages and components\n├── tests/                Unit, integration, API, E2E tests\n├── docker/               Sandbox and benchmark environments\n├── benchmarks/           Evaluation subjects\n├── reports/              Generated evaluation reports\n└── docs/                 Architecture, API, testing, demo docs"""
file_rows = [[P("Folder / file area", header), P("Purpose", header)],
    [P("app/api/", file_small), P("FastAPI routes for repositories, analysis, generation, verification, approval, and evaluation.", file_small)],
    [P("app/models/", file_small), P("PostgreSQL database models for repositories, runs, risks, tests, verification, and approvals.", file_small)],
    [P("app/schemas/", file_small), P("Request and response contracts shared between the frontend, backend, workers, and services.", file_small)],
    [P("app/analyzers/", file_small), P("Python AST, pytest discovery, coverage, complexity, Git history, dependencies, and API detection.", file_small)],
    [P("app/agents/", file_small), P("Unit Test Agent, Integration Test Agent, API Test Agent, and the test type router.", file_small)],
    [P("app/ai/", file_small), P("LLM client, context builders, prompts, assumption extraction, and test repair.", file_small)],
    [P("app/execution/", file_small), P("Docker runner, dependency installation, pytest runner, logs, timeouts, and resource limits.", file_small)],
    [P("app/verification/", file_small), P("Compile checks, pytest checks, stability, regression, mutation execution, and verification engine.", file_small)],
    [P("app/orchestration/", file_small), P("Workflow states, job manager, and coordination of analysis, generation, and verification.", file_small)],
    [P("app/evaluation/", file_small), P("BugsInPy/Tests4Py adapters, benchmark runner, metrics, and evaluation reports.", file_small)],
    [P("workers/", file_small), P("Redis/Celery background tasks for long-running analysis, generation, verification, and evaluation jobs.", file_small)],
    [P("frontend/", file_small), P("Dashboard pages and components for risk, generated tests, reports, approval, and evaluation.", file_small)],
    [P("tests/", file_small), P("Unit, integration, API, regression, and end-to-end tests for TestWarden itself.", file_small)],
    [P("docker/", file_small), P("Sandbox image, benchmark image, test environments, and execution scripts.", file_small)],
    [P("benchmarks/", file_small), P("Selected Python repositories and benchmark subjects used for evaluation.", file_small)],
    [P("reports/", file_small), P("Generated experiment results, metrics tables, and final evaluation outputs.", file_small)],
    [P("docs/", file_small), P("Architecture, API, testing strategy, security, demo script, and project documentation.", file_small)]]
file_tbl = Table(file_rows, colWidths=[6.0*cm,21.5*cm], repeatRows=1, hAlign="RIGHT")
file_tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0B3558")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.3,colors.HexColor("#B8C9D6")),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F7FA")]),("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
S += [file_tbl, Spacer(1,.25*cm), P("Rule: every task must update the relevant file, add or update tests, and leave demo evidence for the sprint review.",body), PageBreak()]

for idx,(name,deliverable,tasks) in enumerate(weeks):
    S += [P(name,h1),P(deliverable,h2)]
    rows=[[P("Member",header),P("Task for this week",header),P("Files / artifacts",header),P("Done when",header)]]
    for i,task in enumerate(tasks):
        rows.append([P(f"M{i+1}",small),P(task,small),P(files_by_week[idx][i],small),P("Code + test + demo evidence",small)])
    S += [table(rows,[2.0*cm,11.2*cm,10.3*cm,3.2*cm])]
    if idx != len(weeks)-1: S += [PageBreak()]

PAGE = landscape(A4)
doc=SimpleDocTemplate(OUT,pagesize=PAGE,rightMargin=1.4*cm,leftMargin=1.4*cm,topMargin=1.2*cm,bottomMargin=1.5*cm,title="TestWarden Weekly Sprint Team Plan",author="TestWarden Team")
doc.build(S,onFirstPage=footer,onLaterPages=footer)
print(OUT)
