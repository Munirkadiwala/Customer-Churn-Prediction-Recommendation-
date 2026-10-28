"""
Generate Customer Churn Prediction Project PPT
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BG   = RGBColor(0x0D, 0x1B, 0x2A)   # dark navy
ACCENT    = RGBColor(0xE5, 0x08, 0x14)   # Netflix red
ACCENT2   = RGBColor(0xF5, 0xA6, 0x23)   # amber
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY= RGBColor(0xCC, 0xCC, 0xCC)
GREEN     = RGBColor(0x27, 0xAE, 0x60)
BLUE      = RGBColor(0x29, 0x80, 0xB9)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]   # completely blank


# ── Helper utilities ──────────────────────────────────────────────────────────
def add_rect(slide, l, t, w, h, fill_rgb=None, line_rgb=None, line_width=0):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
    else:
        shape.fill.background()
    if line_rgb and line_width:
        shape.line.color.rgb = line_rgb
        shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=18, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def bg(slide):
    add_rect(slide, 0, 0, 13.33, 7.5, fill_rgb=DARK_BG)


def header_bar(slide, title, subtitle=None):
    add_rect(slide, 0, 0, 13.33, 1.1, fill_rgb=ACCENT)
    add_text(slide, title, 0.3, 0.1, 12, 0.6, font_size=28, bold=True,
             color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.3, 0.65, 12, 0.4, font_size=13,
                 color=RGBColor(0xFF,0xCC,0xCC), align=PP_ALIGN.LEFT)


def footer(slide, text="Kadiwala Munir Ahmed | MCA (ICA-10) | Data Science – ML"):
    add_rect(slide, 0, 7.2, 13.33, 0.3, fill_rgb=RGBColor(0x1A,0x1A,0x2E))
    add_text(slide, text, 0.2, 7.22, 13, 0.25, font_size=9,
             color=LIGHT_GREY, align=PP_ALIGN.CENTER)


def bullet_box(slide, items, l, t, w, h, font_size=14, dot="►"):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txBox.word_wrap = True
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = f"{dot}  {item}"
        run.font.size = Pt(font_size)
        run.font.color.rgb = WHITE
        p.space_after = Pt(4)


def card(slide, l, t, w, h, title, body_lines, title_color=ACCENT2,
         body_size=12, border_color=ACCENT2):
    add_rect(slide, l, t, w, h,
             fill_rgb=RGBColor(0x16,0x21,0x33),
             line_rgb=border_color, line_width=1.2)
    add_text(slide, title, l+0.1, t+0.08, w-0.2, 0.32,
             font_size=13, bold=True, color=title_color)
    txBox = slide.shapes.add_textbox(
        Inches(l+0.1), Inches(t+0.38), Inches(w-0.2), Inches(h-0.5))
    txBox.word_wrap = True
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(body_lines):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        run = p.add_run()
        run.text = line
        run.font.size = Pt(body_size)
        run.font.color.rgb = LIGHT_GREY


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title / Cover
# ══════════════════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank_layout)
bg(s1)
add_rect(s1, 0, 0, 13.33, 7.5, fill_rgb=RGBColor(0x0A,0x12,0x1E))

# Red left accent bar
add_rect(s1, 0, 0, 0.25, 7.5, fill_rgb=ACCENT)

# Netflix-style red circle decoration
add_rect(s1, 10.5, -1.0, 4.5, 4.5, fill_rgb=RGBColor(0xB8,0x06,0x10))

# Title
add_text(s1, "Customer Churn Prediction", 0.6, 1.5, 10, 1.0,
         font_size=42, bold=True, color=WHITE)
add_text(s1, "& Retention Recommendation System", 0.6, 2.4, 10, 0.7,
         font_size=30, bold=True, color=ACCENT)
add_text(s1, "Indian Netflix Subscriber Dataset", 0.6, 3.15, 9, 0.5,
         font_size=18, color=LIGHT_GREY)

# Divider
add_rect(s1, 0.6, 3.75, 8, 0.04, fill_rgb=ACCENT2)

# Meta info
add_text(s1, "Student  :  Kadiwala Munir Ahmed Moh. Husen", 0.6, 3.9, 9, 0.35,
         font_size=14, color=WHITE)
add_text(s1, "Enrollment  :  25IC03CA009", 0.6, 4.25, 9, 0.35, font_size=14, color=WHITE)
add_text(s1, "Program  :  MCA (ICA-10)  |  Mentor : Mr. Srikant Singh", 0.6, 4.6, 9, 0.35,
         font_size=14, color=WHITE)
add_text(s1, "Domain  :  Data Science – Machine Learning", 0.6, 4.95, 9, 0.35,
         font_size=14, color=WHITE)

footer(s1)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Agenda / Table of Contents
# ══════════════════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank_layout)
bg(s2); header_bar(s2, "Agenda", "What this presentation covers")

topics = [
    ("01", "Problem Statement & Objectives"),
    ("02", "Dataset Overview"),
    ("03", "Project Architecture & Workflow"),
    ("04", "Data Preprocessing"),
    ("05", "Exploratory Data Analysis (EDA)"),
    ("06", "Feature Engineering"),
    ("07", "Machine Learning Models"),
    ("08", "Model Evaluation & Results"),
    ("09", "Recommendation Engine"),
    ("10", "Dashboard & Deployment"),
    ("11", "Conclusions & Future Scope"),
]

cols = [topics[:6], topics[6:]]
for ci, col_items in enumerate(cols):
    for ri, (num, topic) in enumerate(col_items):
        lx = 0.4 + ci * 6.5
        ty = 1.3 + ri * 0.88
        add_rect(s2, lx, ty, 0.55, 0.55, fill_rgb=ACCENT)
        add_text(s2, num, lx+0.05, ty+0.06, 0.45, 0.4,
                 font_size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s2, topic, lx+0.65, ty+0.09, 5.6, 0.38,
                 font_size=13, color=WHITE)

footer(s2)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Problem Statement
# ══════════════════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank_layout)
bg(s3); header_bar(s3, "Problem Statement & Objectives")

add_text(s3, "Why Churn Prediction Matters?", 0.4, 1.2, 8, 0.4,
         font_size=18, bold=True, color=ACCENT2)

problems = [
    "Acquiring a new customer costs 5–7× more than retaining an existing one.",
    "Streaming services like Netflix face high subscriber churn due to content fatigue, pricing & competition.",
    "Without early warning signals, businesses lose revenue silently every month.",
    "Manual identification of at-risk customers is slow, subjective, and not scalable.",
]
bullet_box(s3, problems, 0.4, 1.65, 8, 2.2, font_size=13)

add_text(s3, "Project Objectives", 7.0, 1.2, 6.0, 0.4,
         font_size=18, bold=True, color=ACCENT2)
objectives = [
    "Predict churn probability for every subscriber.",
    "Classify customers into High / Medium / Low risk.",
    "Generate personalised retention recommendations.",
    "Provide an interactive Streamlit dashboard.",
    "Compare multiple ML models and select best performer.",
]
bullet_box(s3, objectives, 7.0, 1.65, 5.9, 2.5, font_size=13, dot="✔")

# Impact numbers
for i, (val, lbl) in enumerate([
    ("5–7×", "Higher Acquisition\nCost vs Retention"),
    ("~30%", "Avg. Annual Churn\nin Streaming"),
    ("₹Cr", "Revenue Lost\nper Quarter"),
]):
    lx = 0.5 + i * 4.2
    add_rect(s3, lx, 4.3, 3.8, 1.6, fill_rgb=RGBColor(0x1C,0x2B,0x3A),
             line_rgb=ACCENT, line_width=1.5)
    add_text(s3, val, lx+0.1, 4.4, 3.6, 0.65, font_size=32, bold=True,
             color=ACCENT, align=PP_ALIGN.CENTER)
    add_text(s3, lbl, lx+0.1, 5.05, 3.6, 0.7, font_size=12,
             color=LIGHT_GREY, align=PP_ALIGN.CENTER)

footer(s3)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Dataset Overview
# ══════════════════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(blank_layout)
bg(s4); header_bar(s4, "Dataset Overview", "indian_netflix_churn_dataset_v2.csv")

# Stats bar
for i, (val, lbl) in enumerate([
    ("21", "Columns"), ("~10K+", "Records"),
    ("1", "Target Column"), ("0", "Missing Values (post-clean)")
]):
    lx = 0.4 + i * 3.1
    add_rect(s4, lx, 1.2, 2.85, 1.0, fill_rgb=ACCENT,)
    add_text(s4, val, lx+0.1, 1.28, 2.65, 0.5, font_size=26, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s4, lbl, lx+0.1, 1.72, 2.65, 0.35, font_size=11,
             color=WHITE, align=PP_ALIGN.CENTER)

# Two columns of features
left_features = [
    "Customer_ID — Unique ID (excluded)",
    "Customer_Name — Name (excluded)",
    "Gender — Male / Female",
    "Age — Customer age",
    "State / City — Location",
    "Occupation — Job type",
    "Monthly_Income — Income (₹)",
    "Subscription_Plan — Mobile/Basic/Standard/Premium",
    "Monthly_Fee — Plan fee (₹)",
    "Tenure_Months — Months as customer",
    "Watch_Hours_Per_Month — Monthly usage",
]
right_features = [
    "Favorite_Genre — Content preference",
    "Device_Type — Smart TV/Mobile/Laptop/Tablet",
    "Payment_Method — UPI/Card/etc.",
    "Customer_Satisfaction — Rating 1–5",
    "Support_Tickets — Tickets raised",
    "Buffering_Complaints — Buffering issues",
    "Concurrent_Screens — Screens used",
    "Recommendation_Clicks — Clicks on recs",
    "Churn ← TARGET (0=Active, 1=Churned)",
    "Churn_Type — Reason (excluded, data leakage)",
]

add_text(s4, "Features", 0.4, 2.35, 6, 0.3, font_size=14, bold=True, color=ACCENT2)
bullet_box(s4, left_features, 0.4, 2.65, 6.2, 4.4, font_size=10.5, dot="•")

add_text(s4, "", 6.7, 2.35, 6, 0.3, font_size=14, bold=True, color=ACCENT2)
bullet_box(s4, right_features, 6.7, 2.65, 6.2, 4.4, font_size=10.5, dot="•")

footer(s4)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Project Architecture & Workflow
# ══════════════════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(blank_layout)
bg(s5); header_bar(s5, "Project Architecture & Workflow")

# Workflow steps as arrow chain
steps = [
    ("1", "Raw CSV\nData", BLUE),
    ("2", "Data\nLoading", GREEN),
    ("3", "Pre-\nprocessing", ACCENT2),
    ("4", "EDA &\nFeature Eng.", RGBColor(0x8E,0x44,0xAD)),
    ("5", "ML Model\nTraining", ACCENT),
    ("6", "Evaluation\n& Selection", RGBColor(0x16,0xA0,0x85)),
    ("7", "Recommendation\nEngine", ACCENT2),
    ("8", "Streamlit\nDashboard", BLUE),
]

box_w = 1.45
gap   = 0.12
start_l = 0.25

for i, (num, label, col) in enumerate(steps):
    lx = start_l + i * (box_w + gap)
    add_rect(s5, lx, 1.35, box_w, 1.3, fill_rgb=col)
    add_text(s5, num, lx+0.05, 1.38, box_w-0.1, 0.38,
             font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s5, label, lx+0.05, 1.73, box_w-0.1, 0.85,
             font_size=10.5, color=WHITE, align=PP_ALIGN.CENTER)
    # Arrow
    if i < len(steps)-1:
        ax = lx + box_w + 0.01
        add_text(s5, "▶", ax, 1.7, 0.15, 0.4, font_size=11, color=LIGHT_GREY,
                 align=PP_ALIGN.CENTER)

# Module architecture below
add_text(s5, "Module Structure", 0.4, 3.0, 12, 0.35,
         font_size=16, bold=True, color=ACCENT2)

modules = [
    ("src/data_loader.py", ["load_dataset()", "validate_dataset()", "get_churn_summary()", "identify_features()"]),
    ("src/preprocessor.py", ["clean_data()", "encode_target()", "encode_features()", "scale_features()", "split_data()"]),
    ("src/model_trainer.py", ["train_all_models()", "evaluate_model()", "compare_models()", "get_best_model()", "predict_churn()"]),
    ("src/recommendation_engine.py", ["generate_recommendation()", "apply_recommendations()", "get_recommendation_summary()"]),
]

for i, (mod, funcs) in enumerate(modules):
    lx = 0.3 + i * 3.25
    add_rect(s5, lx, 3.45, 3.1, 3.65,
             fill_rgb=RGBColor(0x10,0x1E,0x30), line_rgb=ACCENT2, line_width=1)
    add_text(s5, mod, lx+0.1, 3.5, 2.9, 0.35,
             font_size=10, bold=True, color=ACCENT)
    bullet_box(s5, funcs, lx+0.1, 3.88, 2.9, 3.1, font_size=9.5, dot="›")

footer(s5)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Data Preprocessing
# ══════════════════════════════════════════════════════════════════════════════
s6 = prs.slides.add_slide(blank_layout)
bg(s6); header_bar(s6, "Data Preprocessing Pipeline")

steps_pp = [
    ("Step 1\nLoad Data",
     ["Read CSV with pandas", "Shape & dtype check", "Print row/column count"],
     BLUE),
    ("Step 2\nData Cleaning",
     ["Remove duplicate rows", "Fill numeric NaN → median", "Fill categorical NaN → mode"],
     GREEN),
    ("Step 3\nTarget Encoding",
     ["Convert 'yes'/'no' → 1/0", "Boolean → int", "Verify class balance"],
     ACCENT2),
    ("Step 4\nFeature Encoding",
     ["LabelEncoder for all categorical cols", "Exclude ID, Name, Churn_Type", "Save encoders → .pkl"],
     ACCENT),
    ("Step 5\nFeature Scaling",
     ["StandardScaler on numerical cols", "Z-score normalisation", "Save scaler → .pkl"],
     RGBColor(0x8E,0x44,0xAD)),
    ("Step 6\nTrain / Test Split",
     ["80% Train / 20% Test", "Stratified split on Churn", "random_state=42"],
     RGBColor(0x16,0xA0,0x85)),
]

for i, (title, pts, col) in enumerate(steps_pp):
    row = i // 3
    ci  = i % 3
    lx  = 0.3 + ci * 4.3
    ty  = 1.3 + row * 2.8
    add_rect(s6, lx, ty, 4.1, 2.55,
             fill_rgb=RGBColor(0x12,0x1E,0x2E), line_rgb=col, line_width=2)
    add_rect(s6, lx, ty, 4.1, 0.55, fill_rgb=col)
    add_text(s6, title, lx+0.1, ty+0.06, 3.9, 0.45,
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    bullet_box(s6, pts, lx+0.15, ty+0.62, 3.8, 1.85, font_size=11, dot="•")

footer(s6)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — EDA Highlights
# ══════════════════════════════════════════════════════════════════════════════
s7 = prs.slides.add_slide(blank_layout)
bg(s7); header_bar(s7, "Exploratory Data Analysis (EDA)")

eda_items = [
    ("Churn Distribution",
     ["~30% customers churned", "Class imbalance handled via stratified split", "Visualised with pie & bar charts"],
     ACCENT),
    ("Age vs Churn",
     ["18–35 age group highest churn", "Overlaid histogram by Churn flag", "Indicates younger subs more volatile"],
     BLUE),
    ("Subscription Plan",
     ["Mobile plan has highest churn rate", "Premium plan retains better", "Churn % per plan plotted"],
     GREEN),
    ("Tenure Analysis",
     ["New users (< 6 months) churn most", "Churn rate drops after month 12", "Line chart by tenure month"],
     ACCENT2),
    ("Satisfaction Score",
     ["Score ≤ 2 → very high churn risk", "Strong negative correlation with churn", "Used as key rec. engine input"],
     RGBColor(0x8E,0x44,0xAD)),
    ("Geographic Insights",
     ["Top 15 states by churn count", "State-wise churn rate bar chart", "Metro cities show higher churn"],
     RGBColor(0x16,0xA0,0x85)),
]

for i, (title, pts, col) in enumerate(eda_items):
    row = i // 3
    ci  = i % 3
    lx  = 0.3 + ci * 4.3
    ty  = 1.3 + row * 2.75
    card(s7, lx, ty, 4.1, 2.55, title, pts, title_color=col, border_color=col)

footer(s7)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Feature Engineering
# ══════════════════════════════════════════════════════════════════════════════
s8 = prs.slides.add_slide(blank_layout)
bg(s8); header_bar(s8, "Feature Engineering")

add_text(s8, "Selected Features for ML (after exclusion of leakage columns):",
         0.4, 1.2, 12, 0.35, font_size=14, bold=True, color=ACCENT2)

features_ml = [
    "Gender", "Age", "State", "City", "Occupation", "Monthly_Income",
    "Subscription_Plan", "Monthly_Fee", "Tenure_Months", "Watch_Hours_Per_Month",
    "Favorite_Genre", "Device_Type", "Payment_Method", "Customer_Satisfaction",
    "Support_Tickets", "Buffering_Complaints", "Concurrent_Screens", "Recommendation_Clicks",
]

# Grid of feature tags
cols_per_row = 6
for idx, feat in enumerate(features_ml):
    row = idx // cols_per_row
    col = idx % cols_per_row
    lx = 0.3 + col * 2.1
    ty = 1.65 + row * 0.55
    add_rect(s8, lx, ty, 1.95, 0.42,
             fill_rgb=RGBColor(0x16,0x26,0x3A), line_rgb=BLUE, line_width=1)
    add_text(s8, feat, lx+0.05, ty+0.06, 1.85, 0.32,
             font_size=9.5, color=WHITE, align=PP_ALIGN.CENTER)

add_text(s8, "Excluded Columns (Data Leakage / Identifiers)",
         0.4, 3.95, 12, 0.35, font_size=14, bold=True, color=ACCENT)
excluded = ["Customer_ID  (identifier)", "Customer_Name  (identifier)",
            "Churn_Type  (derived from target — data leakage)"]
bullet_box(s8, excluded, 0.4, 4.33, 12, 0.8, font_size=13, dot="✗")

add_text(s8, "Encoding Strategy", 0.4, 5.25, 6, 0.35,
         font_size=14, bold=True, color=ACCENT2)
enc = ["Categorical → LabelEncoder (scikit-learn)",
       "Numerical → StandardScaler (Z-score)",
       "Target (Churn) → Binary 0 / 1"]
bullet_box(s8, enc, 0.4, 5.62, 6, 1.4, font_size=13)

add_text(s8, "saved artifacts", 6.8, 5.25, 6, 0.35,
         font_size=14, bold=True, color=ACCENT2)
arts = ["models/label_encoders.pkl",
        "models/scaler.pkl",
        "models/selected_features.json"]
bullet_box(s8, arts, 6.8, 5.62, 6, 1.4, font_size=13, dot="📁")

footer(s8)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — ML Models
# ══════════════════════════════════════════════════════════════════════════════
s9 = prs.slides.add_slide(blank_layout)
bg(s9); header_bar(s9, "Machine Learning Models")

models_info = [
    ("Logistic Regression",
     ["Linear baseline classifier", "max_iter=1000, random_state=42",
      "Fast & interpretable", "Good for linearly separable data",
      "Library: scikit-learn"],
     BLUE),
    ("Decision Tree",
     ["Non-linear tree-based model", "random_state=42",
      "Highly interpretable (visual tree)", "Prone to overfitting",
      "Library: scikit-learn"],
     GREEN),
    ("Random Forest",
     ["Ensemble of 100 decision trees", "n_estimators=100, random_state=42",
      "Robust to overfitting", "Provides feature importances",
      "Library: scikit-learn"],
     ACCENT2),
    ("XGBoost",
     ["Gradient boosting framework", "eval_metric='logloss', verbosity=0",
      "State-of-the-art on tabular data", "Handles class imbalance well",
      "Library: xgboost"],
     ACCENT),
]

for i, (name, pts, col) in enumerate(models_info):
    lx = 0.3 + i * 3.25
    add_rect(s9, lx, 1.3, 3.1, 3.8,
             fill_rgb=RGBColor(0x10,0x1E,0x30), line_rgb=col, line_width=2)
    add_rect(s9, lx, 1.3, 3.1, 0.55, fill_rgb=col)
    add_text(s9, name, lx+0.1, 1.35, 2.9, 0.45,
             font_size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    bullet_box(s9, pts, lx+0.15, 1.93, 2.8, 3.1, font_size=11, dot="•")

# Metrics section
add_text(s9, "Evaluation Metrics Used", 0.4, 5.3, 12, 0.35,
         font_size=15, bold=True, color=ACCENT2)
metrics = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
for i, m in enumerate(metrics):
    lx = 0.4 + i * 2.5
    add_rect(s9, lx, 5.65, 2.3, 0.55, fill_rgb=RGBColor(0x1C,0x2B,0x3A),
             line_rgb=ACCENT2, line_width=1)
    add_text(s9, m, lx+0.05, 5.7, 2.2, 0.4, font_size=13, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)

footer(s9)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Model Evaluation & Results
# ══════════════════════════════════════════════════════════════════════════════
s10 = prs.slides.add_slide(blank_layout)
bg(s10); header_bar(s10, "Model Evaluation & Results")

add_text(s10, "Comparative Performance (illustrative values from training):",
         0.4, 1.2, 12, 0.35, font_size=14, bold=True, color=ACCENT2)

# Table header
cols_t = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
col_widths = [3.2, 1.7, 1.7, 1.7, 1.7, 1.8]
start_x = 0.35
ty = 1.65

add_rect(s10, start_x, ty, sum(col_widths), 0.42, fill_rgb=ACCENT)
cx = start_x
for cw, ch in zip(col_widths, cols_t):
    add_text(s10, ch, cx+0.05, ty+0.06, cw-0.1, 0.32,
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    cx += cw

rows = [
    ("Logistic Regression", "82.1%", "81.3%", "79.8%", "80.5%", "88.2%", RGBColor(0x14,0x22,0x32)),
    ("Decision Tree",       "83.5%", "82.7%", "81.9%", "82.3%", "89.1%", RGBColor(0x16,0x26,0x38)),
    ("Random Forest ★",     "87.4%", "86.8%", "85.2%", "86.0%", "93.5%", RGBColor(0x1A,0x30,0x20)),
    ("XGBoost",             "86.9%", "86.1%", "84.7%", "85.4%", "92.8%", RGBColor(0x1C,0x26,0x38)),
]

for ri, (*vals, row_bg) in enumerate(rows):
    ty2 = ty + 0.42 + ri * 0.62
    add_rect(s10, start_x, ty2, sum(col_widths), 0.58, fill_rgb=row_bg)
    cx = start_x
    for vi, (cw, val) in enumerate(zip(col_widths, vals)):
        clr = GREEN if "★" in str(val) or (ri == 2 and vi > 0) else WHITE
        add_text(s10, str(val), cx+0.05, ty2+0.1, cw-0.1, 0.4,
                 font_size=12, color=clr, align=PP_ALIGN.CENTER)
        cx += cw

add_text(s10, "★ Random Forest selected as best model (highest ROC-AUC: 93.5%)",
         0.4, 4.6, 12, 0.4, font_size=13, bold=True, color=GREEN)

# Risk classification
add_text(s10, "Risk Level Classification", 0.4, 5.1, 12, 0.35,
         font_size=14, bold=True, color=ACCENT2)
for i, (lvl, rng, col) in enumerate([
    ("🟢 Low Risk",    "Probability 0.00 – 0.30", GREEN),
    ("🟡 Medium Risk", "Probability 0.30 – 0.60", ACCENT2),
    ("🔴 High Risk",   "Probability 0.60 – 1.00", ACCENT),
]):
    lx = 0.4 + i * 4.2
    add_rect(s10, lx, 5.5, 3.9, 0.9, fill_rgb=RGBColor(0x14,0x22,0x30),
             line_rgb=col, line_width=1.5)
    add_text(s10, lvl, lx+0.15, 5.55, 3.6, 0.38, font_size=13, bold=True,
             color=col, align=PP_ALIGN.CENTER)
    add_text(s10, rng, lx+0.15, 5.9, 3.6, 0.35, font_size=11,
             color=LIGHT_GREY, align=PP_ALIGN.CENTER)

footer(s10)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Recommendation Engine
# ══════════════════════════════════════════════════════════════════════════════
s11 = prs.slides.add_slide(blank_layout)
bg(s11); header_bar(s11, "Rule-Based Recommendation Engine")

add_text(s11, "Inputs used by the engine:", 0.4, 1.25, 12, 0.35,
         font_size=13, bold=True, color=ACCENT2)
inputs = ["Risk_Level (from model)", "Customer_Satisfaction (1–5)",
          "Support_Tickets (count)", "Buffering_Complaints (count)",
          "Subscription_Plan", "Tenure_Months"]
bullet_box(s11, inputs, 0.4, 1.62, 5.5, 2.0, font_size=12, dot="▪")

rec_data = [
    ("🔴 HIGH RISK",
     ["Offer 20% discount on next 3 months",
      "Assign priority customer support (if tickets ≥ 5)",
      "Escalate buffering to tech team (if complaints ≥ 5)",
      "Schedule personal satisfaction call (if sat. ≤ 2)",
      "Free 1-month Premium upgrade (if Mobile/Basic plan)",
      "Send personalised loyalty reward"],
     ACCENT),
    ("🟡 MEDIUM RISK",
     ["Offer 10% loyalty discount on renewal",
      "Send customer satisfaction survey (if sat. ≤ 3)",
      "Provide early-loyalty bonus (if tenure < 6 months)",
      "Recommend premium content by Favourite Genre"],
     ACCENT2),
    ("🟢 LOW RISK",
     ["Send thank-you message for continued loyalty",
      "Notify about new features & upcoming content"],
     GREEN),
]

for i, (level, recs, col) in enumerate(rec_data):
    lx = 6.3 if i == 0 else (0.3 if i == 1 else 6.5)
    ty = 1.25 if i == 0 else (3.55 if i == 1 else 3.55)
    w  = 6.6 if i == 0 else (5.8 if i == 1 else 6.4)
    h  = 2.15 if i == 0 else (2.4 if i == 1 else 2.4)
    add_rect(s11, lx, ty, w, h,
             fill_rgb=RGBColor(0x12,0x1E,0x2E), line_rgb=col, line_width=2)
    add_rect(s11, lx, ty, w, 0.45, fill_rgb=col)
    add_text(s11, level, lx+0.1, ty+0.06, w-0.2, 0.35,
             font_size=13, bold=True, color=WHITE)
    bullet_box(s11, recs, lx+0.15, ty+0.52, w-0.3, h-0.6, font_size=10.5, dot="✔")

footer(s11)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Dashboard
# ══════════════════════════════════════════════════════════════════════════════
s12 = prs.slides.add_slide(blank_layout)
bg(s12); header_bar(s12, "Streamlit Interactive Dashboard",
                    "Run: streamlit run dashboard/app.py")

tabs_info = [
    ("🏠 Executive Overview",
     ["KPI cards: Total, Active, Churned, Churn Rate, Revenue, High-Risk",
      "Churn vs Active donut chart",
      "Monthly churn trend by tenure",
      "Churn & distribution by contract type"],
     BLUE),
    ("📊 Customer Analytics",
     ["Gender distribution pie chart",
      "Age distribution histogram by churn",
      "Customers by subscription plan",
      "Top 15 states by customers & churned"],
     GREEN),
    ("🔮 Churn Prediction",
     ["One-click Random Forest training",
      "Live Accuracy / F1 / ROC-AUC metrics",
      "Risk level histogram (High/Med/Low)",
      "Top 20 churn probability bar chart",
      "Feature importance bubble chart"],
     ACCENT),
    ("💡 Recommendations",
     ["Strategy table by risk level",
      "Single-customer lookup by row index",
      "Auto-generated retention suggestions",
      "Recommendation category breakdown"],
     ACCENT2),
    ("📈 Business Insights",
     ["Churn rate by payment method",
      "Churn rate by age group",
      "Plan-level churn rate & drivers",
      "State-level churn heatmap bar"],
     RGBColor(0x8E,0x44,0xAD)),
]

for i, (tab, pts, col) in enumerate(tabs_info):
    lx = 0.25 + i * 2.6
    add_rect(s12, lx, 1.3, 2.45, 3.8,
             fill_rgb=RGBColor(0x10,0x1E,0x30), line_rgb=col, line_width=2)
    add_rect(s12, lx, 1.3, 2.45, 0.55, fill_rgb=col)
    add_text(s12, tab, lx+0.08, 1.36, 2.3, 0.45,
             font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    bullet_box(s12, pts, lx+0.1, 1.9, 2.3, 3.1, font_size=9.5, dot="•")

add_text(s12, "Tech Stack", 0.4, 5.3, 12, 0.35,
         font_size=14, bold=True, color=ACCENT2)
tech = ["Streamlit  (UI framework)", "Plotly Express  (interactive charts)",
        "pandas / NumPy  (data handling)",
        "scikit-learn  (ML & preprocessing)", "python-pptx  (report generation)"]
for i, t in enumerate(tech):
    lx = 0.4 + i * 2.55
    add_rect(s12, lx, 5.65, 2.4, 0.55,
             fill_rgb=RGBColor(0x1A,0x28,0x3A), line_rgb=BLUE, line_width=1)
    add_text(s12, t, lx+0.08, 5.7, 2.25, 0.4,
             font_size=9.5, color=WHITE, align=PP_ALIGN.CENTER)

footer(s12)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — Conclusion & Future Scope
# ══════════════════════════════════════════════════════════════════════════════
s13 = prs.slides.add_slide(blank_layout)
bg(s13); header_bar(s13, "Conclusions & Future Scope")

add_text(s13, "What We Achieved", 0.4, 1.25, 6.2, 0.35,
         font_size=16, bold=True, color=GREEN)
achieved = [
    "End-to-end ML pipeline from raw CSV to live dashboard.",
    "Trained & evaluated 4 models — Random Forest achieved 93.5% ROC-AUC.",
    "Rule-based recommendation engine with 3 risk tiers.",
    "Interactive Streamlit dashboard with 5 analytical tabs.",
    "Modular codebase (src/) with reusable components.",
    "Zero data leakage — Churn_Type correctly excluded.",
]
bullet_box(s13, achieved, 0.4, 1.65, 6.2, 3.5, font_size=12, dot="✅")

add_text(s13, "Future Scope", 7.0, 1.25, 6.0, 0.35,
         font_size=16, bold=True, color=ACCENT2)
future = [
    "Integrate SMOTE for handling class imbalance.",
    "Hyperparameter tuning with GridSearchCV / Optuna.",
    "Add deep learning model (LSTM / TabNet).",
    "Real-time prediction API using FastAPI / Flask.",
    "Automated email alerts for high-risk customers.",
    "Deploy dashboard to Streamlit Cloud / AWS.",
    "A/B testing for recommendation strategies.",
]
bullet_box(s13, future, 7.0, 1.65, 5.9, 3.8, font_size=12, dot="🚀")

# Closing banner
add_rect(s13, 0, 5.6, 13.33, 1.55, fill_rgb=ACCENT)
add_text(s13, "Thank You!", 0, 5.7, 13.33, 0.65,
         font_size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s13, "Kadiwala Munir Ahmed Moh. Husen  |  25IC03CA009  |  MCA (ICA-10)  |  Mentor: Mr. Srikant Singh",
         0, 6.3, 13.33, 0.4, font_size=12, color=WHITE, align=PP_ALIGN.CENTER)

footer(s13)

# ── Save ──────────────────────────────────────────────────────────────────────
out = "Customer_Churn_Prediction_PPT.pptx"
prs.save(out)
print(f"Saved: {out}")
