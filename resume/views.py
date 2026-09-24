"""
Views for the `resume` app. See section headers below for a map of what
lives where (public pages, resume CRUD, sharing, AI assistant, admin).
"""

import json
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.conf import settings

# WeasyPrint turns HTML + CSS into a PDF. We reuse the *exact same* templates
# used for the on-screen preview so the downloaded PDF always matches what
# the user saw (see render_resume_template() / download_resume() below).
from weasyprint import HTML

from .models import Resume, Education, Experience, Project, Skill, Certificate, Language, Hobby, SiteVisitor
from .forms import ResumeForm, EducationForm, ExperienceForm, ProjectForm, SkillForm, CertificateForm, LanguageForm, HobbyForm

TEMPLATES_INFO = [
    {"id": "modern", "name": "Modern", "desc": "Clean, minimal, ATS-friendly", "color": "#0d6efd", "icon": "bi-layout-text-sidebar", "bg": "linear-gradient(135deg,#0d6efd,#6610f2)"},
    {"id": "professional", "name": "Professional", "desc": "Corporate two-column layout", "color": "#198754", "icon": "bi-briefcase-fill", "bg": "linear-gradient(135deg,#198754,#20c997)"},
    {"id": "creative", "name": "Creative", "desc": "Bold, colorful, eye-catching", "color": "#dc3545", "icon": "bi-palette-fill", "bg": "linear-gradient(135deg,#dc3545,#fd7e14)"},
    {"id": "executive", "name": "Executive", "desc": "Dark, elegant, premium feel", "color": "#212529", "icon": "bi-award-fill", "bg": "linear-gradient(135deg,#212529,#495057)"},
]

TEMPLATE_FILE_MAP = {
    "modern": "resume/templates/modern.html",
    "professional": "resume/templates/professional.html",
    "creative": "resume/templates/creative.html",
    "executive": "resume/templates/executive.html",
}


def is_admin(user):
    """Used by @user_passes_test to gate the custom admin dashboard to staff users."""
    return user.is_authenticated and user.is_staff


def get_gemini_model():
    """
    Configure and return a Gemini GenerativeModel instance.

    Centralizing this avoids repeating genai.configure(...) and the model
    name in every view -- change settings.GEMINI_MODEL_NAME once and every
    AI feature picks it up. Currently set to Gemini 2.5 Flash.

    Raises RuntimeError with a friendly message if no API key is configured
    so callers can show that message to the user instead of a raw traceback.
    """
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("Gemini API key is not configured. Add GEMINI_API_KEY to your .env file.")
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel(settings.GEMINI_MODEL_NAME)


def render_resume_template(request, resume, *, preview=False, pdf_mode=False):
    """
    Render one of the 4 style templates (modern/professional/creative/executive)
    for a given resume in one of two modes:

      - preview=True  : logged-in owner previewing inside the dashboard
                        (shows the floating toolbar with Print/Download/Change Template)
      - pdf_mode=True  : used internally by WeasyPrint to build the PDF
                        (no toolbar / no interactive elements)

    Both modes render the exact same underlying HTML/CSS, so the PDF and
    the on-screen preview always look identical to each other.
    """
    tpl_path = TEMPLATE_FILE_MAP.get(resume.template, TEMPLATE_FILE_MAP["modern"])
    template = get_template(tpl_path)
    return template.render({
        "resume": resume,
        "preview": preview,
        "pdf_mode": pdf_mode,
    }, request=request)


# ─── Public ─────────────────────────────────────────────────────────────────

def home(request):
    """Public landing page -- shows the 4 available templates to logged-out visitors."""
    return render(request, "home.html", {"templates": TEMPLATES_INFO})


def about_page(request):
    """Static 'About' page -- what ResumePro is and who built it."""
    return render(request, "about.html")


def help_page(request):
    """Static 'Help' page -- basic FAQ / how-to-use guide."""
    return render(request, "help.html")


def contact_page(request):
    """Static 'Contact' page -- how to reach the developer."""
    return render(request, "contact.html")


# ─── Dashboard ──────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """Logged-in user's home screen: their resumes plus a few summary counts."""
    resumes = Resume.objects.filter(user=request.user)
    return render(request, "dashboard.html", {
        "resumes": resumes,
        "total_resumes": resumes.count(),
        "total_projects": Project.objects.filter(resume__user=request.user).count(),
        "total_skills": Skill.objects.filter(resume__user=request.user).count(),
        "total_certificates": Certificate.objects.filter(resume__user=request.user).count(),
        "templates_info": TEMPLATES_INFO,
    })


