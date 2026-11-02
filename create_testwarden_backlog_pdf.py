from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
import arabic_reshaper
from bidi.algorithm import get_display

OUT = r"E:\marc\GP\TestWarden_Agile_Backlog_and_Sprints.pdf"
pdfmetrics.registerFont(TTFont("Tahoma", r"C:\Windows\Fonts\tahoma.ttf"))
pdfmetrics.registerFont(TTFont("Tahoma-Bold", r"C:\Windows\Fonts\tahomabd.ttf"))

def rtl(t):
    return get_display(arabic_reshaper.reshape(t))
def P(t, s):
    return Paragraph(rtl(t), s)

styles = getSampleStyleSheet()
title = ParagraphStyle("title", parent=styles["Title"], fontName="Tahoma-Bold", fontSize=23, leading=30, alignment=TA_CENTER, textColor=colors.HexColor("#0B3558"), spaceAfter=16)
sub = ParagraphStyle("sub", parent=styles["Normal"], fontName="Tahoma", fontSize=12, leading=19, alignment=TA_CENTER, textColor=colors.HexColor("#40566A"), spaceAfter=12)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Tahoma-Bold", fontSize=17, leading=23, alignment=TA_RIGHT, textColor=colors.HexColor("#0B3558"), spaceBefore=10, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Tahoma-Bold", fontSize=13, leading=19, alignment=TA_RIGHT, textColor=colors.HexColor("#1769AA"), spaceBefore=8, spaceAfter=5)
body = ParagraphStyle("body", parent=styles["BodyText"], fontName="Tahoma", fontSize=9.5, leading=16, alignment=TA_RIGHT, textColor=colors.HexColor("#1E2933"), spaceAfter=4)
small = ParagraphStyle("small", parent=body, fontSize=8.5, leading=13, textColor=colors.HexColor("#536573"))
code = ParagraphStyle("code", parent=body, fontSize=9, leading=15, backColor=colors.HexColor("#EEF5FA"), borderPadding=6, alignment=TA_LEFT)

