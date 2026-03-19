# Moon Studio — ארכיטקטורת מערכת הסוכנים

> מסמך עבודה פנימי — מרץ 2026

---

## 1. חזון המערכת

Moon Studio בונה מערכת סוכני AI שמריצה את חלקי הניהול של העסק — כך שדביר יכול להתרכז ביצירה, לא בתפעול.

**הבעיות שהמערכת פותרת:**
- ניהול לקוחות ולידים — מי פנה, מה הסטטוס, מי תקוע
- מעקב תזרים — מה נשלח, מה שולם, מה חייב
- תפעול שיווק — תוכן, פנייה פרואקטיבית, לידים חדשים
- ניהול זמן — לוח שבועי, תזכורות, סדרי עדיפויות

> **עיקרון מנחה:** הסוכנים מריצים, לא מחליטים. דביר מאשר החלטות אסטרטגיות וכספיות. הסוכנים חוסכים את הזמן.

---

## 2. ארכיטקטורת שלוש שכבות

| שכבה | תיאור |
|------|-------|
| **שכבה 1** | דביר — הוראות, אישורים, החלטות אסטרטגיות |
| **שכבה 2** | Orchestrator — מנתב בין הסוכנים, מתאם, מעלה לדביר כשצריך |
| **שכבה 3** | סוכנים מומחים — כל אחד אחראי על תחום אחד בלבד |

**עיקרון הניתוב:** כל בקשה נכנסת עוברת דרך ה-Orchestrator. הוא קורא את `brain/router.md` ומחליט לאיזה סוכן לנתב — ומתי לעצור ולשאול את דביר.

---

## 3. הסוכנים

| סוכן | קובץ הגדרה | אחריות |
|------|------------|--------|
| **Orchestrator** | `agents/orchestrator.md` | מנתב, מתאם, מעלה לדביר — ה-brain |
| **Project Manager** | `agents/project_manager.md` | לידים, פרויקטים פעילים, לוחות זמנים, דוח שבועי |
| **Finance** | `agents/finance.md` | הצעות מחיר, חשבוניות, מעקב תשלומים, תזרים חודשי |
| **Marketing** | `agents/marketing.md` | שיווק פרואקטיבי, תוכן, פנייה להיי-טק/מסעדות/מותגים |
| **Content** | `agents/content.md` | סקריפטים, בריפים, כתוביות, קריאטיב |
| **Production Coord** | `agents/production_coord.md` | לוחות צילום, ציוד, call sheet, תיאום |

**כללי Escalation — מתי סוכן מפסיק ושואל את דביר:**
- ליד חדש מסגמנט היעד (היי-טק, מסעדה, מותג, משרד פרסום)
- הצעת מחיר מעל 15,000 ₪ לפני שליחה
- הנחה מבוקשת מעל 10%
- תשלום שלא הגיע ביותר מ-7 ימים
- פרויקט שחורג מלוח הזמנים ב-48+ שעות
- כל החלטה שמשפיעה על הכיוון האסטרטגי

---

## 4. מבנה תיקיות — ABCTOM

| תיקייה | מטרה | קבצים עיקריים |
|--------|------|----------------|
| `agents/` | הגדרות הסוכנים | orchestrator.md, project_manager.md, finance.md, marketing.md, content.md, production_coord.md |
| `brain/` | לוגיקת החלטות וניתוב | router.md — עץ ניתוב מלא, כללי זהב, דפוסי זמן |
| `core/` | utilities משותפים | schemas, prompt templates, shared functions |
| `tools/` | חיבורים לכלים חיצוניים | quote-generator/, crm.md, calendar.md, gmail.md |
| `memory/` | זיכרון עסקי — לא לדרוס! | business_context.json |
| `output/` | כל התוצרים | projects/leads.json, quotes/, invoices/, content/, marketing/ |
| `docs/` | מסמכי הנחייה | ARCHITECTURE.md, WORKING_INSTRUCTIONS.md, RESEARCH.md, BUSINESS_DEEP.md |

---