# ─── Template Chooser ────────────────────────────────────────────────────────

@login_required
def choose_template(request):
    """Template picker screen shown before creating a new resume."""
    return render(request, "choose_template.html", {"templates": TEMPLATES_INFO})


# ─── Resume CRUD ─────────────────────────────────────────────────────────────

@login_required
def create_resume(request):
    """Step 2 of resume creation: collect personal-info fields for the template chosen on the previous screen."""
    selected_template = request.GET.get("template", "modern")
    if selected_template not in ["modern", "professional", "creative", "executive"]:
        selected_template = "modern"

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, "Resume created! Now add your details.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = ResumeForm(initial={"template": selected_template})

    return render(request, "create_resume.html", {
        "form": form,
        "selected_template": selected_template,
        "templates_info": TEMPLATES_INFO,
    })


@login_required
def resume_list(request):
    """All of the current user's resumes, in a simple list/grid."""
    resumes = Resume.objects.filter(user=request.user)
    return render(request, "resume_list.html", {"resumes": resumes})


@login_required
def resume_detail(request, id):
    """A single resume's management page: section editors, download/preview/print actions."""
    resume = get_object_or_404(Resume, id=id, user=request.user)
    return render(request, "resume_detail.html", {"resume": resume})


@login_required
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume updated!")
            return redirect("resume_detail", id=resume.id)
    else:
        form = ResumeForm(instance=resume)
    return render(request, "edit_resume.html", {"form": form, "resume": resume})


@login_required
def delete_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        resume.delete()
        messages.success(request, "Resume deleted.")
        return redirect("resume_list")
    return render(request, "delete_resume.html", {"resume": resume})


