# Moon Studio — ארכיטקטורת מערכת הסוכנים

> מסמך עבודה פנימי — עודכן מרץ 2026

---

## 1. חזון המערכת

Moon Studio בונה מערכת סוכני AI שמריצה את חלקי הניהול של העסק — כך שדביר יכול להתרכז ביצירה, לא בתפעול.

**הבעיות שהמערכת פותרת:**
- מעקב לידים ופולואפ — מי פנה, מה הסטטוס, מי נשכח
- מעקב תזרים — מה נשלח, מה שולם, מה חייב
- שיווק פנימי — תוכן אורגני, מחקר מתחרים, רעיונות שבועיים
- ניהול ייצור — לוחות צילום, call sheets, פרילנסרים

> **עיקרון מנחה:** הסוכנים מריצים, לא מחליטים. דביר מאשר החלטות אסטרטגיות וכספיות.

---

## 2. ארכיטקטורת שלוש שכבות

| שכבה | תיאור |
|------|-------|
| **שכבה 1** | דביר — הוראות, אישורים, החלטות אסטרטגיות |
| **שכבה 2** | Orchestrator — מנתב בין הסוכנים, מתאם, מעלה לדביר כשצריך |
| **שכבה 3** | 7 סוכנים מומחים — כל אחד אחראי על תחום אחד בלבד |

---

## 3. הסוכנים

| סוכן | קובץ | אחריות |
|------|------|--------|
| **Orchestrator** | `agents/orchestrator.md` | מנתב, מתאם, מעלה לדביר |
| **Project Manager** | `agents/project_manager.md` | לידים, פרויקטים, Supabase CRM |
| **Finance** | `agents/finance.md` | הצעות מחיר, חשבוניות, תזרים |
| **Client Relations** | `agents/client_relations.md` | פולואפ, Gmail drafts, יחסי לקוחות |
| **Content** | `agents/content.md` | סקריפטים, בריפים, הצעות ללקוח |
| **Marketing** | `agents/marketing.md` | תוכן פנימי: מחקר, רעיונות, סקריפטים, לוח צילום |
| **Production Coord** | `agents/production_coord.md` | ימי צילום, call sheet, פרילנסרים |
| **Supervisor** | `agents/supervisor.md` | דוח יומי — מה קרה, מה ההשפעה |

**כללי Escalation — מתי לעצור ולשאול את דביר:**
- ליד חדש מסגמנט היעד (היי-טק, מותג, מסעדה) — **מיד**
- הנחה מבוקשת מעל 15%
- הצעת מחיר מעל 17,000 ₪ לפני שליחה
- תשלום שלא הגיע ביותר מ-7 ימים
- פרויקט שחורג מלוח הזמנים ב-48+ שעות

---

## 4. מבנה תיקיות — ABCTOM

| תיקייה | מטרה | קבצים עיקריים |
|--------|------|----------------|
| `agents/` | הגדרות הסוכנים | orchestrator.md + 7 סוכנים |
| `brain/` | לוגיקת החלטות וניתוב | router.md |
| `core/` | utilities משותפים | schemas, prompt templates |
| `tools/` | חיבורים לכלים חיצוניים | supabase.md, gmail.md, calendar.md, quote-generator/ |
| `memory/` | זיכרון עסקי — לא לדרוס! | business_context.json |
| `output/` | כל התוצרים | ראה סעיף 5 |
| `docs/` | מסמכי הנחייה | ARCHITECTURE.md, WORKING_INSTRUCTIONS.md |

---

## 5. מבנה output/

| תיקייה | מי כותב לשם | תוכן |
|--------|------------|------|
| `output/projects/` | Project Manager | leads.json, תיקייה לכל פרויקט |
| `output/quotes/` | Finance | PDF הצעות מחיר |
| `output/invoices/` | Finance | חשבוניות |
| `output/content/` | Content | סקריפטים, בריפים, הצעות ללקוח |
| `output/clients/` | Client Relations | followup_log.json לכל לקוח |
| `output/marketing/ideas/` | Marketing | רשימות רעיונות שבועיות |
| `output/marketing/scripts/` | Marketing | סקריפטים פנימיים לסטודיו |
| `output/marketing/research/` | Marketing | מחקר מתחרים שבועי |
| `output/production/` | Production Coord | לוחות צילום, call sheets |
| `output/supervisor/` | Supervisor | דוחות יומיים |

---

## 6. שכבת הזיכרון

| שכבה | תיאור | מיקום |
|------|-------|-------|
| **Hot** | Working memory — השיחה הפעילה | session בלבד |
| **Warm** | Episodic memory — היסטוריית פרויקטים | `output/projects/` |
| **Cold** | Semantic memory — ידע עסקי קבוע | `memory/business_context.json` |
| **CRM** | Real-time data — לידים, פרויקטים, משימות | Supabase (`tools/supabase.md`) |

---

## 7. כלים וחיבורים

| כלי | שימוש | סטטוס |
|-----|-------|-------|
| **Quote Generator** | PDF הצעות מחיר | ✅ פעיל |
| **Supabase CRM** | לידים, פרויקטים, משימות | 🔄 דורש הגדרת .env |
| **Google Calendar** | לוח צילומים + ימי תוכן | ✅ MCP מחובר |
| **Gmail** | טיוטות פולואפ + הצעות | ✅ MCP מחובר |
| **Slack / WhatsApp** | התראות | ⬜ שלב עתידי |

---

## 8. Workflows מרכזיים

### Workflow 1: ליד חדש נכנס
1. PM → רושם ב-Supabase + מסווג
2. **סגמנט יעד → התראה מיידית לדביר**
3. Client Relations → טיוטת מייל היכרות (24 שעות)
4. Finance → טיוטת הצעת מחיר (quote-generator)
5. **דביר מאשר ושולח — אף סוכן לא שולח לבד**

### Workflow 2: תוכן פנימי
1. Marketing → מחקר מתחרים (כל שני)
2. Marketing → רשימת רעיונות → **דביר מאשר**
3. Marketing → סקריפט → **דביר מאשר**
4. Marketing → תזמון יום צילום ב-Calendar
5. **דביר מצלם ומפרסם**

### Workflow 3: פרויקט נסגר
1. PM → סטטוס "סגור" ב-Supabase
2. Finance → חשבונית סופית → **דביר מאשר ושולח**
3. Client Relations → מייל סיום + בקשת המלצה

### Workflow 4: דוחות אוטומטיים (Cron)
- כל יום 17:57 — Supervisor → דוח יומי
- כל ראשון 08:53 — PM → דוח שבועי
- כל שני 09:03 — Marketing → רעיונות שבועיים
- כל 1 בחודש 09:07 — Finance → דוח תזרים

---

## 9. כלל זהב

> **תמיד לקרוא קודם:**
> `docs/ARCHITECTURE.md` → `docs/WORKING_INSTRUCTIONS.md` → `memory/business_context.json` → `agents/orchestrator.md` → `brain/router.md`