## 5. שכבת הזיכרון

**`memory/business_context.json` — מה בפנים:**
- פרטי העסק: שם, סוג, שפה, בעלים
- שירותים ומחירים: כל שירות עם מחיר מדויק
- Pricing tiers: קטן / בינוני / גדול עם טווחים
- מדיניות הנחות: מקסימום 10% בלי אישור דביר
- לקוחות: mix נוכחי + סגמנטי יעד + הערה אסטרטגית
- העדפות דביר: סגנון דוח, מתי להעלות, מה חשוב
- Tone & Voice: איך לדבר עם לקוחות ואיך עם דביר

**שלוש שכבות זיכרון:**

| שכבה | תיאור | מיקום |
|------|-------|-------|
| 🔴 **Hot** | Working memory — הפרויקט/השיחה הפעילה | session בלבד |
| 🟡 **Warm** | Episodic memory — היסטוריית פרויקטים | `output/projects/` |
| 🔵 **Cold** | Semantic memory — ידע עסקי קבוע | `memory/business_context.json` |

---

## 6. כלים וחיבורים

| כלי | שימוש | חיבור | סטטוס |
|-----|-------|-------|-------|
| **Quote Generator** | יצירת הצעות מחיר PDF | Python script מקומי | ✅ פעיל |
| **CRM (Supabase)** | לידים, פרויקטים, משימות | API קיים (Vercel) | 🔄 הבא לבנות |
| **Google Calendar** | לוח זמנים, ימי צילום | MCP מחובר ב-Claude | 🔄 הבא לבנות |
| **Gmail** | שליחת הצעות, followup | MCP מחובר ב-Claude | 🔄 הבא לבנות |
| **WhatsApp Business** | תזכורות ללקוחות | API + MCP עתידי | ⬜ שלב עתידי |

---

## 7. Workflows מרכזיים

### Workflow 1: ליד חדש נכנס
1. PM Agent → רושם ומסווג לפי סגמנט
2. **אם סגמנט יעד → התראה מיידית לדביר**
3. Finance Agent → טיוטת הצעת מחיר (quote-generator skill) תוך 24 שעות
4. **דביר מאשר ושולח — אף סוכן לא שולח לבד**
5. PM Agent → מעדכן סטטוס ל"הצעה נשלחה"

### Workflow 2: פרויקט נסגר
1. PM Agent → מסמן פרויקט כ"סגור"
2. Finance Agent → חשבונית סופית
3. **דביר מאשר ושולח חשבונית**
4. Marketing Agent → בקשת המלצה / case study

### Workflow 3: דוח שבועי (כל יום ראשון)
- PM Agent → לידים השבוע | סגירות | פרויקטים פעילים | עיכובים
- Finance Agent → מה נכנס | מה ממתין | חובות פתוחים
- Orchestrator → מרכז הכל, שולח לדביר כ-bullet points קצר

---

## 8. מפת הדרכים — 6 שלבים

| # | שלב | מה נבנה | סטטוס |
|---|-----|---------|-------|
| **1** | יסודות + GitHub | repo, מבנה ABCTOM, CLAUDE.md | ✅ הושלם |
| **2** | Memory + Orchestrator | business_context.json, orchestrator.md, brain/router.md | ✅ הושלם |
| **3** | סוכנים ראשוניים | project_manager.md, finance.md, marketing.md, content.md, production_coord.md | ✅ הושלם |
| **4** | Context + Self-Eval | docs/, eval criteria, context management | 🔄 בתהליך |
| **5** | חיבור כלים (MCP) | tools/crm.md (Supabase), calendar.md, gmail.md | ⬜ הבא |
| **6** | Scale + Optimize | מדדים, שיפורים, אוטומציות | ⬜ עתידי |

---

## 9. כלל זהב

> **תמיד לקרוא קודם:**
> `docs/ARCHITECTURE.md` → `docs/WORKING_INSTRUCTIONS.md` → `memory/business_context.json` → `agents/orchestrator.md` → `brain/router.md`