@login_required
def change_template(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        new_tpl = request.POST.get("template", "modern")
        if new_tpl in ["modern", "professional", "creative", "executive"]:
            resume.template = new_tpl
            resume.save()
            messages.success(request, f"Template changed to {new_tpl.title()}!")
        return redirect("resume_detail", id=resume.id)
    return render(request, "change_template.html", {"resume": resume, "templates": TEMPLATES_INFO})


@login_required
def preview_resume(request, id):
    """On-screen preview of the resume, exactly as it will appear in the PDF."""
    resume = get_object_or_404(Resume, id=id, user=request.user)
    tpl_path = TEMPLATE_FILE_MAP.get(resume.template, TEMPLATE_FILE_MAP["modern"])
    return render(request, tpl_path, {"resume": resume, "preview": True, "pdf_mode": False})


@login_required
def download_resume(request, id):
    """
    Generate a PDF download of the resume.

    IMPORTANT: this renders the *same* template file used for preview_resume()
    (via render_resume_template with pdf_mode=True), so the PDF is guaranteed
    to look identical to what the user saw on screen -- including the
    profile photo, which previously was missing from the old, separate
    "_pdf.html" templates.
    """
    resume = get_object_or_404(Resume, id=id, user=request.user)
    html_string = render_resume_template(request, resume, preview=False, pdf_mode=True)

    # base_url lets WeasyPrint resolve relative URLs (e.g. the uploaded
    # profile photo at /media/resume_photos/...) against this site.
    base_url = request.build_absolute_uri('/')
    pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'
    return response


# ─── Section CRUD (Education / Experience / Project / Skill / Certificate /
#     Language / Hobby) ───────────────────────────────────────────────────
#
# Every section below follows the exact same simple pattern:
#   add_<section>()    -> GET shows a blank form, POST creates + attaches
#                          it to the resume (ownership checked via
#                          get_object_or_404(Resume, id=id, user=request.user))
#   edit_<section>()   -> GET shows the existing values, POST updates them
#                          (ownership checked via resume__user=request.user
#                          on the child object itself)
#   delete_<section>() -> POST removes the row and redirects back to the
#                          resume detail page
# Comments are only added where a function deviates from this pattern.

@login_required
def add_education(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            e = form.save(commit=False); e.resume = resume; e.save()
            messages.success(request, "Education added.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = EducationForm()
    return render(request, "add_education.html", {"form": form, "resume": resume})


@login_required
def edit_education(request, id):
    edu = get_object_or_404(Education, id=id, resume__user=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            form.save(); messages.success(request, "Education updated.")
            return redirect("resume_detail", id=edu.resume.id)
    else:
        form = EducationForm(instance=edu)
    return render(request, "edit_education.html", {"form": form, "education": edu})


@login_required
def delete_education(request, id):
    edu = get_object_or_404(Education, id=id, resume__user=request.user)
    rid = edu.resume.id
    if request.method == "POST":
        edu.delete(); messages.success(request, "Education deleted.")
        return redirect("resume_detail", id=rid)
    return render(request, "delete_confirm.html", {"title": "Delete Education", "item": edu.degree, "back_id": rid})


# ─── Experience ──────────────────────────────────────────────────────────────

@login_required
def add_experience(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            e = form.save(commit=False); e.resume = resume; e.save()
            messages.success(request, "Experience added.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = ExperienceForm()
    return render(request, "add_experience.html", {"form": form, "resume": resume})


@login_required
def edit_experience(request, id):
    exp = get_object_or_404(Experience, id=id, resume__user=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save(); messages.success(request, "Experience updated.")
            return redirect("resume_detail", id=exp.resume.id)
    else:
        form = ExperienceForm(instance=exp)
    return render(request, "edit_experience.html", {"form": form, "experience": exp})


@login_required
def delete_experience(request, id):
    exp = get_object_or_404(Experience, id=id, resume__user=request.user)
    rid = exp.resume.id
    if request.method == "POST":
        exp.delete(); messages.success(request, "Experience deleted.")
        return redirect("resume_detail", id=rid)
    return render(request, "delete_confirm.html", {"title": "Delete Experience", "item": exp.job_title, "back_id": rid})


# ─── Project ─────────────────────────────────────────────────────────────────

@login_required
def add_project(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False); p.resume = resume; p.save()
            messages.success(request, "Project added.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = ProjectForm()
    return render(request, "add_project.html", {"form": form, "resume": resume})


@login_required
def edit_project(request, id):
    proj = get_object_or_404(Project, id=id, resume__user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=proj)
        if form.is_valid():
            form.save(); messages.success(request, "Project updated.")
            return redirect("resume_detail", id=proj.resume.id)
    else:
        form = ProjectForm(instance=proj)
    return render(request, "edit_project.html", {"form": form, "project": proj})


@login_required
def delete_project(request, id):
    proj = get_object_or_404(Project, id=id, resume__user=request.user)
    rid = proj.resume.id
    if request.method == "POST":
        proj.delete(); messages.success(request, "Project deleted.")
        return redirect("resume_detail", id=rid)
    return render(request, "delete_confirm.html", {"title": "Delete Project", "item": proj.project_name, "back_id": rid})


# ─── Skill ───────────────────────────────────────────────────────────────────

@login_required
def add_skill(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False); s.resume = resume; s.save()
            messages.success(request, "Skill added.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = SkillForm()
    return render(request, "add_skill.html", {"form": form, "resume": resume})


@login_required
def delete_skill(request, id):
    skill = get_object_or_404(Skill, id=id, resume__user=request.user)
    rid = skill.resume.id
    if request.method == "POST":
        skill.delete(); messages.success(request, "Skill deleted.")
        return redirect("resume_detail", id=rid)
    return render(request, "delete_confirm.html", {"title": "Delete Skill", "item": skill.skill_name, "back_id": rid})


# ─── Certificate ─────────────────────────────────────────────────────────────

@login_required
def add_certificate(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False); c.resume = resume; c.save()
            messages.success(request, "Certificate added.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = CertificateForm()
    return render(request, "add_certificate.html", {"form": form, "resume": resume})


@login_required
def delete_certificate(request, id):
    cert = get_object_or_404(Certificate, id=id, resume__user=request.user)
    rid = cert.resume.id
    if request.method == "POST":
        cert.delete(); messages.success(request, "Certificate deleted.")
        return redirect("resume_detail", id=rid)
    return render(request, "delete_confirm.html", {"title": "Delete Certificate", "item": cert.certificate_name, "back_id": rid})


# ─── Language ────────────────────────────────────────────────────────────────

@login_required
def add_language(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            l = form.save(commit=False); l.resume = resume; l.save()
            messages.success(request, "Language added.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = LanguageForm()
    return render(request, "add_language.html", {"form": form, "resume": resume})


@login_required
def delete_language(request, id):
    lang = get_object_or_404(Language, id=id, resume__user=request.user)
    rid = lang.resume.id
    if request.method == "POST":
        lang.delete(); messages.success(request, "Language deleted.")
        return redirect("resume_detail", id=rid)
    return render(request, "delete_confirm.html", {"title": "Delete Language", "item": lang.language, "back_id": rid})


# ─── Hobby ───────────────────────────────────────────────────────────────────

@login_required
def add_hobby(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == "POST":
        form = HobbyForm(request.POST)
        if form.is_valid():
            h = form.save(commit=False); h.resume = resume; h.save()
            messages.success(request, "Hobby added.")
            return redirect("resume_detail", id=resume.id)
    else:
        form = HobbyForm()
    return render(request, "add_hobby.html", {"form": form, "resume": resume})


@login_required
def delete_hobby(request, id):
    hobby = get_object_or_404(Hobby, id=id, resume__user=request.user)
    rid = hobby.resume.id
    if request.method == "POST":
        hobby.delete(); messages.success(request, "Hobby deleted.")
        return redirect("resume_detail", id=rid)
    return render(request, "delete_confirm.html", {"title": "Delete Hobby", "item": hobby.hobby_name, "back_id": rid})


# ─── AI Assistant ─────────────────────────────────────────────────────────────

@login_required
def ai_assistant(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    return render(request, "ai_assistant.html", {"resume": resume})


@login_required
@require_POST
def ai_generate_text(request, id):
    """
    Generate AI text via Gemini for one of several resume-writing tasks,
    selected by the `action` field in the POSTed JSON body:
      - "summary"             : career-objective paragraph
      - "suggest_skills"      : comma-separated list of relevant skills
      - "job_description"     : bullet points for a work-experience entry
      - "project_description" : short blurb for a project entry
      - "full_content"        : summary + skills together, as JSON

    Returns the generated text for the user to review/tweak in the UI
    before it's actually saved (see ai_save_text() below) -- Gemini output
    is never written straight to the resume without a human look first.
    """
    resume = get_object_or_404(Resume, id=id, user=request.user)
    try:
        data = json.loads(request.body)
        action = data.get("action", "")
        # Shared Gemini 2.5 Flash model (see get_gemini_model() at top of file).
        model = get_gemini_model()

        if action == "summary":
            skills = ", ".join([s.skill_name for s in resume.skills.all()]) or "various skills"
            exp = ", ".join([e.job_title for e in resume.experiences.all()]) or "relevant experience"
            prompt = f"""Write a compelling 3-4 sentence professional career summary for a {resume.profession} named {resume.full_name}.
Skills include: {skills}. Experience: {exp}.
Make it results-oriented, specific, and tailored to the role. Use strong action words.
Return only the summary paragraph, no labels or extra text."""

        elif action == "suggest_skills":
            existing = ", ".join([s.skill_name for s in resume.skills.all()])
            prompt = f"""List 10 in-demand skills for a {resume.profession}.
Existing skills: {existing or 'none'}.
Return ONLY a comma-separated list of skill names. No numbering, no explanation."""

        elif action == "job_description":
            prompt = f"""Write a professional job description for {data.get('job_title')} at {data.get('company_name')} ({data.get('employment_type', '')}).
Use 3-4 bullet points starting with strong action verbs. Focus on impact and achievements.
Return only the description text."""

        elif action == "project_description":
            prompt = f"""Write a concise 2-3 sentence project description for a resume.
Project: {data.get('project_name')}. Technologies: {data.get('technologies')}.
Mention what it does and its impact. Make it professional and achievement-focused.
Return only the description."""

        elif action == "full_content":
            years = data.get("years", "0")
            skills_hint = data.get("skills", "")
            prompt = f"""Generate professional resume content for {resume.full_name}, a {resume.profession} with {years} years experience.
Key skills: {skills_hint or 'not specified'}.
Return ONLY valid JSON with keys:
- summary: 3-4 sentence career objective
- skills: list of 8 skill name strings
No markdown, no explanation, only raw JSON."""

        else:
            return JsonResponse({"success": False, "error": "Unknown action"})

        response = model.generate_content(prompt)
        text = response.text.strip()

        if action == "full_content":
            text = text.replace("```json", "").replace("```", "").strip()
            import json as _json
            parsed = _json.loads(text)
            return JsonResponse({"success": True, "data": parsed})

        return JsonResponse({"success": True, "text": text})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@require_POST
def ai_save_text(request, id):
    """Save AI generated text to resume after user edits it."""
    resume = get_object_or_404(Resume, id=id, user=request.user)
    try:
        data = json.loads(request.body)
        field = data.get("field", "")
        text = data.get("text", "").strip()

        if field == "summary" and text:
            resume.summary = text
            resume.save()
            return JsonResponse({"success": True, "message": "Summary saved!"})

        elif field == "skills":
            skill_names = [s.strip() for s in text.split(",") if s.strip()]
            existing = [s.skill_name.lower() for s in resume.skills.all()]
            added = 0
            for name in skill_names:
                if name.lower() not in existing:
                    Skill.objects.create(resume=resume, skill_name=name, level="Intermediate")
                    added += 1
            return JsonResponse({"success": True, "message": f"{added} skills added!"})

        return JsonResponse({"success": False, "error": "Nothing to save."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# ─── Custom Admin Dashboard ───────────────────────────────────────────────────
# A lightweight, staff-only analytics dashboard (separate from Django's
# built-in /admin/) showing user growth, resume counts, template
# popularity and visitor traffic -- powered by the SiteVisitor rows that
# VisitorTrackingMiddleware records on every request.

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_dashboard(request):
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    new_today = User.objects.filter(date_joined__date=today).count()
    new_week = User.objects.filter(date_joined__gte=week_ago).count()
    new_month = User.objects.filter(date_joined__gte=month_ago).count()

    total_resumes = Resume.objects.count()
    resumes_today = Resume.objects.filter(created_at__date=today).count()

    visitors_today = SiteVisitor.objects.filter(visited_at__date=today).count()
    visitors_week = SiteVisitor.objects.filter(visited_at__gte=week_ago).count()
    realtime = SiteVisitor.objects.filter(visited_at__gte=now - timedelta(minutes=5)).values("ip_address").distinct().count()

    # Chart: visitors last 7 days
    daily = (
        SiteVisitor.objects.filter(visited_at__gte=week_ago)
        .annotate(date=TruncDate("visited_at"))
        .values("date").annotate(count=Count("id")).order_by("date")
    )
    chart_labels = json.dumps([str(d["date"]) for d in daily])
    chart_data = json.dumps([d["count"] for d in daily])

    # Chart: new users last 7 days
    user_daily = (
        User.objects.filter(date_joined__gte=week_ago)
        .annotate(date=TruncDate("date_joined"))
        .values("date").annotate(count=Count("id")).order_by("date")
    )
    user_chart_labels = json.dumps([str(d["date"]) for d in user_daily])
    user_chart_data = json.dumps([d["count"] for d in user_daily])

    template_stats = Resume.objects.values("template").annotate(count=Count("id")).order_by("-count")
    recent_users = User.objects.select_related("profile").order_by("-date_joined")[:8]
    recent_resumes = Resume.objects.select_related("user").order_by("-created_at")[:8]
    top_pages = SiteVisitor.objects.values("page").annotate(count=Count("id")).order_by("-count")[:8]

    return render(request, "custom_admin/dashboard.html", {
        "total_users": total_users, "active_users": active_users,
        "new_today": new_today, "new_week": new_week, "new_month": new_month,
        "total_resumes": total_resumes, "resumes_today": resumes_today,
        "visitors_today": visitors_today, "visitors_week": visitors_week,
        "realtime": realtime,
        "chart_labels": chart_labels, "chart_data": chart_data,
        "user_chart_labels": user_chart_labels, "user_chart_data": user_chart_data,
        "template_stats": template_stats,
        "recent_users": recent_users, "recent_resumes": recent_resumes,
        "top_pages": top_pages,
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_users(request):
    search = request.GET.get("q", "")
    users = User.objects.select_related("profile").order_by("-date_joined")
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    return render(request, "custom_admin/users.html", {"users": users, "search": search})


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_user_detail(request, user_id):
    u = get_object_or_404(User, id=user_id)
    resumes = Resume.objects.filter(user=u)
    return render(request, "custom_admin/user_detail.html", {"u": u, "resumes": resumes})


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_toggle_user(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if u != request.user:
        u.is_active = not u.is_active
        u.save()
        status = "activated" if u.is_active else "deactivated"
        messages.success(request, f"User {u.username} {status}.")
    return redirect("admin_users")


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_resumes(request):
    resumes = Resume.objects.select_related("user").order_by("-created_at")
    return render(request, "custom_admin/resumes.html", {"resumes": resumes})


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_realtime(request):
    now = timezone.now()
    realtime = SiteVisitor.objects.filter(visited_at__gte=now - timedelta(minutes=5)).values("ip_address").distinct().count()
    total_users = User.objects.count()
    total_resumes = Resume.objects.count()
    visitors_today = SiteVisitor.objects.filter(visited_at__date=now.date()).count()
    return JsonResponse({
        "realtime": realtime,
        "total_users": total_users,
        "total_resumes": total_resumes,
        "visitors_today": visitors_today,
    })