def table(rows, widths):
    t = Table(rows, colWidths=widths, repeatRows=1, hAlign="RIGHT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0B3558")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Tahoma-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Tahoma"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("LEADING", (0,0), (-1,-1), 13),
        ("ALIGN", (0,0), (-1,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("GRID", (0,0), (-1,-1), .3, colors.HexColor("#B8C9D6")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F3F7FA")]),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return t

def bullets(items):
    return [P("• " + x, body) for x in items]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D2DEE7"))
    canvas.line(1.5*cm, 1.2*cm, A4[0]-1.5*cm, 1.2*cm)
    canvas.setFont("Tahoma", 8)
    canvas.setFillColor(colors.HexColor("#6B7D8B"))
    canvas.drawRightString(A4[0]-1.5*cm, .78*cm, rtl("TestWarden - Agile Backlog"))
    canvas.drawString(1.5*cm, .78*cm, str(doc.page))
    canvas.restoreState()

S=[]
S += [Spacer(1, 1.5*cm), P("TestWarden", title), P("Agile Product Backlog, Sprint Plan & Team Distribution", sub), P("Python + pytest AI testing platform", sub), Spacer(1, 1*cm)]
S += [P("Product Goal", h1), P("Build a platform that analyzes Python repositories, ranks risky code, generates Unit/Integration/API tests, verifies their quality through pytest and mutation testing, and requires developer approval before creating a patch or branch.", body)]
S += [P("MVP Definition", h1), P("The first release supports Python and pytest. It includes repository analysis, risk ranking, AI Unit Test generation, Docker execution, stability checks, mutation testing, reports, and human approval.", body)]
S += [P("Priority Rules", h2), P("Must Have = required for MVP. Should Have = important after MVP. Could Have = future enhancement. Story points use Fibonacci estimates: 1, 2, 3, 5, 8, 13.", body)]
S += [P("Deferred Scope", h2), P("Java/JUnit, IDE extension, PR comments, browser E2E, advanced performance testing, concurrency testing, automatic refactoring, Kubernetes, and full multi-language support are deferred.", body)]
S += [PageBreak()]

S += [P("Product Backlog - MVP", h1)]
rows=[[P("ID",body),P("User Story",body),P("Priority",body),P("Points",body)]]
backlog=[
('REPO-01','Connect a valid Python Git repository','Must',5),('REPO-02','Clone a selected branch or commit','Must',3),('REPO-03','Detect Python and pytest automatically','Must',3),('REPO-04','Show clear errors for invalid or unsupported repositories','Must',2),('ANALYSIS-01','Extract Python files, modules, classes, and functions','Must',5),('ANALYSIS-02','Discover pytest tests, fixtures, and conftest.py','Must',3),('ANALYSIS-03','Calculate coverage and complexity','Must',5),('ANALYSIS-04','Analyze Git change history','Should',5),('RISK-01','Rank functions by testing risk','Must',5),('RISK-02','Explain the factors behind every risk score','Must',3),('ROUTER-01','Recommend Unit, Integration, or API tests','Must',5),('UNIT-01','Generate pytest tests for a selected function','Must',8),('UNIT-02','Follow project fixtures, helpers, and naming style','Must',5),('UNIT-03','Generate normal, boundary, invalid, and error cases','Must',5),('ASSUMP-01','Show assumptions behind generated assertions','Must',5),('SANDBOX-01','Run code and tests inside Docker','Must',8),('VERIFY-01','Check syntax, imports, and pytest execution','Must',5),('VERIFY-02','Rerun tests to detect instability','Must',5),('VERIFY-03','Run existing tests and detect regressions','Must',5),('MUT-01','Create mutations and run tests against them','Must',8),('MUT-02','Calculate and display mutation score','Must',3),('APP-01','Accept, reject, edit, or regenerate tests','Must',5),('APP-02','Create a patch or branch only after approval','Should',5),('EVAL-01','Run TestWarden on BugsInPy/Tests4Py subjects','Must',5),('EVAL-02','Measure bug detection rate and coverage improvement','Must',5)]
for a,b,c,d in backlog: rows.append([P(a,small),P(b,small),P(c,small),P(str(d),small)])
S += [table(rows,[2.2*cm,10.1*cm,2.4*cm,1.4*cm])]

S += [PageBreak(), P("Sprint Plan", h1), P("Assumption: 2-week sprints. Each sprint should end with a demonstrable increment and a short review.", body)]
sprints=[
('Sprint 0 - Planning','Finalize scope, architecture, data contracts, repositories for evaluation, Git workflow, and definition of done.','SRS, architecture, backlog, repo list'),
('Sprint 1 - Foundation','Create FastAPI project, PostgreSQL models, repository cloning, Python/pytest detection, and a basic Docker runner.','Repository can be connected and executed'),
('Sprint 2 - Repository Analysis','Implement AST parser, pytest discovery, fixture detection, coverage collection, complexity analysis, and project structure report.','Analysis report for a Python project'),
('Sprint 3 - Risk Ranking','Implement risk formula, high-risk target list, score explanation, deterministic ordering, and target selection.','Ranked risky functions'),
('Sprint 4 - AI Unit Agent','Build context builder, LLM integration, pytest generation, project-style matching, edge cases, and assumption extraction.','Generated tests for selected functions'),
('Sprint 5 - Verification','Add compile check, pytest execution, logs, repeated runs, failure reasons, and regression checking.','Verified/Rejected test report'),
('Sprint 6 - Mutation Testing','Add mutation generation, mutant execution, killed/survived results, mutation score, and high-risk-only execution.','Mutation-validated tests'),
('Sprint 7 - Integration and API','Add test type router, integration test environment, database/mock support, and API test generation.','Unit + Integration + API prototype'),
('Sprint 8 - Dashboard and Approval','Build risk view, generated test review, assumptions view, verification report, accept/reject/edit, and run history.','Usable web workflow'),
('Sprint 9 - Evaluation and Hardening','Add BugsInPy/Tests4Py adapter, buggy/fixed comparison, metrics, reproducible reports, security review, and final demo.','Evaluation results and final release')]
rows=[[P("Sprint",body),P("Scope",body),P("Deliverable",body)]]
for a,b,c in sprints: rows.append([P(a,small),P(b,small),P(c,small)])
S += [table(rows,[4.0*cm,8.5*cm,3.6*cm])]

S += [PageBreak(), P("Team Distribution - 8 Members", h1), P("Each owner is responsible for implementation, tests, documentation, and integration with the shared data contracts.", body)]
team=[
('Member 1','Repository Connector & Git','Clone repositories, branches/commits, GitHub/GitLab integration, patch/branch output.','REPO'),
('Member 2','AST & Repository Analyzer','AST parsing, function/class extraction, project structure, pytest discovery.','ANALYSIS'),
('Member 3','Coverage, Git & Risk','pytest-cov, complexity, Git history, risk formula, ranking explanation.','ANALYSIS/RISK'),
('Member 4','AI Unit Test Agent','Prompting, context builder, pytest generation, edge cases, test repair.','UNIT/AI'),
('Member 5','Integration & API Agents','Dependency/API detection, mocks, test database, integration and API test generation.','ROUTER/INTEGRATION'),
('Member 6','Sandbox & Execution','Docker sandbox, dependency installation, timeouts, resource limits, logs.','SANDBOX'),
('Member 7','Verification & Mutation','pytest runner, stability, regression, mutation testing, verification report.','VERIFY/MUTATION'),
('Member 8','Backend, Dashboard & Evaluation','FastAPI, PostgreSQL, Redis jobs, dashboard, approval workflow, BugsInPy/Tests4Py evaluation.','API/UI/EVAL')]
rows=[[P("Owner",body),P("Area",body),P("Responsibilities",body),P("Backlog",body)]]
for a,b,c,d in team: rows.append([P(a,small),P(b,small),P(c,small),P(d,small)])
S += [table(rows,[2.5*cm,4.0*cm,8.0*cm,2.0*cm])]
S += [P("Shared responsibilities", h2)] + bullets(["Everyone writes unit tests for their own component.","Everyone follows the agreed JSON/data contracts.","Every feature must have a demo and acceptance criteria.","No branch is merged without integration testing.","Member 8 coordinates integration, but every owner contributes to the final demo."])

S += [PageBreak(), P("Definition of Done", h1), P("A backlog item is complete only when all applicable conditions are satisfied:", body)]
S += bullets(["Implementation is committed to the team branch.","Automated tests are added and passing.","The feature works with a real Python/pytest repository.","Errors are handled and reported clearly.","Documentation is updated.","The feature is connected to the rest of the system.","A team member other than the owner reviews it.","The feature is demonstrated during sprint review."])
S += [P("Sprint Review Demo Path", h1), P("At the end of the project, the team should demonstrate this complete path:", body), P("Connect repository → Analyze project → Rank risky function → Generate pytest test → Review assumptions → Run inside Docker → Check stability → Run mutation testing → Show report → Approve test → Create branch/patch", code)]
S += [P("Recommended MVP Cut", h1), P("If time becomes limited, stop after Sprint 6 and deliver a strong Unit Testing pipeline. Integration tests, API tests, Dashboard enhancements, and benchmark expansion can follow as later increments.", body)]

doc=SimpleDocTemplate(OUT,pagesize=A4,rightMargin=1.5*cm,leftMargin=1.5*cm,topMargin=1.4*cm,bottomMargin=1.7*cm,title="TestWarden Agile Backlog",author="TestWarden Team")
doc.build(S,onFirstPage=footer,onLaterPages=footer)
print(OUT)
